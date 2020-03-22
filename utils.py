# -*- coding: utf-8 -*-
import pymysql


def get_conn():
    """
    数据库连接
    :return: connection obj, cursor obj
    """
    conn = pymysql.connect(host='localhost', user='root', password='123456', database='covid_2019',
                           charset='utf8mb4')
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):
    """
    关闭数据库连接
    :param cursor: cursor obj
    :param conn: connection obj
    :return: None
    """
    conn.close()
    cursor.close()


def sql_query(sql, args=None):
    """
    SQL查询
    :param sql: SQL语句
    :param args: 查询参数
    :return: 查询结果
    """
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res
