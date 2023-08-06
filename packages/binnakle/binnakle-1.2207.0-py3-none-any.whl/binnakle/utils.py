import time


def get_timestamp_ms():
    return int(round(time.time() * 1000))


def remove_empty_keys(d):
    return {k: v for k, v in d.items() if v}
