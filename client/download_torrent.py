import libtorrent as lt
from threading import Lock, Thread
import time
import sys


class DownloadTorrentMeta(type):
    _instances = {}
    _lock: Lock = Lock()


    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class DownloadTorrent(metaclass=DownloadTorrentMeta):
    _instance = None
    _session = None


    def __init__(self):
        if not self._session:
            self._session = lt.session({'listen_interfaces': '0.0.0.0:6881'})
    

    def add_torrent(self, info_hash, save_path):
        torrent_handle = self._session.add_torrent({
            'info_hash': bytes.fromhex(info_hash),
            'save_path': save_path
        })


    def find_torrent(self, info_hash):
        torrent_handle = self._session.find_torrent(lt.sha1_hash(bytes.fromhex(info_hash)))
        if not torrent_handle.is_valid():
            raise Exception('Torrent not found')
        
        return TorrentHandle(torrent_handle)


class TorrentHandle:
    _torrent_handle = None


    def __init__(self, torrent_handle):
        self._torrent_handle = torrent_handle


    def get_status(self):
        stats = self._torrent_handle.status()
        return {
            'name' : stats.name,
            'is_seeding' : stats.is_seeding,
            'progress' : stats.progress,
            'download_rate' : stats.download_rate,
            'upload_rate' : stats.upload_rate,
            'num_peers' : stats.num_peers,
            'state' : stats.state
        }
    

    def pause(self):
        self._torrent_handle.pause()
    

    def resume(self):
        self._torrent_handle.resume()
        

if __name__ == '__main__':
    print(sys.argv[1])
    DownloadTorrent().add_torrent(sys.argv[1].strip(), '.')
    
    my_torrent = DownloadTorrent().find_torrent(sys.argv[1].strip())
    status = my_torrent.get_status()
    
    i = 0
    while not status['is_seeding']:
        if i == 10:
            my_torrent.pause()
        elif i == 20:
            my_torrent.resume()
        
        status = my_torrent.get_status()

        print('\r%.2f%% complete (down: %.1f kB/s up: %.1f kB/s peers: %d) %s' % (
            status['progress'] * 100,
            status['download_rate'] / 1000,
            status['upload_rate'] / 1000,
            status['num_peers'],
            status['state']), end=' '
        )

        time.sleep(1)

        i += 1