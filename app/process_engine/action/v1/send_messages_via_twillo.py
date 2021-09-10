from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.result import Result
from pydantic import BaseModel
from twilio.rest import Client


class TwilloAcount(BaseModel):
    account_SID: str
    account_TOKEN: str


class Message(BaseModel):
    to_whatsapp_number: str
    message: str


class Configuration(BaseModel):
    twillo_settings: TwilloAcount
    message: Message


class PostMan:
    def __init__(self, twillo: TwilloAcount):
        self.twillo = twillo

    def _connect(self) -> Client:
        client = Client(self.twillo.account_SID, self.twillo.account_TOKEN)
        return client

    def send(self, message: Message):
        client = self._connect()
        client.messages.create(body=message.message,from_='whatsapp:+14155238886', to=message.to_whatsapp_number)
        return True


class Twillo(ActionRunner):
    def __init__(self, **kwargs):
        self.status = ''
        try:
            self.config = Configuration(**kwargs)
            self.post = PostMan(self.config.twillo_settings)
        except Exception as exc:
            self.status += str(exc) + '\n'

    async def run(self, void):
        try:
            self.post.send(self.config.message)
        except Exception as exc:
            self.status += str(exc) + '\n'
        if not self.status == '':
            ActionRunner.console = self.status
            print(ActionRunner.console)
            return Result(port='session', value=False)
        return Result(port='session', value=True)


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='app.process_engine.action.v1.send_messages_via_twillo',
            className='Twillo',
            inputs=["void"],
            outputs=['session'],
            init={
                'twillo_settings': {
                    'account_SID': None,
                    'account_TOKEN': None,
                },
                'message': {
                    "to_whatsapp_number": None,
                    "message": None,
                }
            },
            version='0.1',
            license="MIT",
            author="iLLu"

        ),
        metadata=MetaData(
            name='Send message via twillo',
            desc='Send mail via defined twillo.',
            type='flowNode',
            width=200,
            height=100,
            icon='start',
            group=["Connectors"]
        )
    )
