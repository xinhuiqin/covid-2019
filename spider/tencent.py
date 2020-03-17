# -*- coding：utf-8 -*-
from datetime import date
from datetime import datetime
import json
import time
import traceback

import pymysql
import requests

tencent_h5_url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
tencent_other_url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_other'


def get_tencent_data():
    """
    抓取腾讯数据。
    :return:
    """
    china_day_data = []
    provience_day_data = []

    # 中国每日数据详情
    resp = requests.get(tencent_other_url)
    data = json.loads(resp.json()['data'])
    china_day_list = data['chinaDayList']
    china_day_list.sort(key=lambda x: x['date'])
    for i in china_day_list:
        confirm = i['confirm']  # 累计确诊
        suspect = i['suspect']  # 累计疑似
        dead = i['dead']  # 累计死亡
        heal = i['heal']  # 累计治愈
        now_confirm = i['nowConfirm']  # 现有确诊
        now_severe = i['nowSevere']  # 现有重症
        imported_case = i['importedCase']  # 当前输入病例
        dead_rate = i['deadRate']  # 累计死亡率
        heal_rate = i['healRate']  # 累计治愈率
        month, day = i['date'].split('.')  # 日期
        ds = '2020-%s-%s' % (month, day)
        china_day_data.append(
            {
                'ds': ds,
                'confirm': confirm,
                'suspect': suspect,
                'dead': dead,
                'heal': heal,
                'now_confirm': now_confirm,
                'now_severe': now_severe,
                'imported_case': imported_case,
                'dead_rate': dead_rate,
                'dead_rate': dead_rate,
                'heal_rate': heal_rate
            }
        )

    # 省市每日数据汇总
    h5_resp = requests.get(tencent_h5_url)
    h5_data = json.loads(h5_resp.json()['data'])
    # update_time = datetime.strptime(h5_data['lastUpdateTime'], '%Y-%m-%d %H:%M:%S')  # 数据最后更新时间
    update_time = h5_data['lastUpdateTime']  # 数据最后更新时间
    provience_data = h5_data['areaTree'][0]['children']  # 中国各省市
    for provience_infos in provience_data:
        provience = provience_infos['name']  # 省名
        for city_infos in provience_infos['children']:
            city = city_infos['name']  # 市名
            confirm = city_infos['total']['confirm']  # 累计确诊
            confirm_add = city_infos['today']['confirm']  # 新增确诊
            heal = city_infos['total']['heal']  # 累计治愈
            dead = city_infos['total']['dead']  # 累计死亡
            provience_day_data.append([provience, city, confirm, confirm_add, heal, dead, update_time])
    return china_day_data, provience_day_data


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
    if conn:
        conn.close()
    if cursor:
        cursor.close()


def insert_china_day():
    """
    插入中国每日汇总数据
    :return: None
    """
    conn = None
    cursor = None
    try:
        data = get_tencent_data()[0]
        print(f'{time.asctime()} 开始插入历史数据')
        conn, cursor = get_conn()
        sql = '''
            INSERT INTO china_day_list VALUES(%(ds)s, %(confirm)s, %(suspect)s,  %(dead)s, 
             %(heal)s,  %(now_confirm)s,  %(now_severe)s,  %(imported_case)s,  %(dead_rate)s,  %(heal_rate)s)
        '''
        for i in data:
            cursor.execute(sql, i)
        conn.commit()
        print(f'{time.asctime()} 插入历史数据完毕')
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


def update_china_day():
    """
       更新中国每日汇总数据
       :return: None
       """
    conn = None
    cursor = None
    try:
        print(f'{time.asctime()} 开始更新china_day_list')
        data = get_tencent_data()[0]
        conn, cursor = get_conn()
        sql = '''
               INSERT INTO china_day_list VALUES(%(ds)s, %(confirm)s, %(suspect)s,  %(dead)s, 
                %(heal)s,  %(now_confirm)s,  %(now_severe)s,  %(imported_case)s,  %(dead_rate)s,  %(heal_rate)s)
           '''
        # 多条数据的有无判断
        sql_query = '''
            SELECT confirm FROM china_day_list where ds=%s
        '''
        for i in data:
            cursor.execute(sql_query, i['ds'])
            if not cursor.fetchone():
                cursor.execute(sql, i)
        conn.commit()
        print(f'{time.asctime()} 更新china_day_list完毕')
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


def insert_provience_day():
    """
    更新省市每日汇总数据
    :return: None
    """
    conn = None
    cursor = None
    try:
        data = get_tencent_data()[1]
        conn, cursor = get_conn()
        sql = '''
        INSERT INTO provience_day_list(provience, city, confirm, confirm_add, heal, dead, update_time)
        VALUES(%s, %s, %s, %s, %s, %s, %s)
        '''
        # 只有一条数据的有无判断
        sql_query = 'select %s=(select update_time from provience_day_list order by id desc limit 1)'
        cursor.execute(sql_query, data[1][-1])
        if not cursor.fetchone():
            print(f'{time.asctime()}:开始更新最新数据')
            for item in data:
                cursor.execute(sql, item)
            conn.commit()
            print(f'{time.asctime()}:更新最新数据完毕')
        else:
            print(f'{time.asctime()}:已是最新数据')
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


if __name__ == '__main__':
    # insert_china_day()
    insert_provience_day()
    # update_china_day()

