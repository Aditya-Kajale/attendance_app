import pandas as pd
from routes import mysql_stud

def addstud(roll,name,prn,year,division):
    cur = mysql_stud.connection.cursor()
    sql = "INSERT INTO "+ year +" (ROLL_NO, NAME, PRN, YEAR, DIVISION) VALUES (%s, %s, %s, %s, %s)"
    value = (roll,name,prn,year,division)
    cur.execute(sql, value)
    mysql_stud.connection.commit()
