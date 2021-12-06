import sys
import os
import libtorrent as lt
import string
import random

class CreateTorrent:
    
    _files_path = None
    _torrent_save_path = 'storage/tmp/uploads'
    _pieces_size = 4 * 1024 * 1024

    def __init__(self, files_path, pieces_size):
        self._files_path = files_path
        if pieces_size:
            self._pieces_size = pieces_size

    
    def __generate_id(self, size=6, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    
    
    def create(self):

        fs = lt.file_storage()


        # For single file
        parent_folder = os.path.split(self._files_path)[0]
        
        if os.path.isfile(self._files_path):
            size = os.path.getsize(self._files_path)
            fs.add_file(self._files_path, size)

        # For folder

        for root, dirs, files in os.walk(os.path.abspath(self._files_path)):

            for f in files:
                parent_folder = os.path.split(os.path.abspath(self._files_path))[0]
                fname = os.path.join(root[len(parent_folder) + 1:], f)
                size = os.path.getsize(os.path.join(parent_folder, fname))
                fs.add_file(fname, size)

        if fs.num_files() == 0:
            raise Exception('No files added')

        t = lt.create_torrent(fs, 0, self._pieces_size)

        t.set_creator('DecentralizedTracker')

        lt.set_piece_hashes(t, parent_folder, lambda x: sys.stdout.write('.'))

        torrent_path = self._torrent_save_path + '/' + self.__generate_id() + '.torrent'
        f = open(torrent_path, 'wb+')
        f.write(lt.bencode(t.generate()))
        f.close()
        return torrent_path
