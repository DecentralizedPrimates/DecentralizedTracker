from pydantic import BaseModel


class TagMessageQuery(BaseModel):
    info_hash: str
    attribute: str
    value: str


class OpinionMessageQuery(BaseModel):
    attribute: str
    value: str

