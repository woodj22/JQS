import time
import json
from .filesystem import FileSystemInterface
import os


class LocalFileSystem(FileSystemInterface):
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
            file.close()
        return line

    def store_queue_position(self, queue_name, byte_position):
        key = self.queue_position_file_key
        with open(key, 'r+') as f:
            data = json.load(f)
            data[queue_name] = byte_position
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
            f.close()
        return True

    def read_queue_position(self, queue_name):
        key = self.queue_position_file_key
        with open(key, 'r+') as f:
            data = json.load(f)
            byte_position = data[queue_name]

        return byte_position

    @property
    def queue_position_file_key(self):
        return os.path.join(self.base_file_path, 'queue_positions.json')

    def queue_storage_key(self, queue_name):
        return os.path.join(self.base_file_path, queue_name + ".txt")

    @property
    def base_file_path(self):
        return self._base_file_path

    @base_file_path.setter
    def base_file_path(self, value):
        self._base_file_path = value
