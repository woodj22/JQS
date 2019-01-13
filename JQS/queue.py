from JQS.message import make_message
from .filesystem import StorageInterface
import json
import os


class Queue:
    def __init__(self, file_adaptor: StorageInterface):
        self._file_adaptor = file_adaptor

    def append_message_to_queue(self, queue_name, content_body):
        """
        Creates a message by encoding the content and storing it in the queue.
        :param queue_name: str
        :param content_body: obj
        :return: set (position, message content)
        """
        message = make_message(json.dumps(content_body))

        byte_position, content = self.file_adaptor.store_message(queue_name, message)

        return byte_position, content

    def read_top_message_from_queue(self, queue_name):
        """
        Read the next message from the queue. This will add the message into the in flight queue
        and move the next available message position to the next message.
        :param queue_name:  str
        :return: set(in flight position, message, next position)
        """
        current_byte_position = self._file_adaptor.read_queue_position(queue_name)

        next_byte_position, read_message = self._file_adaptor.read_message(queue_name, current_byte_position)

        processing_queue = self.in_flight_queue_name(queue_name)

        in_flight_position, content = self.file_adaptor.store_message(processing_queue, json.loads(read_message))

        self._file_adaptor.store_queue_position(queue_name, next_byte_position)

        return in_flight_position, read_message, next_byte_position

    def clear_queue(self, queue_name):
        """
        Delete all messages from the queue and reset the queue position to 0
        :param queue_name: str
        :return: True
        """
        self._file_adaptor.clear_queue_store(queue_name)
        self._file_adaptor.store_queue_position(queue_name, 0)

        return True

    def message_has_completed(self, queue_name, position):
        """
        Mark a message as completed by deleting it from the in flight queue
        :param queue_name:
        :param position:
        :return:
        """
        self._file_adaptor.delete_message(self.in_flight_queue_name(queue_name), position)

        return True

    def message_has_failed(self, queue_name, position):
        """
        Return true if the message is being retried. It can be retried if it has a retry count > 0
        Return false if message has timed out or retry count == 0
        :param queue_name: str
        :param position: str
        :return: bool
        """
        in_flight_queue_name = self.in_flight_queue_name(queue_name)
        next_byte_position, message = self._file_adaptor.read_message(in_flight_queue_name, position)

        try:
            # Check message is json and has not already been deleted from in flight
            message_dict = json.loads(message)
        except ValueError:
            return False

        if 'retries' in message_dict:
            self._file_adaptor.delete_message(in_flight_queue_name, position)
            if message_dict['retries'] == 0:
                return False

            message_dict['retries'] -= 1
            self._file_adaptor.store_message(queue_name, message_dict)

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
