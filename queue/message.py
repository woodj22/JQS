import time


def make_message(body, retries=0):
    return {
        'body': body,
        'retries': retries,
        'created_at': time.time()
    }
