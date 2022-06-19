import pymysql


def connection():
    return pymysql.connect(host='175.178.71.209',
                           user='comp',
                           password='comp7640',
                           database='comp7640',
                           charset='utf8')
