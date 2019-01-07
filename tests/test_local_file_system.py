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
