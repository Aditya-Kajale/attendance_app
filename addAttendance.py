import pandas as pd
# import connection as cn
from routes import mysql_stud
import mysql.connector


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
    
    elif data[0] == "TY":
        date = data[2].replace('-','_')
        try:
            for i in roll:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(data[3],date,i)
                ty.execute(sql)
                at_ty.commit()

            for i in present:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=1 WHERE roll={} ".format(data[3],date,i)
                ty.execute(sql)
                at_ty.commit()
            
        except:
            print('already exist')
            
            sql ='ALTER TABLE `{}` ADD {} int DEFAULT -1'.format(data[3],date)
            ty.execute(sql)
            at_ty.commit()

            for i in roll:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(data[3],date,i)
                ty.execute(sql)
                at_ty.commit()

            for i in present:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=1 WHERE roll={} ".format(data[3],date,i)
                ty.execute(sql)
                at_ty.commit()
        at_ty.close()
    
    elif data[0] == "SY":
        date = data[2].replace('-','_')
        try:
            for i in roll:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(data[3],date,i)
                sy.execute(sql)
                at_sy.commit()

            for i in present:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=1 WHERE roll={} ".format(data[3],date,i)
                sy.execute(sql)
                at_sy.commit()
            
        except:
            print('already exist')
            
            sql ='ALTER TABLE `{}` ADD {} int DEFAULT -1'.format(data[3],date)
            sy.execute(sql)
            at_sy.commit()

            for i in roll:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(data[3],date,i)
                sy.execute(sql)
                at_sy.commit()

            for i in present:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=1 WHERE roll={} ".format(data[3],date,i)
                sy.execute(sql)
                at_sy.commit()
        at_sy.close()

    elif data[0] == "FY":
        date = data[2].replace('-','_')
        try:
            for i in roll:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(data[3],date,i)
                fy.execute(sql)
                at_fy.commit()

            for i in present:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=1 WHERE roll={} ".format(data[3],date,i)
                fy.execute(sql)
                at_fy.commit()
            
        except:
            print('already exist')
            
            sql ='ALTER TABLE `{}` ADD {} int DEFAULT -1'.format(data[3],date)
            fy.execute(sql)
            at_fy.commit()

            for i in roll:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(data[3],date,i)
                fy.execute(sql)
                at_fy.commit()

            for i in present:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=1 WHERE roll={} ".format(data[3],date,i)
                fy.execute(sql)
                at_fy.commit()
        at_fy.close()


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
    
    elif data[0] == "TY":
        date = data[2].replace('-','_')
        print(date)
        try:
            for i in roll:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(data[3],date,i)
                tyP.execute(sql)
                ap_ty.commit()

            for i in present:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=2 WHERE roll={} ".format(data[3],date,i)
                tyP.execute(sql)
                ap_ty.commit()
            
        except:
            print('already exist')
            
            sql ='ALTER TABLE `{}` ADD {} int DEFAULT -1'.format(data[3],date)
            tyP.execute(sql)
            ap_ty.commit()

            for i in roll:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(data[3],date,i)
                tyP.execute(sql)
                ap_ty.commit()

            for i in present:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=2 WHERE roll={} ".format(data[3],date,i)
                tyP.execute(sql)
                ap_ty.commit()
        ap_ty.close()
    
    elif data[0] == "SY":
        date = data[2].replace('-','_')
        print(date)
        try:
            for i in roll:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(data[3],date,i)
                syP.execute(sql)
                ap_sy.commit()

            for i in present:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=2 WHERE roll={} ".format(data[3],date,i)
                syP.execute(sql)
                ap_sy.commit()
            
        except:
            print('already exist')
            
            sql ='ALTER TABLE `{}` ADD {} int DEFAULT -1'.format(data[3],date)
            syP.execute(sql)
            ap_sy.commit()

            for i in roll:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(data[3],date,i)
                syP.execute(sql)
                ap_sy.commit()

            for i in present:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=2 WHERE roll={} ".format(data[3],date,i)
                syP.execute(sql)
                ap_sy.commit()
        ap_sy.close()
    
    elif data[0] == "FY":
        date = data[2].replace('-','_')
        print(date)
        try:
            for i in roll:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(data[3],date,i)
                fyP.execute(sql)
                ap_fy.commit()

            for i in present:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=2 WHERE roll={} ".format(data[3],date,i)
                fyP.execute(sql)
                ap_fy.commit()
            
        except:
            print('already exist')
            
            sql ='ALTER TABLE `{}` ADD {} int DEFAULT -1'.format(data[3],date)
            fyP.execute(sql)
            ap_fy.commit()

            for i in roll:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(data[3],date,i)
                fyP.execute(sql)
                ap_fy.commit()

            for i in present:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=2 WHERE roll={} ".format(data[3],date,i)
                fyP.execute(sql)
                ap_fy.commit()
        ap_fy.close()