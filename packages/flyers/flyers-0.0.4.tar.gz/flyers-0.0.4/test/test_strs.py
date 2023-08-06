import unittest
from flyers import strs


class MyTestCase(unittest.TestCase):

    def test_something(self):
        self.assertTrue(strs.is_blank('  '))
        self.assertFalse(strs.is_blank(' hello '))


if __name__ == '__main__':
    unittest.main()
