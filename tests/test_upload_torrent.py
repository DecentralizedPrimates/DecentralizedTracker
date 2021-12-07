from engine.uploadTorrent import UploadTorrent
from engine.downloadTorrent import DownloadTorrent
import unittest
import time
import shutil
import os


class TestUploadTorrent(unittest.TestCase):
    
    _tmp_folder = 'tmp'

    def setUp(self):
        if os.path.isdir(self._tmp_folder):
            shutil.rmtree(self._tmp_folder)
        
        os.mkdir(self._tmp_folder)
        f = open(self._tmp_folder + "/file1.txt", "a")
        f.write("Test 1 Test 1")
        f.close()
        f = open(self._tmp_folder + "/file2.txt", "a")
        f.write("Test 2 Test 2")
        f.close()


    def test_upload_torrent(self):
        uploader = torrent = UploadTorrent(self._tmp_folder, 4 * 1024 * 1024)
        my_torrent = uploader.start()

        status = my_torrent.get_status()
        
        i = 0
        while i < 50:

            status = my_torrent.get_status()

            print('\n%.2f%% complete (down: %.1f kB/s up: %.1f kB/s peers: %d) %s, paused: %s, down_limit: %s, up_limit: %s, torrents: %d' % (
                status['progress'] * 100,
                status['download_rate'] / 1000,
                status['upload_rate'] / 1000,
                status['num_peers'],
                status['state'],
                status['is_paused'],
                status['download_limit'],
                status['upload_limit'],
                len(DownloadTorrent().get_torrents())), end=' '
            )
            print("\nInfo Hash:", my_torrent.get_info_hash())
            time.sleep(1)

            i += 1
        

    def tearDown(self):
        shutil.rmtree(self._tmp_folder)


if __name__ == '__main__':
    unittest.main()
