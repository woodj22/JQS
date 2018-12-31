from queue.file_adaptors import LocalFileSystem
from queue.queue import Queue
import os


def clean_up_test_message(file_path):
    if os.path.exists(file_path):
        return os.remove(file_path)
    return False


def test_queue_can_store_a_message_as_encoded_json_and_return_message_file_path():

    message = {
        'body': 'test body',
        'retries': 0,
        'created_at': "now"
    }
    queue_name = 'test-queue'

    filesystem = LocalFileSystem('storage')

    message_file_path = Queue(filesystem).append_message_to_file(queue_name, message)

    file_exists = os.path.isfile(message_file_path)

    # clean_up_test_message(message_file_path)

    assert file_exists is True

# def test_queue_can_read_a_message_from_file_and_return_message():
#     message = {
#         'body': 'test body',
#         'retries': 0,
#         'created_at': "now"
#     }
#     filesystem = LocalFileSystem('storage')