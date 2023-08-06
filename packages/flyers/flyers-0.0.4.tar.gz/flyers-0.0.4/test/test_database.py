import unittest
from flyers import database
from flyers.database import DatabaseConf


class MyTestCase(unittest.TestCase):
    def test_something(self):
        conf = DatabaseConf(
            database='demo'
        )
        print(conf)
        conn = database.mysql.create_connection(conf)
        database.mysql.run_with(conn,
                                consumer_func=lambda cursor: print(database.mysql.show_mysql_server_version(cursor)))

    if __name__ == '__main__':
        unittest.main()
