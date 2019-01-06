from abc import ABCMeta, abstractmethod


class FileInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def store(self, queue_name, content): raise NotImplementedError

    @abstractmethod
    def read(self, queue_name, message_position): raise NotImplementedError
