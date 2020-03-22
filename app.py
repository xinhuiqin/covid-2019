# -*- coding: utf-8 -*-
from datetime import date
import json
from flask import Flask
from flask import render_template

from utils import sql_query

app = Flask(__name__)


@app.route('/')
def index():
    sql = '''
           SELECT ds, confirm, heal, dead, now_confirm, now_severe, imported_case FROM china_day_list
           ORDER BY ds DESC limit 1;
       '''
    res = sql_query(sql)[0]

    data = {
        'ds':res[0],
        'confirm': res[1],
        'heal': res[2],
        'dead': res[3],
        'now_confirm': res[4],
        'now_severe': res[5],
        'imported_case': res[6],
    }

    return render_template('index.html', data=data)


@app.route('/map')
def china_map():
    sql = '''
    SELECT provience, SUM( confirm ) FROM provience_day_list 
    WHERE update_time =( SELECT update_time FROM provience_day_list 
    ORDER BY update_time DESC LIMIT 1 ) GROUP BY provience
    '''
    china_map_data = []
    res = sql_query(sql)
    for tup in res:
        china_map_data.append({"name": tup[0], "value": int(tup[1])})
    return render_template('map.html', china_map_data=china_map_data)


@app.route('/trend/china')
def china_trend():
    """
    全国疫情趋势。
    :return:
    """
    data = []
    # “全国疫情新增趋势”数据:每日新增确诊，新增疑似
    add_new = []
    # “全国确诊(累计确诊，现有确诊)/现有疑似/现有重症”
    con_sus_serv = []
    # “全国累计治愈/死亡”
    dead_heal = []
    # “治愈率死亡率”
    dead_heal_rate = []

    sql = '''
        SELECT ds, add_confirm, add_suspect,
        confirm,now_confirm, suspect, now_severe,
        dead, heal,dead_rate, heal_rate
        FROM china_day_list china_day_list ORDER BY  ds ASC
    '''
    for ds, add_confirm, add_suspect, confirm, now_confirm, suspect, now_severe, dead, heal, dead_rate, heal_rate \
            in sql_query(sql):
        add_new.append({'ds': ds.strftime('%m-%d'), 'add_confirm': add_confirm, 'add_suspect': add_suspect})
        con_sus_serv.append({'ds': ds.strftime('%m-%d'), 'confirm': confirm, 'now_confirm': now_confirm,
                             'suspect': suspect, 'now_severe': now_severe})
        dead_heal.append({'ds': ds.strftime('%m-%d'), 'heal': heal, 'dead': dead})
        dead_heal_rate.append({'ds': ds.strftime('%m-%d'), 'heal_rate': heal_rate, 'dead_rate': dead_rate})
    data = [add_new, con_sus_serv, dead_heal, dead_heal_rate]
    print(data)
    return render_template('chinaTrend.html', data=data)


if __name__ == '__main__':
    app.run()
