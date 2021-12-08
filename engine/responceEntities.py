class ShortInfo:

    def __init__(self, info_hash, title):
        self.info_hash = info_hash
        self.title = title


class TagInfo:

    def __init__(self, attribute, value):
        self.attribute = attribute
        self.value = value


class TorrentInfo:

    def __init__(self, title, info_hash, size, progress):
        self.title = title
        self.info_hash = info_hash
        self.size = size
        self.progress = progress

