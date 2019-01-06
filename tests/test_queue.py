from queue.file_adaptors import LocalFileSystem
from queue.queue import Queue
import os
import json

def clean_up_test_message(file_path):
    if os.path.exists(file_path):
        return os.remove(file_path)
    return False


def test_queue_can_store_a_message_as_encoded_json_and_byte_position():

    message = {
        'body': 'test body',
        'retries': 0,
        'created_at': "now"
    }
    queue_name = 'test-queue'

    filesystem = LocalFileSystem('storage')

    byte_position = Queue(filesystem).append_message_to_queue(queue_name, message)
    file_path = filesystem.queue_storage_key(queue_name)
    file_exists = os.path.isfile(file_path)

    assert file_exists is True

    with open(file_path, 'r+') as file:
        file.seek(byte_position)
        line = file.readline()
        assert type(line) == str

        saved_message = json.loads(line)

        assert message == saved_message

        file.close()


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