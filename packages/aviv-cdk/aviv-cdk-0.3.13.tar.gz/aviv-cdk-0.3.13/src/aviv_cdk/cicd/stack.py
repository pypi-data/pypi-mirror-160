import os
import logging
import typing
from constructs import Construct
from aws_cdk import (
    Stack,
    aws_ssm,
    aws_iam,
    aws_lambda,
    aws_codestarconnections,
    aws_codestarnotifications,
    aws_codepipeline,
    aws_codepipeline_actions,
    aws_sns,
    aws_sns_subscriptions,
    pipelines
)
from .connections import GithubConnection
from .sources import github_url_split


class CodePipelineStack(Stack):
    _notif_github_statuses: aws_lambda.Function=None
    _connections: typing.Dict[str, aws_codestarconnections.CfnConnection]={}
    _sources: typing.Dict[str, pipelines.CodePipelineSource]={}
    codepipeline: pipelines.CodePipeline=None
    __connections_ssm: list=[]
    # source: pipelines.CodePipelineSource
    # waves: typing.Dict[str, pipelines.Wave]={}
    # stages: typing.Dict[str, typing.Dict[str, Stage]]={}

    def __init__(
            self,
            scope: Construct, id: str,
            *, 
            connections: typing.Dict[str, dict]={},
            sources: typing.Dict[str, dict]={},
            pipeline: dict=None,
            **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.connections = self.add_connections(connections)
        self.sources = self.add_sources(sources)
        if pipeline:
            if 'id' not in pipeline:
                pipeline['id'] = id
            self.codepipeline = self.add_codepipeline(**pipeline)

    @property
    def connections(self) -> typing.Dict[str, aws_codestarconnections.CfnConnection]:
        return self._connections

    @connections.setter
    def connections(self, values: dict) -> None:
        self._connections = {}
        for name, connection in values.items():
            if not connection.startswith('arn:aws:codestar-connections') \
                and not connection.startswith('${Token[TOKEN'): # and not connection.startswith('dummy-value-for-'):
                logging.warning(f"{name} not a CS arn {connection}")
            self._connections[name] = connection

    def add_connections(self, values: dict) -> typing.Dict[str, aws_codestarconnections.CfnConnection]:
        """A dict of CodestarConnections arn by name

        Args:
            connections (dict): CodestarConnections by name and connection details

            connection details can be:
            - ConnectionARN
            - SSM
            - Connection attributes like {"myorg": {"connection_name": "myorg"}, "org2": ...}
        """
        connections = {}
        for name, connection in values.items():
            if isinstance(connection, dict):
                connection = GithubConnection(self, name, **connection).arn
            if connection.startswith('aws:ssm:'):
                self.__connections_ssm.append(connection.replace('aws:ssm:', ''))
                connection = aws_ssm.StringParameter.value_from_lookup(self, parameter_name=connection.replace('aws:ssm:', ''))
            connections[name] = connection
        return connections



    @property
    def sources(self) -> typing.Dict[str, pipelines.CodePipelineSource]:
        return self._sources

    @sources.setter
    def sources(self, values: dict) -> None:
        self._sources = values

    def add_sources(self, values: dict) -> typing.Dict[str, pipelines.CodePipelineSource]:
        sources = {}
        for name, source in values.items():
            if isinstance(source, str):
                source ={'url': source}
            if 'url' in source:
                git = github_url_split(url=source['url'])
                del source['url']
                source['repo_string'] = f"{git['owner']}/{git['repo']}"
                source['branch'] = git['branch']
            owner = source['repo_string'].split('/')[0]
            if 'connection_arn' not in source and owner in self.connections:
                source['connection_arn'] = self.connections[owner]
            sources[name] = pipelines.CodePipelineSource.connection(**source)
        return sources



    def add_codepipeline(self, id: str, *, synth: dict={}, **pipelineargs) -> pipelines.CodePipeline:
        if 'synth' not in pipelineargs:
            if isinstance(synth, dict):
                if 'input' not in synth and id in self.sources:
                    synth['input'] = self.sources[id]
                    # Automagically add all sources to synth
                    synth['additional_inputs'] = dict((k, v) for k, v in self.sources.items() if k != id)
                synth = self.add_shellstep(f"{id}-synth", **synth)
            pipelineargs['synth'] = synth
        elif synth:
            logging.warning(f"synth already defined, not applying {synth}")
        if 'pipeline_name' not in pipelineargs:
            pipelineargs['pipeline_name'] = id
        return pipelines.CodePipeline(self, id, **pipelineargs)

    def add_shellstep(self, id: str, **synth) -> pipelines.ShellStep:
        if 'commands' not in synth:
            synth['commands']=[
                'pip install aviv-cdk',
                'npm install -g aws-cdk',
                'cdk synth'
            ]
        return pipelines.ShellStep(id, **synth)

    def ssm_policies(self, codepipeline: pipelines.CodePipeline):
        """Add required IAM policy to codebuild project role in order to fetch SSM Parameters
        (used to store codestar-connections arn per Github 'owner' (aka Github organization))

        Args:
            pipeline (pipelines.CodePipeline): [description]
        """
        codepipeline.synth_project.add_to_role_policy(aws_iam.PolicyStatement(
            actions=["ssm:GetParameter"],
            resources=list(
                f"arn:aws:ssm:{self.region}:{self.account}:parameter{connect_ssm}"
                for connect_ssm in self.__connections_ssm
            ),
            effect=aws_iam.Effect.ALLOW
        ))

    def enable_notif_github_statuses(self, codepipeline: pipelines.CodePipeline):
        # Build pipeline
        # codepipeline.build_pipeline()

        # Create notif topic and bind to pipeline exec events
        topic = aws_sns.Topic(self, 'topic', topic_name=f"{self.codepipeline.pipeline.pipeline_name}-status")
        topic.add_subscription(aws_sns_subscriptions.LambdaSubscription(self.notif_github_statuses))
        codepipeline.pipeline.notify_on(
            'notify-status',
            target=topic,
            detail_type=aws_codestarnotifications.DetailType.FULL,
            events=[
                aws_codepipeline.PipelineNotificationEvents.PIPELINE_EXECUTION_FAILED,
                aws_codepipeline.PipelineNotificationEvents.PIPELINE_EXECUTION_CANCELED,
                aws_codepipeline.PipelineNotificationEvents.PIPELINE_EXECUTION_STARTED,
                aws_codepipeline.PipelineNotificationEvents.PIPELINE_EXECUTION_RESUMED,
                aws_codepipeline.PipelineNotificationEvents.PIPELINE_EXECUTION_SUPERSEDED,
                aws_codepipeline.PipelineNotificationEvents.PIPELINE_EXECUTION_SUCCEEDED
            ]
        )

    @property
    def notif_github_statuses(self) -> aws_lambda.Function:
        if not self._notif_github_statuses:
            self._notif_github_statuses = self.github_statuses()
        return self._notif_github_statuses

    def github_statuses(self, path: str=f"{os.path.dirname(__file__)}/notif.py") -> aws_lambda.Function:
        with open(path, encoding="utf8") as fp:
            code = fp.read()
        return aws_lambda.Function(
            self, 'notif',
            handler='index.lambda_handler',
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            code=aws_lambda.InlineCode(code),
            description='Github status with https://docs.github.com/en/rest/commits/statuses',
            environment={
                "GH_TOKEN": os.environ.get("GH_TOKEN", ""),
            },
            initial_policy=[
                aws_iam.PolicyStatement(
                    actions=['codepipeline:GetPipelineExecution'],
                    resources=['arn:aws:codepipeline:*:*:*']
                ),
                aws_iam.PolicyStatement(
                    actions=['logs:CreateLogGroup', 'logs:CreateLogStream', 'logs:PutLogEvents'],
                    resources=['arn:aws:logs:*:*:*']
                )
            ]
        )
