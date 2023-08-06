import pymysql
from flyers.database import DatabaseConf
from flyers.logs import logger


def run_with(conn: pymysql.Connection, consumer_func):
    cursor = conn.cursor()
    consumer_func(cursor)
    conn.commit()
    cursor.close()


def create_connection(conf: DatabaseConf) -> pymysql.Connection:
    try:
        return pymysql.connect(host=conf.host,
                               port=conf.port,
                               user=conf.user,
                               password=conf.password,
                               database=conf.database)
    except Exception:
        msg = 'Init connection error, conf: {}'.format(conf.__dict__)
        logger.exception(msg)
        raise Exception(msg)


def show_mysql_server_version(cursor):
    cursor.execute("SELECT VERSION()")
    return cursor.fetchone()
