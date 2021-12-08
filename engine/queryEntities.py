from pydantic import BaseModel


class TagMessageQuery(BaseModel):
    info_hash: str
    attribute: str
    value: str


class OpinionMessageQuery:

    def __init__(self, attribute, value):
        self.attribute = attribute
        self.value = value


class InfoQuery(BaseModel):
    info_hash: str


class UploadTorrentQuery(BaseModel):
    title: str
    path: str
