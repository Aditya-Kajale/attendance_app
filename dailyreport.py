import pandas as pd
# import connection as cn
from routes import mysql_stud
import mysql.connector


def dailyreport(year,div,date):
    cur = mysql_stud.connection.cursor()
    dcse = mysql.connector.connect(user='root', password='', host='localhost', database='daily_cse')
    dcse_cur = dcse.cursor()
    total = {}
    total['default'] = [year,div,date]
    tableName = date+'-'+year+'-'+div

    try:
        sql = "SHOW COLUMNS FROM `{}`".format(tableName)
        dcse_cur.execute(sql)
        cn = dcse_cur.fetchall()
        col = []
        for kk in cn:
            col.append(kk[0])
        total['columns'] = col
        sql = 'SELECT * FROM `{}`'.format(tableName)
        dcse_cur.execute(sql)
        data = dcse_cur.fetchall()
        total['data'] = data

        abcount = 0
        prcount = 0
        for i in total['data']:
            if 0 in i:
                abcount += 1
            if 2 or 1 in i:
                prcount += 1
        print(prcount,abcount)
        prcount = prcount -abcount
        total['pr'] = [prcount,abcount]

        sql = "SELECT sphone,pphone FROM `{}`".format(year)
        cur.execute(sql)
        phone = cur.fetchall()
        
        total['columns'].insert(9,'Student Phone')
        total['columns'].insert(9,'Parent Phone')
        
        for i in range(len(total['data'])):
            total['data'][i] = list(total['data'][i])
            total['data'][i].insert(9,phone[i][1])
            total['data'][i].insert(9,phone[i][0])

        total['len'] = len(data[0])-1

    except:
        print('table not exist')

    return total

def updatedailyreport(info,remark):
    cur = mysql_stud.connection.cursor()
    dcse = mysql.connector.connect(user='root', password='', host='localhost', database='daily_cse')
    dcse_cur = dcse.cursor()

    year = info[0]
    div = info[1]
    date = info[2]
    tableName = date+'-'+year+'-'+div

    sql = 'SELECT ROLL_NO FROM {}'.format(info[0])
    cur.execute(sql)
    temp = cur.fetchall()
    roll = []
    for i in temp :
        roll.append(i[0])

    try:
        for i in range(len(roll)):
            print(remark[i],roll[i])
            sql = "UPDATE `{}` SET remark='{}' WHERE `roll`='%s'".format(tableName,remark[i])
            val = (roll[i],)
            dcse_cur.execute(sql,val)
            dcse.commit()
    except:
        print('table not exist')

    print(remark,info,roll)
    dcse.close()
