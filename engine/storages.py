from abc import ABC, abstractmethod
from messages import TagMessage, OpinionMessage
from dbConnector import DBConnector

class TagStorage(ABC):

    def __init__(self):
        DBConnector().execute("""
            CREATE TABLE IF NOT EXISTS Tags (
                info_hash TEXT PRIMARY KEY,
                attribute TEXT,
                time TIMESTAMP,
                salt TEXT
            );
        """)

    @abstractmethod
    def contains_tag(self, tag: TagMessage) -> bool:
        pass

    @abstractmethod
    def put_tag(self, tag: TagMessage):
        pass


class OpinionStorage(ABC):

    @abstractmethod
    def increment_opinion(self, tag: TagMessage):
        pass


if __name__ == '__main__':
    db_connection = sqlite3.connect('storage/db.sqlite3')
    cursor = db_connection.cursor()