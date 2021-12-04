import datetime
import random
import sys

import uvicorn as uvicorn
from fastapi import FastAPI, Depends
import asyncio
from configs import AppConfig
from messageHandlers import DefaultMessageHandler
from messageProcessors import DefaultMessageProcessor
from messageSenders import DefaultMessageSender, MessageSender
from mocks.mockStorages import MockTagStorage, MockOpinionStorage
from kademlia.network import Server
from messages import TagMessage, OpinionMessage
from queryEntities import TagMessageQuery, OpinionMessageQuery

# For interacting with the network local client API should contain the following endpoints:
#
# MainDefaultScreen to display files by default on main screen. (GET)
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
            "name": "MainDefaultScreen",
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

config = AppConfig(sys.argv[1])
global message_sender


@app.on_event('startup')
async def init_message_sender():
    global message_sender
    message_sender = await generate_message_sender(config)


@app.get("/", tags=["MainDefaultScreen"])
async def main_default_screen():
    return {""}


@app.get("/file_search", tags=["FileSearch"])
async def file_search(query: OpinionMessageQuery):
    message = OpinionMessage(query.attribute, query.value)
    message_sender.send_message(message)
    return {""}


@app.get("/settings", tags=["Settings"])
async def settings():
    return {""}


@app.post("/upload", tags=["Upload"])
async def upload():
    return {""}


@app.post("/add_categorie", tags=["AddCategorie"])
async def add_categorie(query: TagMessageQuery):
    message = TagMessage(query.info_hash, query.attribute, query.value,
                         datetime.datetime.now(), random.randint(0, 1 << 32))
    asyncio.create_task(message_sender.send_message(message))
    return {""}


@app.get("/download", tags=["Download"])
async def download():
    return {""}


async def generate_message_sender(config: AppConfig):
    server = Server()
    tag_storage = MockTagStorage()
    opinion_storage = MockOpinionStorage()

    sender = DefaultMessageSender(server)
    message_handler = DefaultMessageHandler(DefaultMessageProcessor(tag_storage, opinion_storage, sender))
    print(config.ip, config.dht_port)
    await server.listen(config.dht_port, message_handler, config.ip)
    await server.bootstrap(config.bootstrap_nodes)
    return sender


if __name__ == "__main__":
    uvicorn.run("app:app", host=config.ip, port=config.flask_port, reload="True", log_level="info")