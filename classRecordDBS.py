import pandas as pd
import mysql.connector
from routes import mysql_stud


def getData(year,division):
    cur = mysql_stud.connection.cursor()
    sql = "SELECT * FROM "+year+" WHERE DIVISION = %s"
    # print(year,division)
    val = (division)
    cur.execute(sql,val)
    data = cur.fetchall()
    mysql_stud.connection.commit()

    return data

