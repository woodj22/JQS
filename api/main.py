from JQS.queue import Queue
from flask import Flask
from flask import request, abort
import json

from JQS.file_adaptors import LocalFileSystem

app = Flask(__name__)

filesystem = LocalFileSystem('storage')
jqs = Queue(filesystem)


@app.route('/JQS/<queue_name>/messages', methods=['GET', 'POST'])
def messages(queue_name):
    if request.method == 'POST':

        message = request.get_json()['message_body']

        jqs.append_message_to_queue(queue_name, message)

        return "OK"
    elif request.method == 'GET':
        in_flight_position, message, byte_message = jqs.read_top_message_from_queue(queue_name)

        message_object = json.loads(message)
        if message_object == '':
            return ''

        message_object['id'] = in_flight_position

        return json.dumps(message_object)

    abort(404)


@app.route('/JQS/<queue_name>/messages/<message_id>', methods=['POST'])
def update_message_status(queue_name, message_id):
    action = request.args.get('action')

    if action == 'completed':
        jqs.message_has_completed(queue_name, int(message_id))
        return 'completed'

    elif action == 'failed':
        jqs.message_has_failed(queue_name, int(message_id))
        return 'failed'
    return 'hello world'

# GET /JQS/<queue_name>/
# Returns ?paginated? list of in_flight and To-Do jobs

# POST /JQS/<queue_name>/messages/{in_flight_position}/?action=completed
# Returns True if message is there.
# Deletes message from in_flight JQS

# POST /JQS/<queue_name>/messages/{in_flight_position}/?action=failed
# Returns job failed If count == 0.
# Deletes message from processing JQS.
#
# Returns job retried if count > 0.
# Copy message back to To-Do JQS
