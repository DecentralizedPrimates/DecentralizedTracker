from abc import ABC, abstractmethod
from messages import TagMessage, OpinionMessage
from dbConnector import DBConnector

class TagStorage(ABC):

    def __init__(self):
        DBConnector().execute("""
            CREATE TABLE IF NOT EXISTS Tags (
                info_hash TEXT PRIMARY KEY,
                attribute TEXT,
                value TEXT,
                time INT,
                salt TEXT
            );
        """)

    @abstractmethod
    def contains_tag(self, tag: TagMessage) -> bool:
        result = DBConnector().fetchone(
            "SELECT * FROM Tags WHERE info_hash = ?;",
            tag.info_hash
        )
        if result:
            return True
        
        return False

    @abstractmethod
    def put_tag(self, tag: TagMessage):
        DBConnector().execute("""
            INSERT INTO Tags VALUES (?, ?, ?, ?);
        """, (tag.info_hash, tag.attribute, tag.value, tag.time, tag.salt)
        )


    def delete_tag(self, tag: TagMessage):
        DBConnector().execute("""
            DELETE FROM Tags WHERE info_hash=?;
        """, tag.info_hash
        )


    




class OpinionStorage(ABC):

    def __init__(self):
        DBConnector().execute("""
            CREATE TABLE IF NOT EXISTS Opinions (
                hash TEXT PRIMARY KEY,
                value INT
            );
        """)
    
    @abstractmethod
    def increment_opinion(self, tag: TagMessage):
        pass

