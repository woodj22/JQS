import json
from .filesystem import FileInterface


class Queue:
    def __init__(self, file_adaptor: FileInterface):
        self._file_adaptor = file_adaptor

    def save_message_to_file(self, message):
        return self.file_adaptor.save('test-queue', message)

    @property
    def file_adaptor(self):
        return self._file_adaptor

    @file_adaptor.setter
    def file_adaptor(self, value):
        self._file_adaptor = value
