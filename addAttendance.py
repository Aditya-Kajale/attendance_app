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
        # BTECH Year --------------------------------------
        if data[0]=="BTECH":
            if data[4] == "Software Engineering":
                date = data[2].replace('-','_')
                try:
                    sql ='ALTER TABLE se ADD {} int DEFAULT 0'.format(date)
                    btech.execute(sql)
                    at_btech.commit()
                    sql = "UPDATE se SET {}=1 WHERE roll={} ".format(date,i)
                    btech.execute(sql)
                    at_btech.commit()
                except:
                    print('already exist')
                    for i in present:
                        print(i,date)
                        sql = "UPDATE se SET {}=1 WHERE roll={} ".format(date,i)
                        btech.execute(sql)
                        at_btech.commit()

            elif data[4] == "Big Data Analytics":
                date = data[2].replace('-','_')
                print(data[4])
                try:
                    sql ='ALTER TABLE bda ADD {} int DEFAULT 0'.format(date)
                    btech.execute(sql)
                    at_btech.commit()
                    sql = "UPDATE bda SET {}=1 WHERE roll={} ".format(date,i)
                    btech.execute(sql)
                    at_btech.commit()
                except:
                    print('already exist')
                    for i in present:
                        print(i,date)
                        sql = "UPDATE bda SET {}=1 WHERE roll={}".format(date,i)
                        btech.execute(sql)
                        at_btech.commit()
            
            elif data[4] == "Cloud Computing":
                date = data[2].replace('-','_')
                print(data[4])
                try:
                    sql ='ALTER TABLE cc ADD {} int DEFAULT 0'.format(date)
                    btech.execute(sql)
                    at_btech.commit()
                    sql = "UPDATE cc SET {}=1 WHERE roll={} ".format(date,i)
                    btech.execute(sql)
                    at_btech.commit()
                except:
                    print('already exist')
                    for i in present:
                        print(i,date)
                        sql = "UPDATE cc SET {}=1 WHERE roll={}".format(date,i)
                        btech.execute(sql)
                        at_btech.commit()

            elif data[4] == "Blockchain Technology":
                date = data[2].replace('-','_')
                print(data[4])
                try:
                    sql ='ALTER TABLE bt ADD {} int DEFAULT 0'.format(date)
                    btech.execute(sql)
                    at_btech.commit()
                    sql = "UPDATE bt SET {}=1 WHERE roll={} ".format(date,i)
                    btech.execute(sql)
                    at_btech.commit()
                except:
                    print('already exist')
                    for i in present:
                        print(i,date)
                        sql = "UPDATE bt SET {}=1 WHERE roll={}".format(date,i)
                        btech.execute(sql)
                        at_btech.commit()

            elif data[4] == "Full Stack Development":
                date = data[2].replace('-','_')
                print(data[4])
                try:
                    sql ='ALTER TABLE fsd ADD {} int DEFAULT 0'.format(date)
                    btech.execute(sql)
                    at_btech.commit()
                    sql = "UPDATE fsd SET {}=1 WHERE roll={} ".format(date,i)
                    btech.execute(sql)
                    at_btech.commit()
                except:
                    print('already exist')
                    for i in present:
                        print(i,date)
                        sql = "UPDATE fsd SET {}=1 WHERE roll={}".format(date,i)
                        btech.execute(sql)
                        at_btech.commit()

            elif data[4] == "System Administration":
                date = data[2].replace('-','_')
                print(data[4])
                try:
                    sql ='ALTER TABLE sa ADD {} int DEFAULT 0'.format(date)
                    btech.execute(sql)
                    at_btech.commit()
                    sql = "UPDATE sa SET {}=1 WHERE roll={} ".format(date,i)
                    btech.execute(sql)
                    at_btech.commit()
                except:
                    print('already exist')
                    for i in present:
                        print(i,date)
                        sql = "UPDATE sa SET {}=1 WHERE roll={}".format(date,i)
                        btech.execute(sql)
                        at_btech.commit()



