import datetime
import random
import sys
from typing import Optional

import uvicorn as uvicorn
from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
import asyncio
from configs import AppConfig
from storages import TagStorage, OpinionStorage
from messageHandlers import DefaultMessageHandler
from messageProcessors import DefaultMessageProcessor
from messageSenders import DefaultMessageSender, MessageSender
from mocks.mockStorages import MockTagStorage, MockOpinionStorage
from kademlia.network import Server
from messages import TagMessage, OpinionMessage
from queryEntities import TagMessageQuery, OpinionMessageQuery, InfoQuery
from responceEntities import ShortInfo, TagInfo
from fastapi.staticfiles import StaticFiles

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

app.mount(
    "/static",
    StaticFiles(directory="../static"),
    name="static",
)

config = AppConfig(sys.argv[1])
templates = Jinja2Templates(directory="../static/templates/")
global message_sender
global tag_storage
global opinion_storage

@app.on_event('startup')
async def init_message_sender():
    global message_sender
    global tag_storage
    global opinion_storage
    tag_storage = MockTagStorage()
    opinion_storage = MockOpinionStorage()
    message_sender = await generate_message_sender(config)


@app.get("/", tags=["MainDefaultScreen"])
async def main_default_screen(request: Request, attribute: str, value: str):
    info_hash = 'abcde'
    tag = TagMessage(info_hash, attribute, value, datetime.datetime.now(), 1)
    opinion_storage.increment_opinion(tag)
    tag = TagMessage(info_hash, 'actor', 'Kyrylo Volkov', datetime.datetime.now(), 1)
    opinion_storage.increment_opinion(tag)
    tag = TagMessage(info_hash, 'year', '1999', datetime.datetime.now(), 1)
    opinion_storage.increment_opinion(tag)
    tag = TagMessage(info_hash, 'genre', 'fantastic', datetime.datetime.now(), 1)
    opinion_storage.increment_opinion(tag)
    query = OpinionMessageQuery(attribute, value)
    info_hashes: list = [item.id for item in opinion_storage.get_top_n(query)]
    titles = [opinion_storage.get_title(info_hash) for info_hash in info_hashes]
    infos = [ShortInfo(info_hash, title) for info_hash, title in zip(info_hashes, titles)]
    return templates.TemplateResponse('index.html', context={'request': request, 'files': infos})


@app.get("/file_about", tags=["MainDefaultScreen"])
async def file_about(request: Request, info_hash: str):
    title = opinion_storage.get_title(info_hash)
    attributes = opinion_storage.get_top_n_attributes(info_hash)
    tags = [TagInfo(attribute[0], attribute[1]) for attribute in attributes]
    return templates.TemplateResponse('file_about.html', context={
        'request': request, 'title': title, 'tags': tags, 'info_hash': info_hash})

# @app.get("/file_search", tags=["FileSearch"])
# async def file_search(query: OpinionMessageQuery):
#     message = OpinionMessage(query.attribute, query.value)
#     message_sender.send_message(message)
#     return {""}


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


@app.post("/download", tags=["Download"])
async def download():
    return {""}


async def generate_message_sender(config: AppConfig):
    server = Server()

    sender = DefaultMessageSender(server)
    message_handler = DefaultMessageHandler(DefaultMessageProcessor(tag_storage, opinion_storage, sender))
    print(config.ip, config.dht_port)
    await server.listen(config.dht_port, message_handler, config.ip)
    await server.bootstrap(config.bootstrap_nodes)
    return sender


if __name__ == "__main__":
    uvicorn.run("app:app", host=config.ip, port=config.flask_port, reload="True", log_level="info")