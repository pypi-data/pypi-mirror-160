import unittest
from flyers.logs import logger
from flyers import logs


class MyTestCase(unittest.TestCase):

    def test_something(self):
        logger.info("haha %s", "ha")
        self.assertFalse(logs.is_debug())
        logger.debug("debug message")

        logs.set_debug_level()
        self.assertTrue(logs.is_debug())

        if logs.is_debug():
            logger.debug("debug message")


if __name__ == '__main__':
    unittest.main()
