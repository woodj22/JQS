import json
from .filesystem import FileSystemInterface
import os


class LocalFileSystem(FileSystemInterface):

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
                return '', byte_position

            next_byte_position = file.tell()

            file.close()
        return next_byte_position, line

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
    #
    # # def store_in_flight_message
    # def mark_message_as_in_flight(self, queue_name, position):
    #     message = self.read_message(queue_name, position)
    #     # exit(os.path.join('in_flight', queue_name))
    #     content, byte_position = self.store_message(os.path.join('in_flight', queue_name), message)
    #
    #     return byte_position
