from unittest import TestCase
import resilient_requests as r_requests


class TestGet(TestCase):
    def test_simple_request(self):
        r = r_requests.get('https://httpstat.us/200')
        self.assertTrue(r.status_code == 200)

    def test_404_request(self):
        try:
            r_requests.get('https://httpstat.us/404', max_tries=2)
            self.assertFalse('404 not reached')
        except Exception as e:
            self.assertTrue(
                e.args == (
                    'Got status code: 404, expected: [200]',))

    def test_429_request(self):
        try:
            r_requests.get('https://httpstat.us/429')
            self.assertFalse('429 not reached')
        except Exception as e:
            self.assertTrue(
                e.args == (
                    'Got status code: 429 Too Many Requests',))

    def test_timeout_request(self):
        try:
            r_requests.get(
                'https://httpstat.us/200',
                timeout=0.01,
                max_tries=2)
            self.assertFalse('Timeout not reached')
        except BaseException:
            self.assertTrue('Timeout reached')

    def test_expected_404(self):
        try:
            r = r_requests.get(
                'https://httpstat.us/404',
                expected_status_code=[404])
            self.assertTrue(r.status_code == 404)
        except BaseException:
            self.assertFalse('Exception raised instead of accepting 404')

    def test_expected_404_but_got_200(self):
        try:
            r_requests.get(
                'https://httpstat.us/200',
                expected_status_code=[404],
                max_tries=2)
            self.assertFalse('Accepted 200 instead of rejecting')
        except BaseException:
            self.assertTrue(True)
