from abc import ABCMeta, abstractmethod


class FileInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def save(self, queue_name, content): raise NotImplementedError
