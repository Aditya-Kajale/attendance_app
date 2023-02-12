import pandas as pd
from routes import mysql_stud
import mysql.connector
import pickle

fs = 'subinfo.pkl'

def addInSubject(roll,name,prn,year,div):
   at_btech = mysql.connector.connect(user='root', password='', host='localhost', database='theory_btech')
   at_ty = mysql.connector.connect(user='root', password='', host='localhost', database='theory_ty')
   at_sy = mysql.connector.connect(user='root', password='', host='localhost', database='theory_sy')
   at_fy = mysql.connector.connect(user='root', password='', host='localhost', database='theory_fy')

   btech = at_btech.cursor()
   ty = at_ty.cursor()
   sy = at_sy.cursor()
   fy = at_fy.cursor()

   fsub = open(fs,'rb')
   subs_btech = pickle.load(fsub)

   # print(year)
   if year == "BTECH":
      for i in subs_btech['Theory'][year]:
         sql = "INSERT INTO "+"`"+i+"`"+" (roll,name,prn,division) VALUES (%s,%s,%s,%s)"
         values = (str(roll),name,prn,div)
         btech.execute(sql,values)
         at_btech.commit()
      at_btech.close()
   
   elif year == 'TY':
      for i in subs_btech['Theory'][year]:
         sql = "INSERT INTO "+"`"+i+"`"+" (roll,name,prn,division) VALUES (%s,%s,%s,%s)"
         values = (str(roll),name,prn,div)
         ty.execute(sql,values)
         at_ty.commit()
      at_ty.close()

   elif year == 'SY':
      for i in subs_btech['Theory'][year]:
         sql = "INSERT INTO "+"`"+i+"`"+" (roll,name,prn,division) VALUES (%s,%s,%s,%s)"
         values = (str(roll),name,prn,div)
         sy.execute(sql,values)
         at_sy.commit()
      at_sy.close()

   elif year == 'FY':
      for i in subs_btech['Theory'][year]:
         sql = "INSERT INTO "+"`"+i+"`"+" (roll,name,prn,division) VALUES (%s,%s,%s,%s)"
         values = (str(roll),name,prn,div)
         fy.execute(sql,values)
         at_fy.commit()
      at_fy.close()


# ------------for practical -------------
def addInPractical(roll,name,prn,year,div,batch):
   ap_btech = mysql.connector.connect(user='root', password='', host='localhost', database='practical_btech')
   ap_ty = mysql.connector.connect(user='root', password='', host='localhost', database='practical_ty')
   ap_sy = mysql.connector.connect(user='root', password='', host='localhost', database='practical_sy')
   ap_fy = mysql.connector.connect(user='root', password='', host='localhost', database='practical_fy')

   btechP = ap_btech.cursor()
   tyP = ap_ty.cursor()
   syP = ap_sy.cursor()
   fyP = ap_fy.cursor()

   fsub = open(fs,'rb')
   subs_btech = pickle.load(fsub)

   if year == "BTECH":
      for i in subs_btech['Practical'][year]:
         sql = "INSERT INTO "+"`"+i+"`"+" (roll,name,prn,division,batch) VALUES (%s,%s,%s,%s,%s)"
         values = (str(roll),name,prn,div,batch)
         btechP.execute(sql,values)
         ap_btech.commit()
      ap_btech.close()
   
   elif year == 'TY':
      for i in subs_btech['Practical'][year]:
         sql = "INSERT INTO "+"`"+i+"`"+" (roll,name,prn,division,batch) VALUES (%s,%s,%s,%s,%s)"
         values = (str(roll),name,prn,div,batch)
         tyP.execute(sql,values)
         ap_ty.commit()
      ap_ty.close()

   elif year == 'SY':
      for i in subs_btech['Practical'][year]:
         sql = "INSERT INTO "+"`"+i+"`"+" (roll,name,prn,division,batch) VALUES (%s,%s,%s,%s,%s)"
         values = (str(roll),name,prn,div,batch)
         syP.execute(sql,values)
         ap_sy.commit()
      ap_sy.close()

   elif year == 'FY':
      for i in subs_btech['Practical'][year]:
         sql = "INSERT INTO "+"`"+i+"`"+" (roll,name,prn,division,batch) VALUES (%s,%s,%s,%s,%s)"
         values = (str(roll),name,prn,div,batch)
         fyP.execute(sql,values)
         ap_fy.commit()
      ap_fy.close()


def parseCSV(filePath,year,div):
   cur = mysql_stud.connection.cursor()
   col_names = ['roll','name','prn','batch']
   csvData = pd.read_csv(filePath,names=col_names, header=None)
   print(csvData)
   for i,row in csvData.iterrows():
      try:
         sql = "INSERT INTO "+ year +" (ROLL_NO, NAME, PRN, YEAR, DIVISION, BATCH) VALUES (%s, %s, %s, %s, %s, %s)"
         value = (row['roll'],row['name'],row['prn'],year,div,row['batch'])
         cur.execute(sql, value)
         mysql_stud.connection.commit()
         addInSubject(row['roll'],row['name'],row['prn'],year,div)
         addInPractical(row['roll'],row['name'],row['prn'],year,div,row['batch'])
      except:
         print('PRN already exist')

