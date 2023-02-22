import pandas as pd
import mysql.connector
from datetime import date, timedelta
import pickle

fs = 'subinfo.pkl'

def studenttAttendance_theory(roll,year,subject):
    at_btech = mysql.connector.connect(user='root', password='', host='localhost', database='theory_btech')
    at_ty = mysql.connector.connect(user='root', password='', host='localhost', database='theory_ty')
    at_sy = mysql.connector.connect(user='root', password='', host='localhost', database='theory_sy')

    btech = at_btech.cursor()
    ty = at_ty.cursor()
    sy = at_sy.cursor()

    total ={}

    if year == 'BTECH':
        attendance = {}
        try:
            sql = 'SELECT * FROM `{}` WHERE roll = "{}"'.format(subject,roll)
            btech.execute(sql)
            data = btech.fetchall()
            data = list(data[0][3:])
            sql = "SHOW COLUMNS FROM `{}`".format(subject)
            btech.execute(sql)
            col = btech.fetchall()
            column = []
            for k in col:
                column.append(k[0])
            column = column[3:]
            # print(data,column)
        except:
            print('except')
        
        for i in range(len(column)):
            if data[i] == 1:
                attendance[column[i]] = 'Present'
            elif data[i] == 0:
                attendance[column[i]] = 'Absent'
            else:
                pass
        total['col'] = []
        total['attendance'] = []

        for i,j in attendance.items():
            total['col'].append(i)
            total['attendance'].append(j)
    
    elif year == 'TY':
        attendance = {}
        try:
            sql = 'SELECT * FROM `{}` WHERE roll = "{}"'.format(subject,roll)
            ty.execute(sql)
            data = ty.fetchall()
            data = list(data[0][3:])
            sql = "SHOW COLUMNS FROM `{}`".format(subject)
            ty.execute(sql)
            col = ty.fetchall()
            column = []
            for k in col:
                column.append(k[0])
            column = column[3:]
            # print(data,column)
        except:
            print('except')
        
        for i in range(len(column)):
            if data[i] == 1:
                attendance[column[i]] = 'Present'
            elif data[i] == 0:
                attendance[column[i]] = 'Absent'
            else:
                pass
        total['col'] = []
        total['attendance'] = []

        for i,j in attendance.items():
            total['col'].append(i)
            total['attendance'].append(j)
    
    elif year == 'SY':
        attendance = {}
        try:
            sql = 'SELECT * FROM `{}` WHERE roll = "{}"'.format(subject,roll)
            sy.execute(sql)
            data = sy.fetchall()
            data = list(data[0][3:])
            sql = "SHOW COLUMNS FROM `{}`".format(subject)
            sy.execute(sql)
            col = sy.fetchall()
            column = []
            for k in col:
                column.append(k[0])
            column = column[3:]
            # print(data,column)
        except:
            print('except')
        
        for i in range(len(column)):
            if data[i] == 1:
                attendance[column[i]] = 'Present'
            elif data[i] == 0:
                attendance[column[i]] = 'Absent'
            else:
                pass
        total['col'] = []
        total['attendance'] = []

        for i,j in attendance.items():
            total['col'].append(i)
            total['attendance'].append(j)

    at_sy.close()
    at_ty.close()
    at_btech.close()
    print(total)
    return total
    
def studenttAttendance_practical(roll,year,subject):
    ap_btech = mysql.connector.connect(user='root', password='', host='localhost', database='practical_btech')
    ap_ty = mysql.connector.connect(user='root', password='', host='localhost', database='practical_ty')
    ap_sy = mysql.connector.connect(user='root', password='', host='localhost', database='practical_sy')
    btechP = ap_btech.cursor()
    tyP = ap_ty.cursor()
    syP = ap_sy.cursor()

    total ={}

    if year == 'BTECH':
        attendance = {}
        try:
            sql = 'SELECT * FROM `{}` WHERE roll = "{}"'.format(subject,roll)
            btechP.execute(sql)
            data = btechP.fetchall()
            data = list(data[0][4:])
            sql = "SHOW COLUMNS FROM `{}`".format(subject)
            btechP.execute(sql)
            col = btechP.fetchall()
            column = []
            for k in col:
                column.append(k[0])
            column = column[4:]
            # print(data,column)
        except:
            print('except')
        
        for i in range(len(column)):
            # print(data[i])
            if data[i] == 2:
                attendance[column[i]] = 'Present'
            elif data[i] == 0:
                attendance[column[i]] = 'Absent'
            else:
                pass
        total['col'] = []
        total['attendance'] = []

        for i,j in attendance.items():
            total['col'].append(i)
            total['attendance'].append(j)

    elif year == 'TY':
        attendance = {}
        try:
            sql = 'SELECT * FROM `{}` WHERE roll = "{}"'.format(subject,roll)
            tyP.execute(sql)
            data = tyP.fetchall()
            data = list(data[0][4:])
            sql = "SHOW COLUMNS FROM `{}`".format(subject)
            tyP.execute(sql)
            col = tyP.fetchall()
            column = []
            for k in col:
                column.append(k[0])
            column = column[4:]
            # print(data,column)
        except:
            print('except')
        
        for i in range(len(column)):
            # print(data[i])
            if data[i] == 2:
                attendance[column[i]] = 'Present'
            elif data[i] == 0:
                attendance[column[i]] = 'Absent'
            else:
                pass
        total['col'] = []
        total['attendance'] = []

        for i,j in attendance.items():
            total['col'].append(i)
            total['attendance'].append(j)
    
    elif year == 'SY':
        attendance = {}
        try:
            sql = 'SELECT * FROM `{}` WHERE roll = "{}"'.format(subject,roll)
            syP.execute(sql)
            data = syP.fetchall()
            data = list(data[0][4:])
            sql = "SHOW COLUMNS FROM `{}`".format(subject)
            syP.execute(sql)
            col = syP.fetchall()
            column = []
            for k in col:
                column.append(k[0])
            column = column[4:]
            # print(data,column)
        except:
            print('except')
        
        for i in range(len(column)):
            # print(data[i])
            if data[i] == 2:
                attendance[column[i]] = 'Present'
            elif data[i] == 0:
                attendance[column[i]] = 'Absent'
            else:
                pass
        total['col'] = []
        total['attendance'] = []

        for i,j in attendance.items():
            total['col'].append(i)
            total['attendance'].append(j)

    print(total)
    ap_sy.close()
    ap_ty.close()
    ap_btech.close()
    return total
