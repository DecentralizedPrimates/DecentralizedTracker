class TorrentHandle:
    _torrent_handle = None


    def __init__(self, torrent_handle):
        self._torrent_handle = torrent_handle


    def get_status(self):
        stats = self._torrent_handle.status()
        return {
            'name' : stats.name,
            'is_seeding' : stats.is_seeding,
            'is_paused' : stats.paused,
            'progress' : stats.progress,
            'download_rate' : stats.download_rate,
            'upload_rate' : stats.upload_rate,
            'num_peers' : stats.num_peers,
            'state' : stats.state,
            'download_limit' : self._torrent_handle.download_limit(),
            'upload_limit' : self._torrent_handle.upload_limit(),
            'has_metadata' : stats.has_metadata
        }
    

    def get_files(self):
        if not self.get_status()['has_metadata']:
            raise Exception('Metadata have not been fetched')
        
        torrent_info = self._torrent_handle.status().torrent_file
        file_storage = torrent_info.files()
        files = []
        for i in range(file_storage.num_files()):
            files.append({
                'name': file_storage.file_name(i),
                'path': file_storage.file_path(i),
                'size': file_storage.file_size(i)
            })
        return files
    

    def get_info_hash(self):
        return self._torrent_handle.info_hash()
    

    def pause(self):
        self._torrent_handle.pause()
    

    def resume(self):
        self._torrent_handle.resume()


    def set_download_limit(self, new_limit):
        self._torrent_handle.set_download_limit(new_limit)
    

    def set_upload_limit(self, new_limit):
        self._torrent_handle.set_upload_limit(new_limit)
    

    def remove_download_limit(self):
        self.set_download_limit(-1)
    

    def remove_upload_limit(self):
        self.set_upload_limit(-1)

