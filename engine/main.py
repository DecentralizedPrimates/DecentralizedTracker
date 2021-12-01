from messageHandlers import DefaultMessageHandler
from messageProcessors import DefaultMessageProcessor
from messageSenders import DefaultMessageSender
from mocks.mockStorages import MockTagStorage, MockOpinionStorage

from quart import Quart, render_template, websocket
from waitress import serve
from kademlia.network import Server

from configs import AppConfig

app = Quart(__name__)


@app.route("/")
def hello():
    return '<p>Hello</p>'


async def get_message_sender(config: AppConfig):
    server = Server()
    tag_storage = MockTagStorage()
    opinion_storage = MockOpinionStorage()

    message_sender = DefaultMessageSender(server)
    message_handler = DefaultMessageHandler(DefaultMessageProcessor(tag_storage, opinion_storage, message_sender))
    await server.listen(config.dht_port, message_handler, config.ip)
    return message_sender


if __name__ == "__main__":
    config = AppConfig('../configs/app.ini')
    message_sender = get_message_sender(config)
    app.run(host=config.ip, port=config.flask_port)
