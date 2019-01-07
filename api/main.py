from queue.queue import Queue
from flask import Flask
from flask import request

from queue.file_adaptors import LocalFileSystem

app = Flask(__name__)


@app.route('/jqs/<queue_name>', methods=['GET', 'POST'])
def handle_queue(queue_name):
    filesystem = LocalFileSystem('storage')

    if request.method == 'POST':
        message = request.get_json()['message_body']

        Queue(filesystem).append_message_to_queue(queue_name, message)

        return "OK"
    else:
        actual_message = Queue(filesystem).read_top_message_from_queue(queue_name)

        return actual_message

