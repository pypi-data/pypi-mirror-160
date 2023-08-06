import json


class DatabaseConf(object):
    def __init__(self,
                 database: str,
                 host: str = 'localhost',
                 port: int = 3306,
                 user: str = 'root',
                 password: str = ''):
        self.database = database
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def __str__(self):
        return str(self.__dict__)

    def json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_dict(d):
        return DatabaseConf(
            database=d['database'],
            host=d['host'],
            user=d['user'],
            port=d['port'],
            password=d['password']
        )


from . import pool
from . import mysql
