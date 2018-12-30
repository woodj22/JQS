from queue.message import make_message


def test_it_can_make_message():
    body = 'this is a test message body.'
    expected = make_message(body)

    assert expected['body'] == body
    assert expected['retries'] == 0
