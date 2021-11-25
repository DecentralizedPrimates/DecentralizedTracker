import sys
import os
import libtorrent as lt

class UploadTorrent:
    
    _files_path = None
    _torrent_save_path = 'storage/tmp/uploads'
    _pieces_size = 4 * 1024 * 1024

    def __init__(self, files_path, pieces_size)
        self._files_path = files_path # os.path.abspath(sys.argv[1])
        if pieces_size:
            self._pieces_size = pieces_size


    def start(self):

        fs = lt.file_storage()

        parent_folder = os.path.split(self._files_path)[0]

        # For single file
        if os.path.isfile(self._files_path):
            size = os.path.getsize(self._files_path)
            fs.add_file(self._files_path, size)

        # For folder
        for root, dirs, files in os.walk(self._files_path):

            for f in files:
                fname = os.path.join(root[len(parent_folder) + 1:], f)
                size = os.path.getsize(os.path.join(parent_folder, fname))
                fs.add_file(fname, size)

        if fs.num_files() == 0:
            throw new Exception('no files added')

        t = lt.create_torrent(fs, 0, self._pieces_size)

        t.set_creator('DecentralizedTracker')

        lt.set_piece_hashes(t, parent_folder, lambda x: sys.stdout.write('.'))

        f = open(self._torrent_save_path + '/test.torrent', 'wb+')
        f.write(libtorrent.bencode(t.generate()))
        f.close()
