from queue.file_adaptors import LocalFileSystem
from queue.queue import Queue
import os


def clean_up_test_message(file_path):
    if os.path.exists(file_path):
        return os.remove(file_path)
    return False


def test_queue_can_store_a_message_and_return_true():

    message = {
        'body': 'test body',
        'retries': 0,
        'created_at': "now"
    }
    filesystem = LocalFileSystem('storage')

    message_file_path = Queue(filesystem).save_message_to_file(message)

    file_exists = os.path.isfile(message_file_path)

    clean_up_test_message(message_file_path)

    assert file_exists is True

