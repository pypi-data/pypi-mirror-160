import unittest
from flyers import nets


class MyTestCase(unittest.TestCase):
    def test_something(self):
        resp = nets.http_get('http://httpbin.org/get')

        self.assertTrue(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
