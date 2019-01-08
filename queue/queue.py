from queue.message import make_message
from .filesystem import FileSystemInterface
import json
import os


class Queue:
    def __init__(self, file_adaptor: FileSystemInterface):
        self._file_adaptor = file_adaptor

    def append_message_to_queue(self, queue_name, content_body):
        message = make_message(json.dumps(content_body))

        byte_position, content = self.file_adaptor.store_message(queue_name, message)

        return byte_position, content

    def read_top_message_from_queue(self, queue_name):
        current_byte_position = self.file_adaptor.read_queue_position(queue_name)

        if current_byte_position is False:
            return ''

        next_byte_position, read_message = self.file_adaptor.read_message(queue_name, current_byte_position)

        processing_queue = self.in_flight_queue_name(queue_name)

        in_flight_position, content = self.file_adaptor.store_message(processing_queue, json.loads(read_message))

        self.file_adaptor.store_queue_position(queue_name, next_byte_position)

        return read_message, in_flight_position, next_byte_position

    def clear_queue(self, queue_name):
        self.file_adaptor.clear_queue_store(queue_name)
        self.file_adaptor.store_queue_position(queue_name, 0)

        return True

    @staticmethod
    def in_flight_queue_name(queue_name):
        return os.path.join('in_flight', queue_name)

    @property
    def file_adaptor(self):
        return self._file_adaptor

    @file_adaptor.setter
    def file_adaptor(self, value):
        self._file_adaptor = value

