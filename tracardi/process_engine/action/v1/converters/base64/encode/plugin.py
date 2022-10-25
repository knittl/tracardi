from base64 import b64encode

from tracardi.service.plugin.domain.register import Documentation, Form, FormComponent, FormField, FormGroup, \
    MetaData, Plugin, PortDoc, Spec
from tracardi.service.plugin.domain.result import Result
from tracardi.service.plugin.runner import ActionRunner
from .model.models import Configuration


def validate(config: dict):
    return Configuration(**config)


class Base64EncodeAction(ActionRunner):
    config: Configuration

    async def set_up(self, init):
        self.config = validate(init)

    async def run(self, payload: dict, in_edge=None):
        dot = self._get_dot_accessor(payload)
        result = b64encode(dot[self.config.to_base64].encode(self.config.input_encoding))

        return Result(port="payload", value={"base64": result})


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module=__name__,
            className=Base64EncodeAction.__name__,
            inputs=['payload'],
            outputs=['payload'],
            version='0.1',
            license='MIT',
            author='knittl',
            init={
                'to_base64': 'payload@data',
                'input_encoding': 'utf-8',
            },
            form=Form(groups=[
                FormGroup(
                    fields=[
                        FormField(
                            id='to_base64',
                            name='String to encode as base64',
                            description='Type path to string or string itself. Default source is payload.',
                            component=FormComponent(type='dotPath', props={'defaultSourceValue': 'payload'}),
                        ),
                        FormField(
                            id='input_encoding',
                            name='Encoding',
                            description='Input text encoding. Will be used to convert input text to bytes before '
                                        'base64-encoding it. Set to "utf-8" if unsure.',
                            component=FormComponent(type='text', props={'label': 'encoding'}),
                        ),
                    ],
                ),
            ]),
        ),
        metadata=MetaData(
            name='To Base64',
            desc='Encodes input text as base64',
            group=['Converters'],
            tags=['base64'],
            documentation=Documentation(
                inputs={
                    "payload": PortDoc(desc="This port takes payload object.")
                },
                outputs={
                    "payload": PortDoc(desc="Returns base64-encoded data.")
                },
            ),
        ),
    )
