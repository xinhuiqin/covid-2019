# -*- coding：utf-8 -*-
import json
import time
import traceback

import pymysql
import requests

from utils import get_conn, close_conn

tencent_h5_url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
tencent_other_url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_other'


def get_tencent_data():
    """
    抓取腾讯数据。
    :return:
    """
    # 因为是从多个对象里取数据，需要更新，所以最外层应该使用字典
    china_day_data = {}
    # 可以一次性for循环完，所以最外层可以使用列表或者字典
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
        imported_case = i['importedCase']  # 累计输入病例
        dead_rate = i['deadRate']  # 累计死亡率
        heal_rate = i['healRate']  # 累计治愈率
        month, day = i['date'].split('.')  # 日期
        ds = '2020-%s-%s' % (month, day)
        china_day_data[ds] = {
            'confirm': confirm,
            'suspect': suspect,
            'dead': dead,
            'heal': heal,
            'now_confirm': now_confirm,
            'now_severe': now_severe,
            'imported_case': imported_case,
            'dead_rate': dead_rate,
            'heal_rate': heal_rate,
            # 每日新增从1.20开始才有数据，所以现在设置值为0，后续再更新
            'add_confirm': 0,
            'add_suspect': 0,
            'add_dead': 0,
            'add_heal': 0,
            'add_imported_case': 0
        }
    china_day_add_list = data['chinaDayAddList']
    for i in china_day_add_list:
        month, day = i['date'].split('.')  # 日期
        ds = '2020-%s-%s' % (month, day)
        add_confirm = i['confirm']
        add_suspect = i['suspect']
        add_dead = i['dead']
        add_heal = i['heal']
        add_imported_case = i['importedCase']
        china_day_data[ds].update(
            {
                'add_confirm': add_confirm,
                'add_suspect': add_suspect,
                'add_dead': add_dead,
                'add_heal': add_heal,
                'add_imported_case': add_imported_case
            }
        )

    # 省市每日数据汇总
    h5_resp = requests.get(tencent_h5_url)
    h5_data = json.loads(h5_resp.json()['data'])
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


def insert_china_day():
    """
       中国每日汇总数据表首次插入
       :return: None
       """
    conn = None
    cursor = None
    try:
        data = get_tencent_data()[0]
        conn, cursor = get_conn()
        sql = '''
               INSERT INTO china_day_list VALUES(%(ds)s, %(confirm)s, %(suspect)s,  %(dead)s, %(heal)s,  
               %(now_confirm)s, %(now_severe)s,  %(imported_case)s,  %(dead_rate)s,  %(heal_rate)s,
               %(add_confirm)s, %(add_suspect)s,%(add_dead)s,%(add_heal)s, %(add_imported_case)s)
           '''
        print(f'{time.asctime()} china_day_list开始插入数据')
        for k, v in data.items():
            v.update({'ds': k})
            cursor.execute(sql, v)
        conn.commit()
        print(f'{time.asctime()} china_day_list插入数据完毕')
    except:
        conn.rollback()
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


def update_china_day():
    """
       更新中国每日汇总数据(每日只更新一次)
       :return: None
       """
    conn = None
    cursor = None
    try:
        data = get_tencent_data()[0]
        conn, cursor = get_conn()
        sql = '''INSERT INTO china_day_list VALUES(%(ds)s, %(confirm)s, %(suspect)s,  %(dead)s, %(heal)s, 
                    %(now_confirm)s, %(now_severe)s,  %(imported_case)s,  %(dead_rate)s,  %(heal_rate)s,
                    %(add_confirm)s, %(add_suspect)s,%(add_dead)s,%(add_heal)s, %(add_imported_case)s)
                '''
        # 多条数据的有无判断
        sql_query = '''
            SELECT confirm FROM china_day_list where ds=%s
        '''
        cursor.execute(sql_query, list(data.items())[-1][0])
        if not cursor.fetchone():
            print(f'{time.asctime()} 开始更新china_day_list')
            list(data.items())[-1][1].update({'ds': list(data.items())[-1][0]})
            cursor.execute(sql, list(data.items())[-1][1])
            conn.commit()
            print(f'{time.asctime()} china_day_list更新完毕')
        else:
            print(f'{time.asctime()} china_day_list已是最新数据')
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
        if not cursor.fetchone()[0]:
            print(f'{time.asctime()}:provience_day_list数据开始更新')
            for item in data:
                cursor.execute(sql, item)
            conn.commit()
            print(f'{time.asctime()}:provience_day_list更新最新数据完毕')
        else:
            print(f'{time.asctime()}:provience_day_list已是最新数据')
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


if __name__ == '__main__':
    insert_china_day()
    insert_provience_day()
    update_china_day()
