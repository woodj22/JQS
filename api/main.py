from JQS.queue import Queue
from flask import Flask
from flask import request
import json

from JQS.file_adaptors import LocalFileSystem

app = Flask(__name__)


@app.route('/JQS/<queue_name>/messages', methods=['GET', 'POST'])
def handle_queue(queue_name):
    filesystem = LocalFileSystem('storage')

    if request.method == 'POST':
        message = request.get_json()['message_body']

        Queue(filesystem).append_message_to_queue(queue_name, message)

        return "OK"
    else:
        in_flight_position, message, byte_message = Queue(filesystem).read_top_message_from_queue(queue_name)

        message_object = json.loads(message)
        if message_object == '':

            return ''

        message_object['id'] = in_flight_position

        return json.dumps(message_object)

# GET /JQS/<queue_name>/
# Returns ?paginated? list of in_flight and To-Do jobs

# POST /JQS/<queue_name>/messages{in_flight_position}/completed
# Returns True if message is there.
# Deletes message from in_flight JQS

# POST /JQS/<queue_name>/messages{in_flight_position}/failed
# Returns job failed If count == 0.
# Deletes message from processing JQS.
#
# Returns job retried if count > 0.
# Copy message back to To-Do JQS

