import base64
import json

import requests


class Notifier:
    def __init__(self, storage):
        self.__storage = storage

        if self.__storage.load_data():
            self.__observers = self.__storage.load_data()
        else:
            self.__observers = {}
        self.__responses = []

    @property
    def observers(self):
        return self.__observers

    @property
    def responses(self):
        return self.__responses

    def register_observer(self, observer):
        self.observers.update(observer)
        self.__storage.dump_data(self.observers)

    def remove_observer(self, observer):
        for k in observer:
            self.observers.pop(k, None)
        self.__storage.dump_data(self.observers)

    def notify_observers(self, data):
        self.responses.clear()

        for url in self.observers.values():
            self.responses.append(self._notify_observer(url, data))

    def _notify_observer(self, url, data):
        try:
            return requests.post(url, base64.b64encode(json.dumps(data, default=str).encode()))
        except BaseException as err:
            print(f"Timeout for observer with URL: {url}")
            print(f"EXCEPTION: {err=}, {type(err)}")
