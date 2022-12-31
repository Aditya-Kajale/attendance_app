import pandas as pd
import mysql.connector
from routes import mysql_stud
import pickle

at_btech = mysql.connector.connect(user='root', password='', host='localhost', database='theory_btech')
at_ty = mysql.connector.connect(user='root', password='', host='localhost', database='theory_ty')
at_sy = mysql.connector.connect(user='root', password='', host='localhost', database='theory_sy')
at_fy = mysql.connector.connect(user='root', password='', host='localhost', database='theory_fy')

btech = at_btech.cursor()
ty = at_ty.cursor()
sy = at_sy.cursor()
fy = at_fy.cursor()

def getData(year,division):
    cur = mysql_stud.connection.cursor()
    sql = "SELECT * FROM "+year+" WHERE DIVISION = %s"
    # print(year,division)
    val = (division)
    cur.execute(sql,val)
    data = cur.fetchall()
    mysql_stud.connection.commit()

    return data

def getData_batchvise(year,division,batch):
    cur = mysql_stud.connection.cursor()
    data = []
    for i in batch:
        sql = "SELECT * FROM "+year+" WHERE DIVISION = %s AND BATCH = %s"
        val = (division,i)
        cur.execute(sql,val)
        temp = cur.fetchall()
        for j in temp:
            data.append(j)
    mysql_stud.connection.commit()
    return data

def delete_data(year,division):
    # delete from student database
    cur = mysql_stud.connection.cursor()
    sql = "DELETE FROM "+year+" WHERE DIVISION = %s"
    val = (division)
    cur.execute(sql,val)
    mysql_stud.connection.commit()



