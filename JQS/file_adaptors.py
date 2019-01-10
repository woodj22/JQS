import json
from .filesystem import StorageInterface
import os


class LocalFileSystem(StorageInterface):


    def __init__(self, base_file_path):
        self._base_file_path = base_file_path

        self._queue_position_file_key = os.path.join(self.base_file_path, 'queue_positions.json')

    def store_message(self, queue_name, content):
        key = self.queue_storage_key(queue_name)
        os.makedirs(os.path.dirname(key), exist_ok=True)

        with open(key, 'a+') as file:
            byte_position = file.tell()

            json.dump(content, file)

            file.write("\n")

            file.close()

        return byte_position, content

    def read_message(self, queue_name, byte_position):
        key = self.queue_storage_key(queue_name)
        with open(key, 'r+') as file:
            file.seek(byte_position)
            line = file.readline()

            if line is '':
                return byte_position, json.dumps('')

            next_byte_position = file.tell()

            file.close()
        return next_byte_position, line

    def delete_message(self, queue_name, message_position):
        key = self.queue_storage_key(queue_name)
        with open(key, 'r+b') as file:
            file.seek(message_position)
            file.readline()
            next_message_position = file.tell()

            file.seek(message_position)

            bytes_to_change = next_message_position - message_position - 1

            write_string = (' ' * bytes_to_change) + "\n"

            file.write(write_string.encode('utf8'))

        return True

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
            f.close()
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
