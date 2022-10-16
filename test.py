import pandas as pd
# import connection as cn
import mysql.connector 


connection = mysql.connector.connect(host='localhost',
                                       database='Students',
                                       username='root',
                                       password='')

cursor = connection.cursor()
filePath = 'static/files\Book1.csv'
col_names = ['roll','name','prn']
csvData = pd.read_csv(filePath,names=col_names, header=None)
for i,row in csvData.iterrows():
    sql = "INSERT INTO FY (ROLL_NO, NAME, PRN, YEAR, DIVISION) VALUES (%s, %s, %s, %s, %s)"
    value = (row['roll'],row['name'],row['prn'],'fy','b')
    cursor.execute(sql, value)
    connection.commit()


cursor.close()
connection.close()





