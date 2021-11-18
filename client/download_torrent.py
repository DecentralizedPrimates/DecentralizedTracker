from client.singleton_meta_class import SingletonMetaClass
from client.torrent_handle import TorrentHandle
import libtorrent as lt
import re


class DownloadTorrent(metaclass=SingletonMetaClass):
    _instance = None
    _session = None

    
    def __init__(self):
        if not self._session:
            self._session = lt.session({'listen_interfaces': '0.0.0.0:6881'})
    
    
    def __get_torrent_handle(self, info_hash):
        return self._session.find_torrent(lt.sha1_hash(bytes.fromhex(info_hash)))
    

    def add_torrent(self, info_hash, save_path):
        if not re.match(r'^[a-f\d]{40}$', info_hash, re.IGNORECASE):
            raise Exception('Incorrect infohash')

        if self.__get_torrent_handle(info_hash).is_valid():
            raise Exception('Could not add duplicate torrent')
        
        torrent_handle = self._session.add_torrent({
            'info_hash': bytes.fromhex(info_hash),
            'save_path': save_path
        })


    def find_torrent(self, info_hash):
        torrent_handle = self.__get_torrent_handle(info_hash)
        if not torrent_handle.is_valid():
            raise Exception('Torrent not found')
        
        return TorrentHandle(torrent_handle)
    

    def remove_torrent(self, info_hash, with_downloaded_data = False):
        torrent_handle = self.__get_torrent_handle(info_hash)
        if with_downloaded_data:
            self._session.remove_torrent(torrent_handle, self._session.delete_files)
        else:
            self._session.remove_torrent(torrent_handle)


    def get_torrents(self):
        return [TorrentHandle(torrent_handle) for torrent_handle in self._session.get_torrents()]
