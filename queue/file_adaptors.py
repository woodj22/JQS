import time
import json
from .filesystem import FileInterface
import os


class LocalFileSystem(FileInterface):
    def __init__(self, base_file_path):
        self._base_file_path = base_file_path

    def save(self, queue_name, content):
        key = os.path.join(self.base_file_path, queue_name, str(int(time.time())) + ".json")
        with open(key, 'w+') as file:
            json.dump(content, file)

        return key

    @property
    def base_file_path(self):
        return self._base_file_path

    @base_file_path.setter
    def base_file_path(self, value):
        self._base_file_path = value
