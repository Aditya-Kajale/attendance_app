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

def addInSubject(roll,year,div):
   subs_btech = ['bda','bt','cc','fsd','sa','se']
   print(subs_btech)
   print(year)
   if year=="BTECH":
      for i in subs_btech:
         sql = "INSERT INTO "+i+" (roll,division) VALUES (%s,%s)"
         values = (str(roll),div)
         btech.execute(sql,values)
         at_btech.commit()
      

def parseCSV(filePath,year,div):
   cur = mysql_stud.connection.cursor()
   # print(cur)
   col_names = ['roll','name','prn']
   csvData = pd.read_csv(filePath,names=col_names, header=None)

   for i,row in csvData.iterrows():
      sql = "INSERT INTO "+ year +" (ROLL_NO, NAME, PRN, YEAR, DIVISION) VALUES (%s, %s, %s, %s, %s)"
      value = (row['roll'],row['name'],row['prn'],year,div)
      cur.execute(sql, value)
      mysql_stud.connection.commit()
      addInSubject(row['roll'],year,div)


   

      






