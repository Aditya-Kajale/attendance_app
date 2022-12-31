import pandas as pd
from routes import mysql_stud
import mysql.connector
import pickle

at_btech = mysql.connector.connect(user='root', password='', host='localhost', database='theory_btech')
at_ty = mysql.connector.connect(user='root', password='', host='localhost', database='theory_ty')
at_sy = mysql.connector.connect(user='root', password='', host='localhost', database='theory_sy')
at_fy = mysql.connector.connect(user='root', password='', host='localhost', database='theory_fy')

btech = at_btech.cursor()
ty = at_ty.cursor()
sy = at_sy.cursor()
fy = at_fy.cursor()
fs = 'subinfo.pkl'

def addInSubject(roll,name,prn,year,div):
   fsub = open(fs,'rb')
   subs_btech = pickle.load(fsub)
   # print(year)
   if year == "BTECH":
      for i in subs_btech[year]:
         sql = "INSERT INTO "+"`"+i+"`"+" (roll,name,prn,division) VALUES (%s,%s,%s,%s)"
         values = (str(roll),name,prn,div)
         btech.execute(sql,values)
         at_btech.commit()
    

def addstud(roll,name,prn,year,division,batch):
   try:
      cur = mysql_stud.connection.cursor()
      sql = "INSERT INTO "+ year +" (ROLL_NO, NAME, PRN, YEAR, DIVISION, BATCH) VALUES (%s, %s, %s, %s, %s, %s)"
      value = (roll,name,prn,year,division,batch)
      cur.execute(sql, value)
      mysql_stud.connection.commit()
      print(batch)
      addInSubject(roll,name,prn,year,division)
   except:
      print('PRN already exist')

