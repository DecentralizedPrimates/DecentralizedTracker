from engine.downloadTorrent import DownloadTorrent
import unittest
import time
import shutil
import os


class TestDownloadTorrent(unittest.TestCase):
    def setUp(self):
        self.first_info_hash = 'b26c81363ac1a236765385a702aec107a49581b5' # Ubuntu 20.04 ISO image
        self.first_save_path = 'tmp'
        self.second_info_hash = 'bc26c6bc83d0ca1a7bf9875df1ffc3fed81ff555' # Ubuntu 18.04 ISO image
        self.second_save_path = 'tmp2'


    def test_download_torrent(self):
        DownloadTorrent().add_torrent(self.first_info_hash, self.first_save_path)
    
        my_torrent = DownloadTorrent().find_torrent(self.first_info_hash)
        
        status = my_torrent.get_status()
        
        i = 0
        while not status['is_seeding']:
            if i == 10:
                my_torrent.pause()
            elif i == 20:
                my_torrent.resume()
                DownloadTorrent().add_torrent(self.second_info_hash, self.second_save_path)
            elif i == 30:
                my_torrent.set_download_limit(10 * 1024)
                my_torrent.set_upload_limit(15 * 1024)
            elif i == 40:
                my_torrent.remove_download_limit()
                my_torrent.remove_upload_limit()
            elif i == 50:
                if status['has_metadata']:
                    print('\nFirst torrent files list:\n')
                    print(my_torrent.get_files())

                DownloadTorrent().remove_torrent(self.second_info_hash, True)
                DownloadTorrent().remove_torrent(self.first_info_hash, True)
                time.sleep(5)
                return True

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
            
            time.sleep(1)

            i += 1
    
    
    def tearDown(self):
        if os.path.isdir(self.first_save_path):
            shutil.rmtree(self.first_save_path)
        
        if os.path.isdir(self.second_save_path):
            shutil.rmtree(self.second_save_path)


if __name__ == '__main__':
    unittest.main()
