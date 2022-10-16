import pandas as pd
# import connection as cn
from routes import mysql_stud
import mysql.connector

at_btech = mysql.connector.connect(user='root', password='', host='localhost', database='theory_btech')
at_ty = mysql.connector.connect(user='root', password='', host='localhost', database='theory_ty')
at_sy = mysql.connector.connect(user='root', password='', host='localhost', database='theory_sy')
at_fy = mysql.connector.connect(user='root', password='', host='localhost', database='theory_fy')

btech = at_btech.cursor()
ty = at_ty.cursor()
sy = at_sy.cursor()
fy = at_fy.cursor()

def addAttendance(data,present): 
    print(data,present)
    if data[3]=='Theory':
        if data[0]=="BTECH":
            if data[4] == "Software Engineering":
                aditya = data[2].replace('-','_')
                print(aditya)
                try:
                    sql ='ALTER TABLE se ADD {} int DEFAULT 0'.format(aditya)
                    btech.execute(sql)
                    at_btech.commit()
                    sql = "UPDATE se SET {}=1 WHERE roll={} ".format(aditya,i)
                    btech.execute(sql)
                    at_btech.commit()
                except:
                    print('already exist')
                    for i in present:
                        print(i,aditya)
                        sql = "UPDATE se SET {}=1 WHERE roll={} ".format(aditya,i)
                        btech.execute(sql)
                        at_btech.commit()
