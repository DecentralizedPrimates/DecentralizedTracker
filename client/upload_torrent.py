from client.create_torrent import CreateTorrent
from client.download_torrent import DownloadTorrent
import sys
import os
import libtorrent as lt

class UploadTorrent:

    def __init__(self, files_path, pieces_size):
        self._files_path = files_path
        self._pieces_size = pieces_size
    

    def start(self):
        torrent_path = CreateTorrent(self._files_path, self._pieces_size).create()
        return DownloadTorrent().add_file_torrent(torrent_path, self._files_path)
