import datetime
import random

import uvicorn as uvicorn
from fastapi import FastAPI, Depends
import asyncio
from configs import AppConfig
from messageHandlers import DefaultMessageHandler
from messageProcessors import DefaultMessageProcessor
from messageSenders import DefaultMessageSender, MessageSender
from mocks.mockStorages import MockTagStorage, MockOpinionStorage
from kademlia.network import Server
from messages import TagMessage

# For interacting with the network local client API should contain the following endpoints:
#
# MainDefaultSreen to display files by default on main screen. (GET)
# FileSearch to find a file by name and other parameters (GET)
# Settings (POST)
# Upload (POST)
# AddCategorie (POST)
# Download (GET)

app = FastAPI(
    title="DecetralizedTracker API",
    description="Local client API for interacting with the network.",
    version="0.1.0",
    openapi_tags=[
        {
            "name": "MainDefaultSreen",
            "description": "Display files by default on main screen.",
        },
        {
            "name": "FileSearch",
            "description": "Find a file by name and other parameters.",
        },
        {
            "name": "Settings",
            "description": "",
        },
        {
            "name": "Upload",
            "description": "",
        },
        {
            "name": "AddCategorie",
            "description": "",
        },
        {
            "name": "Download",
            "description": "",
        },
    ],
)


def get_message_sender():
    return message_sender


@app.get("/", tags=["MainDefaultSreen"])
async def main_default_screen():
    return {""}


@app.get("/file_search", tags=["FileSearch"])
async def file_search():
    return {""}


@app.get("/settings", tags=["Settings"])
async def settings():
    return {""}


@app.post("/upload", tags=["Upload"])
async def upload():
    return {""}


@app.post("/add_categorie", tags=["AddCategorie"])
async def add_categorie():
    return {""}


@app.get("/test")
async def test(sender: MessageSender = Depends(get_message_sender)):
    print('here')
    message = TagMessage("abcd", "title", "fast and furious", datetime.datetime.now(), random.randint(0, 100))
    sender.send_message(message)
    return {""}


@app.get("/download", tags=["Download"])
async def download():
    return {""}


# def connect_to_bootstrap_node(args):
#     loop = asyncio.get_event_loop()
#     loop.set_debug(True)
#
#     loop.run_until_complete(server.listen(8469))
#     bootstrap_node = (args.ip, int(args.port))
#     loop.run_until_complete(server.bootstrap([bootstrap_node]))
#
#     try:
#         loop.run_forever()
#     except KeyboardInterrupt:
#         pass
#     finally:
#         server.stop()
#         loop.close()
#
#
# def create_bootstrap_node():
#     loop = asyncio.get_event_loop()
#     loop.set_debug(True)
#
#     loop.run_until_complete(server.listen(8469, TestMessageHandler()))
#
#     try:
#         loop.run_forever()
#     except KeyboardInterrupt:
#         pass
#     finally:
#         server.stop()
#         loop.close()


def generate_message_sender(config: AppConfig):
    server = Server()
    tag_storage = MockTagStorage()
    opinion_storage = MockOpinionStorage()

    message_sender = DefaultMessageSender(server)
    message_handler = DefaultMessageHandler(DefaultMessageProcessor(tag_storage, opinion_storage, message_sender))
    asyncio.get_event_loop().run_until_complete(server.listen(config.dht_port, message_handler, config.ip))
    asyncio.get_event_loop().run_until_complete(server.bootstrap(config.bootstrap_nodes))
    return message_sender


if __name__ == "__main__":
    config = AppConfig('../configs/bootstrap.ini')
    message_sender = generate_message_sender(config)
    uvicorn.run("app:app", host=config.ip, port=config.flask_port, reload="True", log_level="info")
