import pandas as pd
import mysql.connector
from routes import mysql_stud
import pickle


def get_attendance(year, data, subject, date):
    at_btech = mysql.connector.connect(
        user='root', password='root@123', host='localhost', database='theory_btech')
    at_ty = mysql.connector.connect(
        user='root', password='root@123', host='localhost', database='theory_ty')
    at_sy = mysql.connector.connect(
        user='root', password='root@123', host='localhost', database='theory_sy')

    btech = at_btech.cursor()
    ty = at_ty.cursor()
    sy = at_sy.cursor()

    date = date.replace('-', '_')
    roll = [i[0] for i in data]
    lc = []
    if year == 'BTECH':
        for i in roll:
            try:
                sql = "SELECT `{}` FROM `{}` WHERE `roll`='{}'".format(
                    date, subject, i)
                btech.execute(sql)
                cc = btech.fetchall()
                lc.append(cc[0][0])
            except Exception as e:
                print(e)

    elif year == 'TY':
        for i in roll:
            try:
                sql = "SELECT `{}` FROM `{}` WHERE `roll`='{}'".format(
                    date, subject, i)
                ty.execute(sql)
                cc = ty.fetchall()
                lc.append(cc[0][0])
            except Exception as e:
                print(e)

    elif year == 'SY':
        for i in roll:
            try:
                sql = "SELECT `{}` FROM `{}` WHERE `roll`='{}'".format(
                    date, subject, i)
                sy.execute(sql)
                cc = sy.fetchall()
                lc.append(cc[0][0])
            except Exception as e:
                print(e)

    at_btech.close()
    at_ty.close()
    at_sy.close()
    return lc


def get_practicalAttendance(year, data, subject, date):
    ap_btech = mysql.connector.connect(
        user='root', password='root@123', host='localhost', database='practical_btech')
    ap_ty = mysql.connector.connect(
        user='root', password='root@123', host='localhost', database='practical_ty')
    ap_sy = mysql.connector.connect(
        user='root', password='root@123', host='localhost', database='practical_sy')

    btechP = ap_btech.cursor()
    tyP = ap_ty.cursor()
    syP = ap_sy.cursor()
    date = date.replace('-', '_')
    roll = [i[0] for i in data]

    lc = []
    if year == 'BTECH':
        for i in roll:
            try:
                sql = "SELECT `{}` FROM `{}` WHERE `roll`='{}'".format(
                    date, subject, i)
                btechP.execute(sql)
                cc = btechP.fetchall()
                lc.append(cc[0][0])
            except Exception as e:
                print(e)

    elif year == 'TY':
        for i in roll:
            try:
                sql = "SELECT `{}` FROM `{}` WHERE `roll`='{}'".format(
                    date, subject, i)
                tyP.execute(sql)
                cc = tyP.fetchall()
                lc.append(cc[0][0])
            except Exception as e:
                print(e)

    elif year == 'SY':
        for i in roll:
            try:
                sql = "SELECT `{}` FROM `{}` WHERE `roll`='{}'".format(
                    date, subject, i)
                syP.execute(sql)
                cc = syP.fetchall()
                lc.append(cc[0][0])
            except Exception as e:
                print(e)
    ap_btech.close()
    ap_ty.close()
    ap_sy.close()

    return lc


def editattendance(present, data):
    at_btech = mysql.connector.connect(
        user='root', password='root@123', host='localhost', database='theory_btech')
    at_ty = mysql.connector.connect(
        user='root', password='root@123', host='localhost', database='theory_ty')
    at_sy = mysql.connector.connect(
        user='root', password='root@123', host='localhost', database='theory_sy')

    btech = at_btech.cursor()
    ty = at_ty.cursor()
    sy = at_sy.cursor()

    year = data[0]
    division = data[1]
    date = data[2]
    subject = data[3]
    date = date.replace('-', '_')

    if year == 'BTECH':
        for i in range(len(present)):
            sql = "UPDATE `{}` SET `{}`='{}' WHERE `roll`='{}'".format(
                subject, date, present[i], data[5][i])
            btech.execute(sql)
            at_btech.commit()

    elif year == 'TY':
        for i in range(len(present)):
            sql = "UPDATE `{}` SET `{}`='{}' WHERE `roll`='{}'".format(
                subject, date, present[i], data[5][i])
            ty.execute(sql)
            at_ty.commit()

    elif year == 'SY':
        for i in range(len(present)):
            sql = "UPDATE `{}` SET `{}`='{}' WHERE `roll`='{}'".format(
                subject, date, present[i], data[5][i])
            sy.execute(sql)
            at_sy.commit()

    at_btech.close()
    at_ty.close()
    at_sy.close()


def editattendancePractical(present, data):
    ap_btech = mysql.connector.connect(
        user='root', password='root@123', host='localhost', database='practical_btech')
    ap_ty = mysql.connector.connect(
        user='root', password='root@123', host='localhost', database='practical_ty')
    ap_sy = mysql.connector.connect(
        user='root', password='root@123', host='localhost', database='practical_sy')

    btechP = ap_btech.cursor()
    tyP = ap_ty.cursor()
    syP = ap_sy.cursor()

    year = data[0]
    division = data[1]
    date = data[2]
    subject = data[3]
    date = date.replace('-', '_')

    if year == 'BTECH':
        for i in range(len(present)):
            sql = "UPDATE `{}` SET `{}`='{}' WHERE `roll`='{}'".format(
                subject, date, present[i], data[5][i])
            btechP.execute(sql)
            ap_btech.commit()

    elif year == 'TY':
        for i in range(len(present)):
            sql = "UPDATE `{}` SET `{}`='{}' WHERE `roll`='{}'".format(
                subject, date, present[i], data[5][i])
            tyP.execute(sql)
            ap_ty.commit()

    elif year == 'SY':
        for i in range(len(present)):
            sql = "UPDATE `{}` SET `{}`='{}' WHERE `roll`='{}'".format(
                subject, date, present[i], data[5][i])
            syP.execute(sql)
            ap_sy.commit()

    ap_btech.close()
    ap_sy.close()
    ap_ty.close()
