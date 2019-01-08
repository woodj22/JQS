from queue.file_adaptors import LocalFileSystem
import json


def test_it_can_store_message_correctly():
    filesystem = LocalFileSystem('storage')
    filesystem.clear_queue_store('test-queue')
    storage_key = filesystem.queue_storage_key('test-queue')
    message_body = 'This is the content body'

    filesystem.store_message('test-queue', message_body)

    with open(storage_key, 'r+') as file:
        line = file.readline()
        assert message_body == json.loads(line)


def test_it_can_read_message_from_a_byte_position_and_return_message_and_byte_position():

    filesystem = LocalFileSystem('storage')
    message_body = 'This is the content body'
    queue_name, byte_position = filesystem.store_message('test-queue', message_body)

    next_byte_position, actual_message = filesystem.read_message('test-queue', byte_position)
    message_length = len(actual_message.encode('UTF-8'))

    assert message_body == json.loads(actual_message)

    assert next_byte_position == (byte_position + message_length)
