import datetime
import random
import sys
import time
from typing import Optional

import uvicorn as uvicorn
from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
import asyncio
from configs import AppConfig
from downloadTorrent import DownloadTorrent
from engine.uploadTorrent import UploadTorrent
from storages import TagStorage, OpinionStorage
from messageHandlers import DefaultMessageHandler
from messageProcessors import DefaultMessageProcessor
from messageSenders import DefaultMessageSender, MessageSender
from mocks.mockStorages import MockTagStorage, MockOpinionStorage
from kademlia.network import Server
from messages import TagMessage, OpinionMessage
from queryEntities import TagMessageQuery, OpinionMessageQuery, InfoQuery, UploadTorrentQuery
from responceEntities import ShortInfo, TagInfo, TorrentInfo
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
global message_processor
global message_sender
global tag_storage
global opinion_storage
global download_torrent


@app.on_event('startup')
async def init_message_sender():
    global message_processor
    global message_sender
    global tag_storage
    global opinion_storage
    global download_torrent
    tag_storage = MockTagStorage()
    opinion_storage = MockOpinionStorage()
    download_torrent = DownloadTorrent()
    download_torrent.cc = "ss"
    message_processor, message_sender = await generate_message_helpers(config)


@app.get("/", tags=["MainDefaultScreen"])
async def main_default_screen(request: Request, attribute: Optional[str] = None, value: Optional[str] = None):
    if attribute is not None and value is not None:
        query = OpinionMessageQuery(attribute, value)
        info_hashes: list = [item.id for item in opinion_storage.get_top_n(query)]
        titles = [opinion_storage.get_title(info_hash) for info_hash in info_hashes]
        infos = [ShortInfo(info_hash, title) for info_hash, title in zip(info_hashes, titles)]
    else:
        infos = []
    return templates.TemplateResponse('index.html', context={'request': request, 'files': infos})


@app.get("/file_about", tags=["MainDefaultScreen"])
async def file_about(request: Request, info_hash: str):
    title = opinion_storage.get_title(info_hash)
    attributes = opinion_storage.get_top_n_attributes(info_hash)
    tags = [TagInfo(attribute[0], attribute[1]) for attribute in attributes]
    return templates.TemplateResponse('file_about.html', context={
        'request': request, 'title': title, 'tags': tags, 'info_hash': info_hash})


@app.get("/settings", tags=["Settings"])
async def settings():
    return {""}


@app.get("/upload", tags=["Upload"])
async def upload(request: Request):
    return templates.TemplateResponse('upload.html', context={'request': request})


@app.post("/uploadFiles", tags=["UploadFile"])
async def upload_torrent(upload_torrent_query: UploadTorrentQuery):
    global download_torrent
    handle = UploadTorrent(upload_torrent_query.path, 4 * 1024 * 1024, download_torrent).start()
    handle.set_upload_limit(config.upload_rate_limit)
    info_hash = str(handle.get_info_hash()).upper()
    message = TagMessage(info_hash, 'title', upload_torrent_query.title,
                         datetime.datetime.now(), random.randint(0, 1 << 32))
    message_processor.process_tag_message(message)
    return {""}


@app.get("/add_tag", tags=["AddTag"])
async def add_tag(request: Request, info_hash: str):
    title = opinion_storage.get_title(info_hash)
    return templates.TemplateResponse('add_tag.html', context={
        'request': request, 'title': title, 'info_hash': info_hash})


@app.post("/add_categorie", tags=["AddCategorie"])
async def add_categorie(query: TagMessageQuery):
    message = TagMessage(query.info_hash, query.attribute, query.value,
                         datetime.datetime.now(), random.randint(0, 1 << 32))
    message_processor.process_tag_message(message)
    return {""}


@app.get("/downloads", tags=["Downloads"])
async def downloads(request: Request):
    global download_torrent
    torrents = download_torrent.get_torrents_info()
    infos = []
    for torrent in torrents:
        info = TorrentInfo(torrent['title'],
                           torrent['info_hash'],
                           torrent['size'] // (1024 * 1024),
                           int(torrent['progress'] * 100))
        title = opinion_storage.get_title(info.info_hash)
        if len(title) > 0:
            info.title = title
        infos.append(info)
    return templates.TemplateResponse('downloads.html', context={'request': request, 'files': infos})


@app.post("/download", tags=["Download"])
async def download(info_query: InfoQuery):
    global download_torrent
    handle = download_torrent.add_torrent(info_query.info_hash, config.download_path)
    handle.set_upload_limit(config.upload_rate_limit)
    return {""}


async def generate_message_helpers(config: AppConfig):
    server = Server()

    sender = DefaultMessageSender(server)
    processor = DefaultMessageProcessor(tag_storage, opinion_storage, sender)
    message_handler = DefaultMessageHandler(processor)
    await server.listen(config.dht_port, message_handler, config.ip)
    await server.bootstrap(config.bootstrap_nodes)
    return processor, sender


if __name__ == "__main__":
    uvicorn.run("app:app", host=config.ip, port=config.flask_port, reload="True", log_level="info")