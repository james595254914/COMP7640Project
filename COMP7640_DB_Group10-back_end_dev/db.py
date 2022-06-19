import pymysql


def connection():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='gg123',
                           database='project',
                           charset='utf8')
