import argparse
import logging
import asyncio

from kademlia.network import Server
from engine.messageHandlers import DefaultMessageHandler
from engine.messageProcessors import DefaultMessageProcessor
from engine.messageSenders import DefaultMessageSender

from engine.messages import TagMessage, OpinionMessage
from mocks.mockStorages import MockTagStorage, MockOpinionStorage

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.addHandler(handler)
log.setLevel(logging.DEBUG)

tag1 = TagMessage('1', 'genre', 'comedy', 100.0, '0')
tag_storage = MockTagStorage()


def connect_to_bootstrap_node():
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    server = Server()
    opinion_storage = MockOpinionStorage()
    messageSender = DefaultMessageSender(server)
    messageHandler = DefaultMessageHandler(DefaultMessageProcessor(tag_storage, opinion_storage, messageSender))
    loop.run_until_complete(server.listen(8471, messageHandler))
    bootstrap_node = ("localhost", 8470)
    loop.run_until_complete(server.bootstrap([bootstrap_node]))
    result = loop.run_until_complete(messageSender.send_message(tag1))
    print(result)
    try:
        loop.run_forever()

    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
        loop.close()


def main():
    connect_to_bootstrap_node()

if __name__ == "__main__":
    main()
