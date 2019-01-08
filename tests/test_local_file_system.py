import pytest

from queue.file_adaptors import LocalFileSystem
import json


def test_it_can_store_message_in_the_correct_place():
    filesystem = LocalFileSystem('storage')
    filesystem.clear_queue_store('test-queue')
    storage_key = filesystem.queue_storage_key('test-queue')
    message_body = 'This is the content body'

    filesystem.store_message('test-queue', message_body)

    with open(storage_key, 'r+') as file:
        line = file.readline()
        # exit(line)
        assert message_body == json.loads(json.loads(line)['body'])
        assert type(json.loads(line)['created_at']) == int
        assert (json.loads(line)['retries']) == 0


def test_it_can_read_message_from_a_byte_position_and_return_message_and_byte_position():

    filesystem = LocalFileSystem('storage')
    filesystem.clear_queue_store('test-queue')
    storage_key = filesystem.queue_storage_key('test-queue')
    message_body = 'This is the content body'
    queue_name, byte_position = filesystem.store_message('test-queue', message_body)

    actual_message, next_byte_position = filesystem.read_message('test-queue', byte_position)

    message_length = len(actual_message.encode('UTF-8'))

    assert message_body == json.loads(json.loads(actual_message)['body'])

    assert next_byte_position == (byte_position + message_length)

    with open(storage_key, 'r+') as file:
        line = file.readline()

        assert message_body == json.loads(json.loads(line)['body'])
