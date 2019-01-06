from queue.file_adaptors import LocalFileSystem
from queue.queue import Queue
import os
import json

def clean_up_test_message(file_path):
    if os.path.exists(file_path):
        return os.remove(file_path)
    return False


def test_queue_can_store_a_message_as_encoded_json_and_return_byte_position():

    message = {
        'body': 'test body',
        'retries': 0,
        'created_at': "now"
    }
    queue_name = 'test-queue'

    filesystem = LocalFileSystem('storage')

    message_info = Queue(filesystem).append_message_to_queue(queue_name, message)

    file_exists = os.path.isfile(message_info[0])
    with open(message_info[0], 'r+') as file:
        file.seek(message_info[1])
        line = file.readline()
        # exit(line)
        # assert line == json.(message)
        # assert type(line) == str
        file.close()

    assert file_exists is True


def test_queue_can_read_a_message_from_file_and_return_message():
    message = {
        'body': 'test body',
        'retries': 0,
        'created_at': "now"
    }
    queue_name = 'test-queue'

    filesystem = LocalFileSystem('storage')

    message_info = Queue(filesystem).read_top_message_from_queue(queue_name, message)

    filesystem = LocalFileSystem('storage')