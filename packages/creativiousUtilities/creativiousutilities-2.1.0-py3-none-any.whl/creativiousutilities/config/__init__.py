import yaml
from yaml import load, dump
import os

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader,Dumper

class YAMLConfig:
    def __init__(self, default_config_filepath: str, config_filepath: str):
        self.config_filepath = config_filepath
        self.default_config_filepath = default_config_filepath
        self.default_config = self.__load(self.default_config_filepath)
        if not os.path.exists(self.config_filepath):
            self.__clone_default_config()

    def load(self):
        return self.__load(self.config_filepath)

    @classmethod
    def __load(cls, filepath):
        with open(filepath, "r") as f:
            data = yaml.load(f, Loader=Loader)
        return data

    def __clone_default_config(self):
        with open(self.default_config_filepath, "r") as f:
            string = f.read()
        with open(self.config_filepath, "w+") as f:
            f.write(string)

    @classmethod
    def __save(cls, filepath, data):
        with open(filepath, "w+") as f:
            yaml.dump(data, f, Dumper=Dumper)