import json
import boto3
import os
import urllib3


def lambda_handler(event, context):
    message = event['Records'][0]['Sns']['Message']
    data = json.loads(message)
    print(data)

    #Push only notifications about Pipeline Execution State Changes
    if data.get("detailType") != "CodePipeline Pipeline Execution State Change":
        return()

    response = boto3.client('codepipeline').get_pipeline_execution(
        pipelineName=data['detail']['pipeline'],
        pipelineExecutionId=data['detail']['execution-id']
    )
    print(response)
    commit_id = response['pipelineExecution']['artifactRevisions'][0]['revisionId']
    repo_id = response['pipelineExecution']['artifactRevisions'][0]['revisionUrl'].split("FullRepositoryId=")[1].split("&")[0]

    #Based on https://docs.github.com/en/free-pro-team@latest/rest/reference/repos#statuses
    if data['detail']['state'].upper() in [ "SUCCEEDED" ]:
        state = "success"
    elif data['detail']['state'].upper() in [ "STARTED", "STOPPING", "STOPPED", "SUPERSEDED" ]:
        state = "pending"
    else:
        state = "error"

    region = os.environ['AWS_REGION']
    build_status={}
    build_status['state'] = state
    build_status['context'] = "CodePipeline"
    build_status['description'] = data['detail']['pipeline']
    build_status['target_url'] = "https://" + region + ".console.aws.amazon.com/" \
        + "codesuite/codepipeline/pipelines/" + data['detail']['pipeline'] \
        + "/executions/" + data['detail']['execution-id'] + "?region=" + region

    print(build_status)
    gh_token = os.environ['GH_TOKEN']
    http = urllib3.PoolManager()
    r = http.request(
        'POST', "https://api.github.com/repos/" + repo_id + "/statuses/" + commit_id,
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'Curl/0.1',
            'Authorization' : f"token {gh_token}"
        },
        body=json.dumps(build_status).encode('utf-8')
    )

    print(r.data)
    return message
