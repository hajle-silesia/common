import json

import os


class Storage:
    def __init__(self):
        self.path = ""

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, path):
        self.__path = path

    def dump_data(self, data):
        if self.path:
            with open(self.path, "w", encoding="utf-8") as data_json:
                json.dump(data, data_json)

    def load_data(self):
        if os.path.exists(self.path):
            with open(self.path, encoding="utf-8") as data_json:
                return json.load(data_json)
