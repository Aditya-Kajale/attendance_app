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

def addInSubject(roll,name,year,div):
   subs_btech = ['bda','bt','cc','fsd','sa','se']
   # print(subs_btech)
   # print(year)
   if year=="BTECH":
      for i in subs_btech:
         sql = "INSERT INTO "+i+" (roll,name,division) VALUES (%s,%s,%s)"
         values = (str(roll),name,div)
         btech.execute(sql,values)
         at_btech.commit()
      

def parseCSV(filePath,year,div,batchlength):
   batch_a = ['A1','A2','A3','A4','A5']
   batch_b = ['B1','B2','B3','B4','B5']
   cur = mysql_stud.connection.cursor()
   # print(cur)
   col_names = ['roll','name','prn']
   csvData = pd.read_csv(filePath,names=col_names, header=None)

   if div == 'A':
      count = 0
      ind = 0
      for i,row in csvData.iterrows():
         if count == int(batchlength):
            count = 0
            ind+=1
         print(count,batch_a[ind],batchlength)
         sql = "INSERT INTO "+ year +" (ROLL_NO, NAME, PRN, YEAR, DIVISION, BATCH) VALUES (%s, %s, %s, %s, %s, %s)"
         value = (row['roll'],row['name'],row['prn'],year,div,batch_a[ind])
         cur.execute(sql, value)
         mysql_stud.connection.commit()
         addInSubject(row['roll'],row['name'],year,div)
         count +=1
            
   if div == 'B':
      count = 0
      ind = 0
      for i,row in csvData.iterrows():
         if count == int(batchlength):
            count = 0
            ind+=1
         print(count,batch_b[ind],batchlength)
         sql = "INSERT INTO "+ year +" (ROLL_NO, NAME, PRN, YEAR, DIVISION, BATCH) VALUES (%s, %s, %s, %s, %s, %s)"
         value = (row['roll'],row['name'],row['prn'],year,div,batch_b[ind])
         cur.execute(sql, value)
         mysql_stud.connection.commit()
         addInSubject(row['roll'],row['name'],year,div)
         count +=1
            
         


   

      






