import json
from .filesystem import FileInterface


class Queue:
    def __init__(self, file_adaptor: FileInterface):
        self._file_adaptor = file_adaptor

    def append_message_to_file(self, queue_name, message):
        return self.file_adaptor.store(queue_name, message)

    @property
    def file_adaptor(self):
        return self._file_adaptor

    @file_adaptor.setter
    def file_adaptor(self, value):
        self._file_adaptor = value
