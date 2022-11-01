import pandas as pd
# import connection as cn
from datetime import date, timedelta
import mysql.connector 

at_btech = mysql.connector.connect(user='root', password='', host='localhost', database='theory_btech')

btech = at_btech.cursor()

sdate = date(2022,10,22)   # start date
edate = date(2022,10,31)   # end date
a = [sdate+timedelta(days=x) for x in range((edate-sdate).days)]
print(a)
tt = []
for i in a:
    ss = i.strftime("%Y_%m_%d")
    tt.append(ss)

# dts = '+'.join(tt)
# print(tt)

ll = []
try:
    for i in tt:
        print(i)
        sql = 'SELECT {} AS "total" FROM se WHERE division = "A"'.format(i)
        btech.execute(sql)
        data = btech.fetchall()
        # print(data)
        for k in range(len(data)):
            data[k] = data[k][0]
        ll.append(data)
except:
    print('except')

su = [sum(x) for x in zip(*ll)]
print(su)


# # sdate = '2019-3-22'
# # sdate = date(sdate)



    




