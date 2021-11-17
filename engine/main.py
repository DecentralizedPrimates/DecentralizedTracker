from messageHandlers import DefaultMessageHandler
from messageProcessors import DefaultMessageProcessor
from messageSenders import DefaultMessageSender
from mocks.mockStorages import MockTagStorage, MockOpinionStorage

from flask import Flask
from kademlia.network import Server


app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


tag_storage = MockTagStorage()
opinion_storage = MockOpinionStorage()

server = Server()
messageSender = DefaultMessageSender(server)
messageHandler = DefaultMessageHandler(DefaultMessageProcessor(tag_storage, opinion_storage, messageSender))
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5300)

