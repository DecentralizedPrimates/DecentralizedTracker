from flask import Flask, request

from mocks.download_torrent_handler_mock import DownloadTorrentHandlerMock


app = Flask(__name__)

download_torrent_handler = DownloadTorrentHandlerMock()


@app.route('/download_torrent', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        try:
            # using query params
            response = download_torrent_handler.get_params(**request.args)
        except Exception:
            return None

        return response

    if request.method == 'POST':
        try:
            # using request body data
            response = download_torrent_handler.get_params(**request.json)
        except Exception:
            return None

        return response


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5300, debug=True)
