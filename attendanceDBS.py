from tkinter import N
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

            new_dates = []
            for i in dates:
                try:    
                    sql = 'SELECT {} FROM se WHERE division = "{}"'.format(i,division)
                    btech.execute(sql)
                    data = btech.fetchall()
                    total[i] = data
                    new_dates.append(i)
                except:
                    print('except')
            # print(new_dates)

            total['dates'] = new_dates

            for i in range(len(total['dates'])):
                for j in range(len(total['roll'])):
                    total['roll'][j].append(total[total['dates'][i]][j][0])

            total['pre'] = [year,division,subject]
    print(total)
    return total


def classAttendance(year,division,sdate,edate):
    total = {}
    total['pre'] = [year,division,sdate,edate]
    sdate = list(map(int,sdate.split('-')))
    edate = list(map(int,edate.split('-')))
    sdate = date(sdate[0],sdate[1],sdate[2])
    edate = date(edate[0],edate[1],edate[2])
    a = [sdate+timedelta(days=x) for x in range((edate-sdate).days)]
    dates = []
    for i in a:
        ss = i.strftime("%Y_%m_%d")
        dates.append(ss)
    ll = []
    new_dates = []

    if year=='BTECH':
        sql = 'SELECT roll,division FROM se WHERE division = "{}"'.format(division)
        btech.execute(sql)
        data = btech.fetchall()
        row = []
        for i in data:
            row.append(list(i))
        total['roll'] = row
        # print(total)
        total['subs'] = []
        
        # FOR SOFTWARE ENGINEERING---------------
        total['subs'].append('SE')
        for i in dates:
            try:
                sql = 'SELECT {} AS "total" FROM se WHERE division = "A"'.format(i)
                btech.execute(sql)
                data = btech.fetchall()
                # print(data)
                for k in range(len(data)):
                    data[k] = data[k][0]
                ll.append(data)
                new_dates.append(i)
            except:
                print('except')
        total['dates'] = new_dates
        su = [sum(x) for x in zip(*ll)]

        for j in range(len(total['roll'])):
            total['roll'][j].append(su[j])

        # FOR DIFFRENT SUBJECT--------------------

    return total