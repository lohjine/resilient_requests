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
        exception = False
        msg = 'Unknown Error, error message not filled out'

        # default arguments are not instantiated until actual function call below
        # but if user specify, it will appear in kwargs
        # so we manually fill with default arguments if not present in kwargs
        expected_status_code = kwargs.get('expected_status_code', [200])
        max_tries = kwargs.get('max_tries', 3)
        exponential_backoff = kwargs.get(
            'exponential_backoff', {'min': 0.1, 'max': 5})
        jitter = kwargs.get('jitter', 0.05)

        if not isinstance(expected_status_code, (list,tuple)):
            raise TypeError(f'expected_status_code was {expected_status_code}, but it must be a list or tuple')
        if not all([isinstance(i, int) for i in expected_status_code]):
            raise ValueError(f'expected_status_code was {expected_status_code}, but it must contain all integers')
        if not isinstance(max_tries, int):
            raise TypeError(f'max_tries was {type(max_tries)}, but it must be an integer')
        if not max_tries > 0:
            raise ValueError('max_tries must be more than 0')
        if not (isinstance(exponential_backoff, dict) or not exponential_backoff):
            raise TypeError(f'exponential_backoff was {exponential_backoff}, but it must be a dict or falsy')
        if isinstance(exponential_backoff, dict):
            if not (isinstance(exponential_backoff.get('min', False), (float, int)) and isinstance(exponential_backoff.get('max', False), (float, int))):
                raise ValueError(f"exponential_backoff was {exponential_backoff}, but it must contain keys 'min' and 'max' with float/int values")
        if not isinstance(jitter, float):
            raise TypeError(f'jitter was {type(jitter)}, but it must be a float')
        if not jitter >= 0:
            raise ValueError('jitter must be more than or equal to 0')

        while True:
            tries += 1

            try:
                r = func(*args, **kwargs)

                if r.status_code in expected_status_code:
                    break

                if r.status_code == 429:
                    if status_codes:
                        msg = f'Got status codes: {status_codes}, and 429 Too Many Requests'
                    else:
                        msg = f'Got status code: 429 Too Many Requests'

                status_codes.add(r.status_code)

            except Exception as e:
                exception = e

            if 429 in status_codes: # do not retry if 429 Too Many Requests
                 raise(HTTPStatusCodeError(msg))

            if tries >= max_tries:
                if exception:
                    raise exception
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
                sleep_time += random.random() * jitter

            time.sleep(sleep_time)

        return r

    return wrapper_resilient_requests


@resilient_requests
def get(url, timeout=15, expected_status_code=[200], max_tries=3,
        exponential_backoff={'min': 0.1, 'max': 5}, jitter=0.05, *args, **kwargs):
    """
    Sends a resilient GET request.

    Args:
        url (str): URL for the new :class:`Request` object.
        timeout (int): timeout for the new :class:`Request` object.
        expected_status_code (list of int): Expected status code for your request, request will be retried/raise error if other status codes are received.
        max_tries (int): Number of retries for request
        exponential_backoff (dict or falsy): Backoff parameters for retries. 'min' is number of seconds for the first retry. 'max' is the maximum number of seconds for each retry. Set equal values for both to have a constant retry interval. Note that jitter of +-50ms is automatically added.
        jitter (float): Amount of jitter in seconds for retries
        *args: Additional arguments will be passed into the `Request` object.
        *args: Additional named arguments will be passed into the `Request` object.

    Returns:
        :class:`Request` object
    """
    r = requests.get(url, timeout=timeout, *args, **kwargs)
    return r


@resilient_requests
def put(url, timeout=15, expected_status_code=[200], max_tries=3,
        exponential_backoff={'min': 0.1, 'max': 5}, jitter=0.05, *args, **kwargs):
    """
    Sends a resilient PUT request.

    Args:
        url (str): URL for the new :class:`Request` object.
        timeout (int): timeout for the new :class:`Request` object.
        expected_status_code (list of int): Expected status code for your request, request will be retried/raise error if other status codes are received.
        max_tries (int): Number of retries for request
        exponential_backoff (dict or falsy): Backoff parameters for retries. 'min' is number of seconds for the first retry. 'max' is the maximum number of seconds for each retry. Set equal values for both to have a constant retry interval. Note that jitter of +-50ms is automatically added.
        jitter (float): Amount of jitter in seconds for retries
        *args: Additional arguments will be passed into the `Request` object.
        *args: Additional named arguments will be passed into the `Request` object.

    Returns:
        :class:`Request` object
    """
    r = requests.put(url, timeout=timeout, *args, **kwargs)
    return r


@resilient_requests
def delete(url, timeout=15, expected_status_code=[200], max_tries=3,
           exponential_backoff={'min': 0.1, 'max': 5}, jitter=0.05, *args, **kwargs):
    """
    Sends a resilient DELETE request.

    Args:
        url (str): URL for the new :class:`Request` object.
        timeout (int): timeout for the new :class:`Request` object.
        expected_status_code (list of int): Expected status code for your request, request will be retried/raise error if other status codes are received.
        max_tries (int): Number of retries for request
        exponential_backoff (dict or falsy): Backoff parameters for retries. 'min' is number of seconds for the first retry. 'max' is the maximum number of seconds for each retry. Set equal values for both to have a constant retry interval. Note that jitter of +-50ms is automatically added.
        jitter (float): Amount of jitter in seconds for retries
        *args: Additional arguments will be passed into the `Request` object.
        *args: Additional named arguments will be passed into the `Request` object.

    Returns:
        :class:`Request` object
    """
    r = requests.delete(url, timeout=timeout, *args, **kwargs)
    return r


@resilient_requests
def head(url, timeout=15, expected_status_code=[200], max_tries=3,
         exponential_backoff={'min': 0.1, 'max': 5}, jitter=0.05, *args, **kwargs):
    """
    Sends a resilient HEAD request.

    Args:
        url (str): URL for the new :class:`Request` object.
        timeout (int): timeout for the new :class:`Request` object.
        expected_status_code (list of int): Expected status code for your request, request will be retried/raise error if other status codes are received.
        max_tries (int): Number of retries for request
        exponential_backoff (dict or falsy): Backoff parameters for retries. 'min' is number of seconds for the first retry. 'max' is the maximum number of seconds for each retry. Set equal values for both to have a constant retry interval. Note that jitter of +-50ms is automatically added.
        jitter (float): Amount of jitter in seconds for retries
        *args: Additional arguments will be passed into the `Request` object.
        *args: Additional named arguments will be passed into the `Request` object.

    Returns:
        :class:`Request` object
    """
    r = requests.head(url, timeout=timeout, *args, **kwargs)
    return r


@resilient_requests
def options(url, timeout=15, expected_status_code=[200], max_tries=3,
            exponential_backoff={'min': 0.1, 'max': 5}, jitter=0.05, *args, **kwargs):
    """
    Sends a resilient OPTIONS request.

    Args:
        url (str): URL for the new :class:`Request` object.
        timeout (int): timeout for the new :class:`Request` object.
        expected_status_code (list of int): Expected status code for your request, request will be retried/raise error if other status codes are received.
        max_tries (int): Number of retries for request
        exponential_backoff (dict or falsy): Backoff parameters for retries. 'min' is number of seconds for the first retry. 'max' is the maximum number of seconds for each retry. Set equal values for both to have a constant retry interval. Note that jitter of +-50ms is automatically added.
        jitter (float): Amount of jitter in seconds for retries
        *args: Additional arguments will be passed into the `Request` object.
        *args: Additional named arguments will be passed into the `Request` object.

    Returns:
        :class:`Request` object
    """
    r = requests.options(url, timeout=timeout, *args, **kwargs)
    return r
