import pandas as pd
# import connection as cn
from routes import mysql_stud
import mysql.connector


def deletteFromDailyReport(year, division, date, subject, torp, roll):
    print('in daily')
    dcse = mysql.connector.connect(
        user='root', password='', host='localhost', database='daily_cse')
    dcse_cur = dcse.cursor()

    tableName = date+'-'+year+'-'+division
    sub = subject.split()
    sname = ''
    for i in sub:
        if i[0] == '(':
            sname += i[1]+i[2]
        else:
            sname += i[0]

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
        print(col)
        if torp == "Theory":
            for i in range(len(col)):
                if sname in col[i]:
                    ind = i

            for i in roll:
                sql = "UPDATE `{}` SET `{}`=-1 WHERE roll={}".format(
                    tableName, col[ind], i)
                dcse_cur.execute(sql)
                dcse.commit()

        elif torp == "Practical":
            # print('in practical')
            for i in range(len(col)):
                if 'pr' in col[i]:
                    ind = i
            indnext = ind+1

            for i in roll:
                sql = "UPDATE `{}` SET `{}`=-1 WHERE roll={}".format(
                    tableName, col[ind], i)
                dcse_cur.execute(sql)
                dcse.commit()
                sql = "UPDATE `{}` SET `{}`=-1 WHERE roll={}".format(
                    tableName, col[indnext], i)
                dcse_cur.execute(sql)
                dcse.commit()
                sql = "UPDATE `{}` SET `prsub`='' WHERE roll={}".format(
                    tableName, i)
                dcse_cur.execute(sql)
                dcse.commit()


def deleteAttendanceTheory(year, division, date, subject, batch, torp):
    at_btech = mysql.connector.connect(
        user='root', password='', host='localhost', database='theory_btech')
    at_ty = mysql.connector.connect(
        user='root', password='', host='localhost', database='theory_ty')
    at_sy = mysql.connector.connect(
        user='root', password='', host='localhost', database='theory_sy')

    btech = at_btech.cursor()
    ty = at_ty.cursor()
    sy = at_sy.cursor()
    cur = mysql_stud.connection.cursor()

    date = date.replace('-', '_')

    if year == "BTECH":

        roll = []
        try:
            for i in batch:
                sql = "SELECT ROLL_NO from `{}` WHERE batch='{}'".format(
                    year, i)
                cur.execute(sql)
                temp = cur.fetchall()
                for k in temp:
                    roll.append(k[0])

            for i in roll:
                sql = "UPDATE `{}` SET {}=-1 WHERE roll={}".format(
                    subject, date, i)
                btech.execute(sql)
                at_btech.commit()
        except:
            print('something wrong with date ')

        date = date.replace('_', '-')
        deletteFromDailyReport(year, division, date, subject, torp, roll)


def deleteAttendancePractical(year, division, date, subject, timeslot, batch, torp):
    ap_btech = mysql.connector.connect(
        user='root', password='', host='localhost', database='practical_btech')
    ap_ty = mysql.connector.connect(
        user='root', password='', host='localhost', database='practical_ty')
    ap_sy = mysql.connector.connect(
        user='root', password='', host='localhost', database='practical_sy')

    btechP = ap_btech.cursor()
    tyP = ap_ty.cursor()
    syP = ap_sy.cursor()
    cur = mysql_stud.connection.cursor()

    date = date.replace('-', '_')

    if year == "BTECH":
        roll = []
        roll = []
        try:
            for i in batch:
                sql = "SELECT ROLL_NO from `{}` WHERE batch='{}'".format(
                    year, i)
                cur.execute(sql)
                temp = cur.fetchall()
                for k in temp:
                    roll.append(k[0])
            print(roll)
            for i in roll:
                sql = "UPDATE `{}` SET {}=-1 WHERE roll={}".format(
                    subject, date, i)
                btechP.execute(sql)
                ap_btech.commit()
        except:
            print('something wrong with date ')

        date = date.replace('_', '-')
        deletteFromDailyReport(year, division, date, subject, torp, roll)
