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

def addAttendance(data,present,roll): 
    # print(data,present)

    if data[3]=='Theory':
        # BTECH Year --------------------------------------
        if data[0]=="BTECH":
            date = data[2].replace('-','_')
            try:
                for i in roll:
                    # print(i,date)
                    # print(data[4])
                    sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(data[4],date,i)
                    btech.execute(sql)
                    at_btech.commit()

                for i in present:
                    # print(i,date)
                    # print(data[4])
                    sql = "UPDATE `{}` SET {}=1 WHERE roll={} ".format(data[4],date,i)
                    btech.execute(sql)
                    at_btech.commit()
                
            except:
                print('already exist')
                
                sql ='ALTER TABLE `{}` ADD {} int DEFAULT -1'.format(data[4],date)
                btech.execute(sql)
                at_btech.commit()

                for i in roll:
                    # print(i,date)
                    # print(data[4])
                    sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(data[4],date,i)
                    btech.execute(sql)
                    at_btech.commit()

                for i in present:
                    # print(i,date)
                    # print(data[4])
                    sql = "UPDATE `{}` SET {}=1 WHERE roll={} ".format(data[4],date,i)
                    btech.execute(sql)
                    at_btech.commit()


    elif data[3]=='Practical':
        print('Practical attendance part')

