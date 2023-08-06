from flyers.datetimes import *
import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        t = 1624170600
        d = datetime.fromtimestamp(t)

        self.assertEqual(timestamp_to_date_str(t), '2021-06-20')
        self.assertEqual(timestamp_to_datetime_str(t), '2021-06-20 14:30:00')

        self.assertEqual(parse_datetime('2021-06-20 14:30:00'), d)
        self.assertEqual(parse_date('2021-06-20'), datetime.fromtimestamp(1624118400))

        self.assertFalse(check_datetime('2021-002-1212'))

        print(format_duration(1657247354000))


if __name__ == '__main__':
    unittest.main()
