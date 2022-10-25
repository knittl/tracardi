from base64 import b64decode

from tracardi.service.plugin.domain.register import Form, FormGroup, FormField, FormComponent, \
    Documentation, PortDoc
from tracardi.service.plugin.domain.register import Plugin, Spec, MetaData
from tracardi.service.plugin.domain.result import Result
from tracardi.service.plugin.runner import ActionRunner
from .model.models import Configuration


def validate(config: dict):
    return Configuration(**config)


class Base64DecodeAction(ActionRunner):
    config: Configuration

    async def set_up(self, init):
        self.config = validate(init)

    async def run(self, payload: dict, in_edge=None):
        dot = self._get_dot_accessor(payload)
        result = b64decode(dot[self.config.from_base64]).decode(self.config.output_encoding)

        return Result(port="payload", value={"text": result})


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module=__name__,
            className=Base64DecodeAction.__name__,
            inputs=['payload'],
            outputs=['payload'],
            version='0.1',
            license='MIT',
            author='knittl',
            init={
                'from_base64': 'payload@base64',
                'output_encoding': 'utf-8'
            },
            form=Form(groups=[
                FormGroup(
                    fields=[
                        FormField(
                            id='from_base64',
                            name='Base64-encoded data to decode to string',
                            description='Type path to string or string itself. Default source is payload.',
                            component=FormComponent(type='dotPath', props={'defaultSourceValue': 'payload'})
                        ),
                        FormField(
                            id='output_encoding',
                            name='Encoding',
                            description='Output text encoding. Will be used to convert output bytes to text to bytes '
                                        'after base64-decoding it. Set to "utf-8" if unsure.',
                            component=FormComponent(type='text', props={'label': 'encoding'})
                        )
                    ]
                ),
            ]),
        ),
        metadata=MetaData(
            name='From Base64',
            desc='Decodes base64 input to plain text',
            group=['Converters'],
            tags=['base64'],
            documentation=Documentation(
                inputs={
                    "payload": PortDoc(desc="This port takes payload object with base64 encoded data.")
                },
                outputs={
                    "payload": PortDoc(desc="Returns the plain text decoded from base64-encoded input.")
                }
            ),
        )
    )
