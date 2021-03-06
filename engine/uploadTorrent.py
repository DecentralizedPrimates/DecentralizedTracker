from engine.createTorrent import CreateTorrent
from engine.downloadTorrent import DownloadTorrent


class UploadTorrent:

    def __init__(self, files_path, pieces_size, downloader: DownloadTorrent):
        self._files_path = files_path
        self._pieces_size = pieces_size
        self._downloader = downloader
    

    def start(self):
        torrent_path = CreateTorrent(self._files_path, self._pieces_size).create()
        return self._downloader.add_file_torrent(torrent_path, self._files_path)
