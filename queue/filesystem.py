from abc import ABCMeta, abstractmethod


class FileInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def store(self, queue_name, content): raise NotImplementedError

    # def update_queue_position
