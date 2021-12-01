import configparser


class AppConfig:

    def __init__(self, config_file):
        configs = configparser.ConfigParser()
        configs.read(config_file)
        self.ip = configs['DEFAULT']['IP']
        self.flask_port = configs['DEFAULT']['FlaskPort']
        self.dht_port = configs['DEFAULT']['DhtPort']
