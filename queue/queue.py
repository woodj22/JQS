import json
from .filesystem import FileInterface


class Queue:
    def __init__(self, file_adaptor: FileInterface):
        self._file_adaptor = file_adaptor

    def append_message_to_queue(self, queue_name, message):
        queue_name, byte_position = self.file_adaptor.store(queue_name, message)
        self.write_queue_byte_position_to_file(queue_name, byte_position)

        return byte_position

    def read_top_message_from_queue(self, queue_name):
        byte_position = self.read_queue_byte_position_from_file(queue_name)

        return self.file_adaptor.read(queue_name, byte_position)

    @staticmethod
    def write_queue_byte_position_to_file(queue_name, byte_position):
        key = 'storage/queue_positions.json'
        with open(key, 'r+') as f:
            data = json.load(f)
            data[queue_name] = byte_position
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
            f.close()
        return True

    @staticmethod
    def read_queue_byte_position_from_file(queue_name):
        key = 'storage/queue_positions.json'
        with open(key, 'r+') as f:
            data = json.load(f)
            byte_position = data[queue_name]

        return byte_position

    @property
    def file_adaptor(self):
        return self._file_adaptor

    @file_adaptor.setter
    def file_adaptor(self, value):
        self._file_adaptor = value
