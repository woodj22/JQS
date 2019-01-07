import json
from .filesystem import FileSystemInterface
import os
from .message import make_message


class LocalFileSystem(FileSystemInterface):

    def __init__(self, base_file_path):
        self._base_file_path = base_file_path
        self._queue_position_file_key = os.path.join(self.base_file_path, 'queue_positions.json')

    def store_message(self, queue_name, content_body):
        key = self.queue_storage_key(queue_name)

        with open(key, 'a+') as file:
            byte_position = file.tell()
            content = make_message(json.dumps(content_body))
            json.dump(content, file)
            file.write("\n")
            file.close()

        return queue_name, byte_position

    def read_message(self, queue_name, byte_position):
        key = self.queue_storage_key(queue_name)
        with open(key, 'r+') as file:
            file.seek(byte_position)
            line = file.readline()

            if line is '':
                return '', byte_position

            next_byte_position = file.tell()

            file.close()
        return line, next_byte_position

    def store_queue_position(self, queue_name, byte_position):
        key = self.queue_position_file_key

        with open(key, 'r+') as f:
            data = json.load(f)
            data[queue_name] = byte_position
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
            f.close()

        return byte_position

    def read_queue_position(self, queue_name):
        key = self.queue_position_file_key

        with open(key, 'r') as f:
            data = json.load(f)

            if queue_name not in data:
                return False

            byte_position = data[queue_name]

        return byte_position

    def clear_queue_store(self, queue_name):
        queue_file_key = self.queue_storage_key(queue_name)
        open(queue_file_key, 'w').close()

    @property
    def queue_position_file_key(self):
        return self._queue_position_file_key

    @queue_position_file_key.setter
    def queue_position_file_key(self, value):
        self._queue_position_file_key = value

    def queue_storage_key(self, queue_name):
        return os.path.join(self.base_file_path, queue_name + ".txt")

    @property
    def base_file_path(self):
        return self._base_file_path

    @base_file_path.setter
    def base_file_path(self, value):
        self._base_file_path = value
