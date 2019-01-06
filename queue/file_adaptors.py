import time
import json
from .filesystem import FileInterface
import os


class LocalFileSystem(FileInterface):
    def __init__(self, base_file_path):
        self._base_file_path = base_file_path

    def store(self, queue_name, content):
        key = self.queue_storage_key(queue_name)

        with open(key, 'a+') as file:
            byte_position = file.tell()
            json.dump(content, file)
            file.write("\n")
            file.write("\n")
            file.close()

        return queue_name, byte_position

    def read(self, queue_name, byte_position):
        key = self.queue_storage_key(queue_name)
        with open(key, 'r+') as file:
            file.seek(byte_position)
            line = file.readline()
            # exit(line)
            file.close()
        return line

    def queue_storage_key(self, queue_name):
        return os.path.join(self.base_file_path, queue_name + ".txt")

    @property
    def base_file_path(self):
        return self._base_file_path

    @base_file_path.setter
    def base_file_path(self, value):
        self._base_file_path = value
