import pandas as pd
# import connection as cn
from routes import mysql_stud
import mysql.connector


ap_btech = mysql.connector.connect(user='root', password='', host='localhost', database='practical_btech')
ap_ty = mysql.connector.connect(user='root', password='', host='localhost', database='practical_ty')
ap_sy = mysql.connector.connect(user='root', password='', host='localhost', database='practical_sy')
ap_fy = mysql.connector.connect(user='root', password='', host='localhost', database='practical_fy')

btechP = ap_btech.cursor()
tyP = ap_ty.cursor()
syP = ap_sy.cursor()
fyP = ap_fy.cursor()

def addAttendance_theory(data,present,roll): 
    at_btech = mysql.connector.connect(user='root', password='', host='localhost', database='theory_btech')
    at_ty = mysql.connector.connect(user='root', password='', host='localhost', database='theory_ty')
    at_sy = mysql.connector.connect(user='root', password='', host='localhost', database='theory_sy')
    at_fy = mysql.connector.connect(user='root', password='', host='localhost', database='theory_fy')

    btech = at_btech.cursor()
    ty = at_ty.cursor()
    sy = at_sy.cursor()
    fy = at_fy.cursor()

    # print(data,present)
    if data[0]=="BTECH":
        date = data[2].replace('-','_')
        try:
            for i in roll:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(data[3],date,i)
                btech.execute(sql)
                at_btech.commit()

            for i in present:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=1 WHERE roll={} ".format(data[3],date,i)
                btech.execute(sql)
                at_btech.commit()
            
        except:
            print('already exist')
            
            sql ='ALTER TABLE `{}` ADD {} int DEFAULT -1'.format(data[3],date)
            btech.execute(sql)
            at_btech.commit()

            for i in roll:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(data[3],date,i)
                btech.execute(sql)
                at_btech.commit()

            for i in present:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=1 WHERE roll={} ".format(data[3],date,i)
                btech.execute(sql)
                at_btech.commit()
        at_btech.close()


def addAttendance_practical(data,present,roll): 
    ap_btech = mysql.connector.connect(user='root', password='', host='localhost', database='practical_btech')
    ap_ty = mysql.connector.connect(user='root', password='', host='localhost', database='practical_ty')
    ap_sy = mysql.connector.connect(user='root', password='', host='localhost', database='practical_sy')
    ap_fy = mysql.connector.connect(user='root', password='', host='localhost', database='practical_fy')

    btechP = ap_btech.cursor()
    tyP = ap_ty.cursor()
    syP = ap_sy.cursor()
    fyP = ap_fy.cursor()

    if data[0]=="BTECH":
        date = data[2].replace('-','_')
        print(date)
        try:
            for i in roll:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(data[3],date,i)
                btechP.execute(sql)
                ap_btech.commit()

            for i in present:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=2 WHERE roll={} ".format(data[3],date,i)
                btechP.execute(sql)
                ap_btech.commit()
            
        except:
            print('already exist')
            
            sql ='ALTER TABLE `{}` ADD {} int DEFAULT -1'.format(data[3],date)
            btechP.execute(sql)
            ap_btech.commit()

            for i in roll:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(data[3],date,i)
                btechP.execute(sql)
                ap_btech.commit()

            for i in present:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=2 WHERE roll={} ".format(data[3],date,i)
                btechP.execute(sql)
                ap_btech.commit()
        ap_btech.close()