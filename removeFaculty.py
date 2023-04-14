
import pandas as pd
import mysql.connector
from routes import mysql_stud
import pickle


def removeFaculty(fc, id):
    logindbs = mysql.connector.connect(
        user='root', password='', host='localhost', database='login')
    lo_cur = logindbs.cursor()
    sql = "DELETE FROM `account` WHERE `id` = {}".format(id)
    lo_cur.execute(sql)

    logindbs.commit()
    logindbs.close()
