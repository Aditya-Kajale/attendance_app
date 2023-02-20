import pandas as pd
import mysql.connector
from routes import mysql_stud
import pickle

fs = 'subinfo.pkl'
fsub = open(fs,'rb')
subs = pickle.load(fsub)


def cleanfromsubs(year):
    at_btech = mysql.connector.connect(user='root', password='', host='localhost', database='theory_btech')
    at_ty = mysql.connector.connect(user='root', password='', host='localhost', database='theory_ty')
    at_sy = mysql.connector.connect(user='root', password='', host='localhost', database='theory_sy')
    btech = at_btech.cursor()
    ty = at_ty.cursor()
    sy = at_sy.cursor()

    ap_btech = mysql.connector.connect(user='root', password='', host='localhost', database='practical_btech')
    ap_ty = mysql.connector.connect(user='root', password='', host='localhost', database='practical_ty')
    ap_sy = mysql.connector.connect(user='root', password='', host='localhost', database='practical_sy')
    btechP = ap_btech.cursor()
    tyP = ap_ty.cursor()
    syP = ap_sy.cursor()
    print('in clean from sub')

    if year == 'BTECH':
        tableT = []
        tableP = []
        for i in subs['Theory'][year]:
            tableT.append(i)
        for i in subs['Practical'][year]:
            tableP.append(i)
        
        # for theory ---------------------------------------------------
        for i in tableT:
            sql = "SHOW COLUMNS FROM `{}`".format(i)
            btech.execute(sql)
            col = btech.fetchall()
            column = []
            for k in col:
                column.append(k[0])
            column = column[3:]
            for j in column:
                sql = "ALTER TABLE `{}` DROP `{}`".format(i,j)
                btech.execute(sql)

            sql = "TRUNCATE `{}`".format(i)
            btech.execute(sql)
        
        
        # for practical ------------------------------------------------
        for i in tableP:
            sql = "SHOW COLUMNS FROM `{}`".format(i)
            btechP.execute(sql)
            col = btechP.fetchall()
            column = []
            for k in col:
                column.append(k[0])
            column = column[3:]
            for j in column:
                sql = "ALTER TABLE `{}` DROP `{}`".format(i,j)
                btechP.execute(sql)
            
            sql = "TRUNCATE `{}`".format(i)
            btechP.execute(sql)
        
def cleandata(year):
    cur = mysql_stud.connection.cursor()
    sql = "DELETE FROM {}".format(year)
    cur.execute(sql)
    mysql_stud.connection.commit()
    cleanfromsubs(year)
    