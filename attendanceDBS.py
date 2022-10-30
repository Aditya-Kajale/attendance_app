import pandas as pd
import mysql.connector
from datetime import date, timedelta

at_btech = mysql.connector.connect(user='root', password='', host='localhost', database='theory_btech')
at_ty = mysql.connector.connect(user='root', password='', host='localhost', database='theory_ty')
at_sy = mysql.connector.connect(user='root', password='', host='localhost', database='theory_sy')
at_fy = mysql.connector.connect(user='root', password='', host='localhost', database='theory_fy')

btech = at_btech.cursor()
ty = at_ty.cursor()
sy = at_sy.cursor()
fy = at_fy.cursor()

def subjectAttendance (year,division,subject,sdate,edate):
    total ={}
    sdate = list(map(int,sdate.split('-')))
    edate = list(map(int,edate.split('-')))
    sdate = date(sdate[0],sdate[1],sdate[2])
    edate = date(edate[0],edate[1],edate[2])
    a = [sdate+timedelta(days=x) for x in range((edate-sdate).days)]
    dates = []
    for i in a:
        ss = i.strftime("%Y_%m_%d")
        dates.append(ss)

    total['dates'] = dates
    # print(year,type(division),subject,sdate,edate,total)
    
    if year=='BTECH':
        if subject=="Software Engineering":
            sql = 'SELECT roll,division FROM se WHERE division = "{}"'.format(division)
            btech.execute(sql)
            data = btech.fetchall()

            row = []
            for i in data:
                row.append(list(i))
            total['roll'] = row


            for i in total['dates']:
                sql = 'SELECT {} FROM se WHERE division = "{}"'.format(i,division)
                btech.execute(sql)
                data = btech.fetchall()
                total[i] = data
            

            for i in range(len(total['dates'])):
                for j in range(len(total['roll'])):
                    total['roll'][j].append(total[total['dates'][i]][j][0])

            # print(total)
            total['pre'] = [year,division,subject]

    return total