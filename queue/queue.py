import json
from .filesystem import FileSystemInterface


class Queue:
    def __init__(self, file_adaptor: FileSystemInterface):
        self._file_adaptor = file_adaptor

    def append_message_to_queue(self, queue_name, message):
        queue_name, byte_position = self.file_adaptor.store(queue_name, message)

        return byte_position

    def read_top_message_from_queue(self, queue_name):
        current_byte_position = self.file_adaptor.read_queue_position(queue_name)

        message, next_byte_position = self.file_adaptor.read(queue_name, current_byte_position)

        self.file_adaptor.store_queue_position(queue_name, next_byte_position)

        return message

    def clear_queue(self, queue_name):
        self.file_adaptor.clear_queue_store(queue_name)
        self.file_adaptor.store_queue_position(queue_name, 0)

        return True

    @property
    def file_adaptor(self):
        return self._file_adaptor

    @file_adaptor.setter
    def file_adaptor(self, value):
        self._file_adaptor = value

