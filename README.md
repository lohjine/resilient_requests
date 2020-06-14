# resilient_requests
 
Python requests library is awesome, and makes it really quick to just requests.get(url) for something. But oftentimes when this gets used in long-running processes, it will eventually run into errors of some sort, or retrieving unexpected results.

Hence the next step is to make your call resilient by adding retry code, checking for correct status code. This gets tedious quick as it has to be added to every single call. This wrapper helps you to make your call resilient, and starts off with sane defaults.

[resilient_code](https://github.com/lohjine/resilient_code) - General resilient code

## Installation

```
pip install git+https://github.com/lohjine/resilient_requests
```

## Usage

```python
import resilient_requests as r_requests

r = r_requests.get(url, timeout=15, expected_status_code = [200], max_tries = 3, exponential_backoff={'min': 0.1, 'max': 5})
r = r_requests.put(url, timeout=15, expected_status_code = [200], max_tries = 3, exponential_backoff={'min': 0.1, 'max': 5})
r = r_requests.delete(url, timeout=15, expected_status_code = [200], max_tries = 3, exponential_backoff={'min': 0.1, 'max': 5})
r = r_requests.head(url, timeout=15, expected_status_code = [200], max_tries = 3, exponential_backoff={'min': 0.1, 'max': 5})
r = r_requests.options(url, timeout=15, expected_status_code = [200], max_tries = 3, exponential_backoff={'min': 0.1, 'max': 5})

```

r_requests functions are wrappers around their requests counterpart, with additional parameters (and their default parameters) noted in the examples above.

Additional arguments are passed into the underlying requests call.
