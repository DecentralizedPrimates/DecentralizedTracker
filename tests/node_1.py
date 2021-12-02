import argparse
import logging
import asyncio

# from handler_example import TestMessageHandler
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


def create_bootstrap_node():
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    server = Server()
    opinion_storage = MockOpinionStorage()
    messageSender = DefaultMessageSender(server)
    messageHandler = DefaultMessageHandler(DefaultMessageProcessor(tag_storage, opinion_storage, messageSender))
    loop.run_until_complete(server.listen(8470, messageHandler))
    # print(tag_storage.contains_tag(tag1))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
        loop.close()


def main():
    create_bootstrap_node()

if __name__ == "__main__":
    main()
