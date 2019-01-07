from queue.file_adaptors import LocalFileSystem
from queue.queue import Queue
import os
import json


def test_clear_queue_can_lower_position_to_zero_and_clear_queue_file():
    queue_name = 'test-queue'

    filesystem = LocalFileSystem('storage')
    byte_position_file_key = filesystem.queue_position_file_key
    queue_storage_key = filesystem.queue_storage_key(queue_name)

    Queue(filesystem).clear_queue(queue_name)

    with open(byte_position_file_key, 'r') as f:
        data = json.load(f)

        byte_position = data[queue_name]
        assert byte_position == 0
        f.close()

    assert os.path.getsize(queue_storage_key) == 0


def test_queue_can_store_a_message_as_encoded_json_and_byte_position():
    message = 'This is a test message'

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

        saved_message = json.loads(json.loads(line)['body'])

        assert message == saved_message

        file.close()


def test_queue_can_read_a_message_from_file_with_correct_json_and_increments_message_position():
    message = 'New test read message'

    queue_name = 'test-queue'

    filesystem = LocalFileSystem('storage')
    queue = Queue(filesystem)

    queue.clear_queue(queue_name)

    queue.append_message_to_queue(queue_name, message)
    current_position2 = queue.append_message_to_queue(queue_name, message)

    actual_message = queue.read_top_message_from_queue(queue_name)

    assert filesystem.read_queue_position(queue_name) == current_position2

    assert message == json.loads(json.loads(actual_message)['body'])
