from flyers.database import DatabaseConf
from flyers.logs import logger
import pymysql
from dbutils.pooled_db import PooledDB

# 最大连接数
MAX_CONNECTIONS = 10


def new_connection_pool(conf: DatabaseConf) -> PooledDB:
    logger.info('create new database connection pool, conf: {}'.format(conf))
    return PooledDB(
        pymysql,
        MAX_CONNECTIONS,
        host=conf.host,
        user=conf.user,
        port=conf.host,
        passwd=conf.password,
        db=conf.database,
        use_unicode=True)


def run_with(pool: PooledDB, consumer_func):
    conn, cursor = get_conn(pool)
    consumer_func(conn, cursor)
    close_conn(pool, conn, cursor)


def get_conn(pool: PooledDB):
    conn = pool.connection()
    return conn, conn.cursor()


def close_conn(pool: PooledDB, conn, cursor):
    pool.cache(conn)
    cursor.close()
