from tracardi.domain.resources.github import GitHub
from tracardi.process_engine.action.v1.connectors.github.github_client import GitHubClient
from tracardi.process_engine.action.v1.connectors.github.model.config import Configuration
from tracardi.service.plugin.domain.register import Plugin, Spec, Form, MetaData, FormComponent, FormField, FormGroup, \
    Documentation, PortDoc
from tracardi.service.plugin.domain.result import Result
from tracardi.service.plugin.runner import ActionRunner
from tracardi.service.storage.driver import storage


def validate(config: dict):
    return Configuration(**config)


class GitHubListIssuesAction(ActionRunner):
    config: Configuration
    credentials: GitHub

    async def set_up(self, init):
        self.config = validate(init)
        resource = await storage.driver.resource.load(self.config.resource.id)
        self.credentials = resource.credentials.get_credentials(self, output=GitHub)

    async def run(self, payload: dict, in_edge=None):
        client = GitHubClient(self.credentials, self.config, self.console)
        response = await client.list_issues()
        return Result(
            port='payload',
            value=response,
        )


def register() -> Plugin:
    # TODO
    return Plugin(
        start=False,
        spec=Spec(
            module=__name__,
            className=GitHubListIssuesAction.__name__,
            inputs=['payload'],
            outputs=['payload'],
            version='0.1',
            license='MIT',
            author='knittl',
            init={
                'resource': {
                    'id': '',
                    'name': ''
                },
                'timeout': 30,
                'issue_id': '', # TODO split configs (list|get)
            },
            form=Form(groups=[
                FormGroup(
                    fields=[
                        FormField(
                            id='resource',
                            name='Resource',
                            description='Select your GitHub resource.',
                            component=FormComponent(
                                type='resource',
                                props={'label': 'GitHub Resource', 'tag': 'github'})
                        ),
                        FormField(
                            id='timeout',
                            name='Timeout',
                            description='Timeout for requests.',
                            component=FormComponent(type='text'),
                        ),
                        # TODO
                        # config: page, sort, query?
                        # TODO
                        # FormField(
                        #     id='access_token',
                        #     name='Personal Access Token',
                        #     description='GitHub Personal Access Token with appropriate permissions.',
                        #     component=FormComponent(type='text'),
                        # ),
                        # FormField(
                        #     id='owner',
                        #     name='Owner',
                        #     description='Owner of the repository. Can be a user or organization.',
                        #     component=FormComponent(type='text'),
                        # ),
                        # FormField(
                        #     id='repo',
                        #     name='Repo',
                        #     description='Name of the repository.',
                        #     component=FormComponent(type='text'),
                        # ),
                    ],
                ),
            ]),
        ),
        metadata=MetaData(
            name='List Issues',
            desc='Lists GitHub issues',
            group=['GitHub'],
            tags=['github'],
            documentation=Documentation(
                inputs={
                    "payload": PortDoc(desc="This port takes payload object.")
                },
                outputs={
                    "payload": PortDoc(desc="Returns issues data.")
                },
            ),
        ),
    )
