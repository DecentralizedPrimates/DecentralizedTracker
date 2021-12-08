import configparser
import json


class AppConfig:

    def __init__(self, config_file):
        configs = configparser.ConfigParser()
        configs.read(config_file)
        self.ip = configs['DEFAULT']['IP']
        self.flask_port = int(configs['DEFAULT']['ServerPort'])
        self.dht_port = configs['DEFAULT']['DhtPort']
        bootstrap_nodes = json.loads(configs['DEFAULT']['Bootstrap'])
        self.bootstrap_nodes = []
        for full_address in bootstrap_nodes:
            ip, port = full_address.split(":")
            port = int(port)
            self.bootstrap_nodes.append((ip, port))
        self.download_path = configs['DEFAULT']['DownloadPath']
