import unittest
from flyers import systems
from flyers import logs


class MyTestCase(unittest.TestCase):

    def test_something(self):
        logs.set_debug_level()
        result = systems.run_shell_with_result("curl http://httpbin.org/get")
        if result == 0:
            logs.logger.info('success: {}'.format(result.stdout))
        else:
            logs.logger.info('failure: {}'.format(result.stderr))

        systems.run_shell('curl http://httpbin.org/get')
        systems.async_run_shell('curl http://httpbin.org/get', lambda ret: print(ret))


if __name__ == '__main__':
    unittest.main()
