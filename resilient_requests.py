import requests
import functools
import time
import random


class HTTPStatusCodeError(Exception):
    def __init__(self, message):
        super().__init__(message)


def resilient_requests(func):
    @functools.wraps(func)
    def wrapper_resilient_requests(*args, **kwargs):

        tries = 0
        sleep_time = 0
        status_codes = set()

        # default arguments are not instantiated until actual function call below
        # but if user specify, it will appear in kwargs
        # so we manually fill with default arguments if not present in kwargs
        expected_status_code = kwargs.get('expected_status_code', [200])
        max_tries = kwargs.get('max_tries', 3)
        exponential_backoff = kwargs.get(
            'exponential_backoff', {'min': 0.1, 'max': 5})

        while True:
            tries += 1
            r = func(*args, **kwargs)

            if r.status_code in expected_status_code:
                break

            if r.status_code == 429:  # do not retry if 429 Too Many Requests
                if status_codes:
                    msg = f'Got status codes: {status_codes}, and 429 Too Many Requests'
                else:
                    msg = f'Got status code: 429 Too Many Requests'
                raise(HTTPStatusCodeError(msg))

            status_codes.add(r.status_code)

            if tries >= max_tries:
                if len(status_codes) == 1:
                    msg = f'Got status code: {r.status_code}, expected: {expected_status_code}'
                else:
                    msg = f'Got status codes: {status_codes}, expected: {expected_status_code}'
                raise(HTTPStatusCodeError(msg))

            if exponential_backoff:
                if sleep_time == 0:
                    sleep_time = exponential_backoff['min']
                else:
                    sleep_time *= 2
                    if sleep_time > exponential_backoff['max']:
                        sleep_time = exponential_backoff['max']

                # add jitter
                sleep_time += random.randint(-50, 50) / 1000

            time.sleep(sleep_time)

        return r

    return wrapper_resilient_requests


@resilient_requests
def get(url, timeout=15, expected_status_code=[200], max_tries=3,
        exponential_backoff={'min': 0.1, 'max': 5}, *args, **kwargs):
    r = requests.get(url, timeout=timeout, *args, **kwargs)
    return r


@resilient_requests
def put(url, timeout=15, expected_status_code=[200], max_tries=3,
        exponential_backoff={'min': 0.1, 'max': 5}, *args, **kwargs):
    r = requests.put(url, timeout=timeout, *args, **kwargs)
    return r


@resilient_requests
def delete(url, timeout=15, expected_status_code=[200], max_tries=3,
           exponential_backoff={'min': 0.1, 'max': 5}, *args, **kwargs):
    r = requests.delete(url, timeout=timeout, *args, **kwargs)
    return r


@resilient_requests
def head(url, timeout=15, expected_status_code=[200], max_tries=3,
         exponential_backoff={'min': 0.1, 'max': 5}, *args, **kwargs):
    r = requests.head(url, timeout=timeout, *args, **kwargs)
    return r


@resilient_requests
def options(url, timeout=15, expected_status_code=[200], max_tries=3,
            exponential_backoff={'min': 0.1, 'max': 5}, *args, **kwargs):
    r = requests.options(url, timeout=timeout, *args, **kwargs)
    return r
