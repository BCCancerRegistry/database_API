from configparser import ConfigParser
from os import getenv,environ
from configparser import NoSectionError
from urllib.parse import quote_plus

class AppConfig:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read(getenv("APPCONFIG", "config.ini"))

    def get_appconfig(self):
        return self.config

class DbConfig:
    def __init__(self, usertype):
        appconfig = AppConfig()
        config = appconfig.get_appconfig()
        if config.has_section(usertype):
            self.username = config[usertype].get("username")
            self.password = quote_plus(config[usertype].get("password"))
        else:
            print(config.sections())
            raise NoSectionError(usertype)
        self.hostname = config['DB_CONN'].get("hostname")
        self.dbname = config['DB_CONN'].get("dbname")


class Environ:
    def __init__(self):
        appconfig = AppConfig()
        config = appconfig.get_appconfig()
        self.env_config = {}
        if config.has_section("ENVIRON"):
            for i in config['ENVIRON'].keys():
                print("Setting env {i} to {j}".format(i=i.upper(), j=config['ENVIRON'].get(i)))
                self.env_config[i.upper()] = config['ENVIRON'].get(i)