from abc import ABCMeta, abstractmethod


class StorageInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def store_message(self, queue_name, content): raise NotImplementedError

    @abstractmethod
    def read_message(self, queue_name, message_position): raise NotImplementedError

    @abstractmethod
    def delete_message(self, queue_name, message_position): raise NotImplementedError

    @abstractmethod
    def store_queue_position(self, queue_name, message_position): raise NotImplementedError

    @abstractmethod
    def read_queue_position(self, queue_name): raise NotImplementedError

    @abstractmethod
    def clear_queue_store(self, queue_name): raise NotImplementedError
