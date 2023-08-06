# AVIV CDK for Python

A set of AWS CDK examples and constructs.

## Install

Requires:

- Python >= 3.6, pip
- cdk

```sh
npm install -g aws-cdk
pip install aviv-cdk

# With 'extra' to install additionnal libraries
pip install aviv-cdk[data]
```

## Use it

```python
import aviv_cdk
```

### CICD

```python
from aws_cdk import App
from aviv_cdk.cicd.stack import CodePipelineStack

app = App()
CodePipelineStack(
    app, 'cicd-stack',
    connections={'myorg': dict(connection_name='myorg')},
    sources={'cicd-stack': dict(repo_string='myorg/repo', branch='main')},
    pipeline=dict(
        self_mutation=False
    )
  )
app.synth()
```

### Route53

```python
from aviv_cdk.route53 import DomainZone

# Creates a new HostedZone
z = DomainZone(stack, 'myzone', fqdn='mydomain.com')
# add record
z.a('toto.mydomain.com', '10.0.0.1')

# Use an existing Zone
z = DomainZone(stack, 'myzone', fqdn='mydomain.com', zone_id='42')
z.txt('mydomain.com', 'my-dummy-check')
```

### RDS

### Fargate

## Development

### Develop and contribute :)

Requirements:

- pipenv, cdk client
- [optional] docker & AWS codebuild docker image (standard >= 4.0)

```sh
git clone https://github.com/aviv-group/aviv-cdk-python && cd aviv-cdk-python
pipenv install -d -e .

# Build with codebuild agent - see: buildspec.yml
codebuild_build.sh -i aws/codebuild/standard:4.0 -a cdk.out

# Run tests
pipenv run pytest -v tests/
```

### Build, distrib & release

_Requires __twine__ to be installed (`pip install twine`) and credentials to upload a new verison to pypi._

```sh
# Test and build
python3 setup.py sdist bdist_wheel

# Release on pypi
python3 -m twine upload --repository testpypi dist/*
python3 -m twine upload --repository pypi dist/*
```

## Contribute

Yes please! Fork this project, tweak it and share it back by sending your PRs.  
Have a look at the [TODO's](TODO) and [changelog](CHANGELOG) file if you're looking for inspiration.

## License

This project is developed under the [MIT license](license).

## Author(s) and Contributors

- Jules Clement \<jules.clement@aviv-group.com>
