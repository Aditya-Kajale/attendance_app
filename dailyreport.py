import pandas as pd
# import connection as cn
from routes import mysql_stud
import mysql.connector


def dailyreport(year, div, date):
    cur = mysql_stud.connection.cursor()
    dcse = mysql.connector.connect(
        user='root', password='', host='localhost', database='daily_cse')
    dcse_cur = dcse.cursor()
    total = {}
    total['default'] = [year, div, date]
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
        print(prcount, abcount)
        prcount = prcount - abcount
        total['pr'] = [prcount, abcount]

        sql = "SELECT sphone,pphone FROM `{}`".format(year)
        cur.execute(sql)
        phone = cur.fetchall()

        total['columns'].insert(9, 'Student Phone')
        total['columns'].insert(9, 'Parent Phone')

        for i in range(len(total['data'])):
            total['data'][i] = list(total['data'][i])
            total['data'][i].insert(9, phone[i][1])
            total['data'][i].insert(9, phone[i][0])

        total['len'] = len(data[0])-1

    except:
        print('table not exist')

    return total


def updatedailyreport(info, remark):
    cur = mysql_stud.connection.cursor()
    dcse = mysql.connector.connect(
        user='root', password='', host='localhost', database='daily_cse')
    dcse_cur = dcse.cursor()

    year = info[0]
    div = info[1]
    date = info[2]
    tableName = date+'-'+year+'-'+div

    sql = 'SELECT ROLL_NO FROM {}'.format(info[0])
    cur.execute(sql)
    temp = cur.fetchall()
    roll = []
    for i in temp:
        roll.append(i[0])

    try:
        for i in range(len(roll)):
            print(remark[i], roll[i])
            sql = "UPDATE `{}` SET remark='{}' WHERE `roll`='%s'".format(
                tableName, remark[i])
            val = (roll[i],)
            dcse_cur.execute(sql, val)
            dcse.commit()
    except:
        print('table not exist')

    print(remark, info, roll)
    dcse.close()


def check_session(year, division, date, timeslot):
    cur = mysql_stud.connection.cursor()
    dcse = mysql.connector.connect(
        user='root', password='', host='localhost', database='daily_cse')
    dcse_cur = dcse.cursor()
    msg = ''
    tableName = date+'-'+year+'-'+division

    sql = "SHOW TABLES LIKE '%{}%'".format(tableName)
    dcse_cur.execute(sql)
    table_exist = dcse_cur.fetchall()

    if table_exist:
        sql = "SHOW COLUMNS FROM `{}`".format(tableName)
        dcse_cur.execute(sql)
        cn = dcse_cur.fetchall()
        col = []
        for kk in cn:
            col.append(kk[0])

        # print(col[ind-1])
        try:
            ind = col.index(timeslot)
        except:
            pass

        try:
            if timeslot not in col:
                msg = 'Attendance for this time slot is recorded already.'
            else:
                if 'pr' in col[ind-1]:
                    msg = 'Attendance for this time slot is recorded already'
            # print(col[ind-1])
        except:
            pass

    return msg


def check_session_practical(year, division, date, batch, timeslot):
    cur = mysql_stud.connection.cursor()
    dcse = mysql.connector.connect(
        user='root', password='', host='localhost', database='daily_cse')
    dcse_cur = dcse.cursor()
    msg = ''
    tableName = date+'-'+year+'-'+division
    batch = batch[0]
    sql = "SHOW TABLES LIKE '%{}%'".format(tableName)
    dcse_cur.execute(sql)
    table_exist = dcse_cur.fetchall()

    if table_exist:
        sql = "SHOW COLUMNS FROM `{}`".format(tableName)
        dcse_cur.execute(sql)
        cn = dcse_cur.fetchall()
        col = []
        for kk in cn:
            col.append(kk[0])

        tt = {'10:15': 3,
              '11:15': 4,
              '1:15': 5,
              '2:15': 6,
              '3:30': 7,
              '4:30': 8}

        print(col[tt[timeslot]])

        try:
            if timeslot not in col:
                msg = 'Attendance for this batch or time slot is already recorded'
                sql = 'SELECT ROLL_NO FROM `{}` WHERE batch = "{}"'.format(
                    year, batch)
                cur.execute(sql)
                temp = cur.fetchall()

                sql = "SELECT prsub FROM `{}` WHERE roll = '{}'".format(
                    tableName, temp[0][0])
                dcse_cur.execute(sql)
                res = dcse_cur.fetchall()
                print(res)
                if 'pr' in col[tt[timeslot]]:
                    if res[0][0] == '':
                        msg = ''
                    else:
                        msg = 'Attendance for this time slot is recorded already'
            else:
                if col[tt[timeslot]+1] not in tt:
                    msg = 'Attendance for this time slot is recorded already'

            # print(col[ind-1])
        except:
            pass

    return msg
