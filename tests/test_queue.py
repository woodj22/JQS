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

    byte_position, content = Queue(filesystem).append_message_to_queue(queue_name, message)

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


def test_queue_can_read_a_message_from_file_with_correct_json_increments_message_position_and_copy_to_in_flight():
    message = 'New test read message'

    queue_name = 'test-queue'

    filesystem = LocalFileSystem('storage')
    queue = Queue(filesystem)
    position_file_key = filesystem.queue_position_file_key
    queue.clear_queue(queue_name)

    queue.append_message_to_queue(queue_name, message)

    in_flight_position, actual_message, next_byte_position = queue.read_top_message_from_queue(queue_name)

    assert message == json.loads(json.loads(actual_message)['body'])

    in_flight_key = filesystem.queue_storage_key(os.path.join('in_flight', queue_name))
    # Assert message in in_flight/{test-queue} file
    with open(in_flight_key, 'r') as file:

        file.seek(in_flight_position)

        message = file.readline()

        assert actual_message == message

    # Assert new position stored
    with open(position_file_key, 'r') as file:

        data = json.load(file)

        if queue_name not in data:
            return False
        file.close()
        byte_position = data[queue_name]
        assert byte_position == next_byte_position
