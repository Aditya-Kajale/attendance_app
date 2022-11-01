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
    
    # For BTECH -----------------------------------------------
    if year=='BTECH':
        # For SE -----------------------------------------------
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
        
        # For BDA -----------------------------------------------
        elif subject=="Big Data Analytics":
            sql = 'SELECT roll,division FROM bda WHERE division = "{}"'.format(division)
            btech.execute(sql)
            data = btech.fetchall()

            row = []
            for i in data:
                row.append(list(i))
            total['roll'] = row

            new_dates = []
            for i in dates:
                try:    
                    sql = 'SELECT {} FROM bda WHERE division = "{}"'.format(i,division)
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


        # For CC -----------------------------------------------
        elif subject=="Cloud Computing":
            sql = 'SELECT roll,division FROM cc WHERE division = "{}"'.format(division)
            btech.execute(sql)
            data = btech.fetchall()

            row = []
            for i in data:
                row.append(list(i))
            total['roll'] = row

            new_dates = []
            for i in dates:
                try:    
                    sql = 'SELECT {} FROM cc WHERE division = "{}"'.format(i,division)
                    btech.execute(sql)
                    data = btech.fetchall()
                    total[i] = data
                    new_dates.append(i)
                except:
                    print('except')

            total['dates'] = new_dates

            for i in range(len(total['dates'])):
                for j in range(len(total['roll'])):
                    total['roll'][j].append(total[total['dates'][i]][j][0])

            total['pre'] = [year,division,subject]

        # For BT -----------------------------------------------
        elif subject=="Blockchain Technology":
            sql = 'SELECT roll,division FROM bt WHERE division = "{}"'.format(division)
            btech.execute(sql)
            data = btech.fetchall()

            row = []
            for i in data:
                row.append(list(i))
            total['roll'] = row

            new_dates = []
            for i in dates:
                try:    
                    sql = 'SELECT {} FROM bt WHERE division = "{}"'.format(i,division)
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
        
        # For FSD -------------------------------------------
        elif subject=="Full Stack Development":
            sql = 'SELECT roll,division FROM fsd WHERE division = "{}"'.format(division)
            btech.execute(sql)
            data = btech.fetchall()

            row = []
            for i in data:
                row.append(list(i))
            total['roll'] = row

            new_dates = []
            for i in dates:
                try:    
                    sql = 'SELECT {} FROM fsd WHERE division = "{}"'.format(i,division)
                    btech.execute(sql)
                    data = btech.fetchall()
                    total[i] = data
                    new_dates.append(i)
                except:
                    print('except')

            total['dates'] = new_dates

            for i in range(len(total['dates'])):
                for j in range(len(total['roll'])):
                    total['roll'][j].append(total[total['dates'][i]][j][0])

            total['pre'] = [year,division,subject]

        # For SA --------------------------------------------
        elif subject=="System Administration":
            sql = 'SELECT roll,division FROM sa WHERE division = "{}"'.format(division)
            btech.execute(sql)
            data = btech.fetchall()

            row = []
            for i in data:
                row.append(list(i))
            total['roll'] = row

            new_dates = []
            for i in dates:
                try:    
                    sql = 'SELECT {} FROM sa WHERE division = "{}"'.format(i,division)
                    btech.execute(sql)
                    data = btech.fetchall()
                    total[i] = data
                    new_dates.append(i)
                except:
                    print('except')

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
        ll = []
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

        # FOR Big Data Analysis------------------------------
        ll = []
        total['subs'].append('BDA')
        for i in dates:
            try:
                sql = 'SELECT {} AS "total" FROM bda WHERE division = "A"'.format(i)
                btech.execute(sql)
                data = btech.fetchall()
                # print(data)
                for k in range(len(data)):
                    data[k] = data[k][0]
                ll.append(data)
            except:
                print('except')
        su = [sum(x) for x in zip(*ll)]

        for j in range(len(total['roll'])):
            total['roll'][j].append(su[j])

        # For Cloud Computing ------------------------------
        ll = []
        total['subs'].append('CC')
        for i in dates:
            try:
                sql = 'SELECT {} AS "total" FROM cc WHERE division = "A"'.format(i)
                btech.execute(sql)
                data = btech.fetchall()
                # print(data)
                for k in range(len(data)):
                    data[k] = data[k][0]
                ll.append(data)
            except:
                print('except')
        su = [sum(x) for x in zip(*ll)]

        for j in range(len(total['roll'])):
            total['roll'][j].append(su[j])
        
        # For Blockchain Technology ------------------------
        ll = []
        total['subs'].append('BT')
        for i in dates:
            try:
                sql = 'SELECT {} AS "total" FROM bt WHERE division = "A"'.format(i)
                btech.execute(sql)
                data = btech.fetchall()
                # print(data)
                for k in range(len(data)):
                    data[k] = data[k][0]
                ll.append(data)
            except:
                print('except')
        su = [sum(x) for x in zip(*ll)]

        for j in range(len(total['roll'])):
            total['roll'][j].append(su[j])

        # For Full Stacck Development ------------------------
        ll = []
        total['subs'].append('FSD')
        for i in dates:
            try:
                sql = 'SELECT {} AS "total" FROM fsd WHERE division = "A"'.format(i)
                btech.execute(sql)
                data = btech.fetchall()
                # print(data)
                for k in range(len(data)):
                    data[k] = data[k][0]
                ll.append(data)
            except:
                print('except')
        su = [sum(x) for x in zip(*ll)]

        for j in range(len(total['roll'])):
            total['roll'][j].append(su[j])

        # For System Administration --------------------------
        ll = []
        total['subs'].append('SA')
        for i in dates:
            try:
                sql = 'SELECT {} AS "total" FROM sa WHERE division = "A"'.format(i)
                btech.execute(sql)
                data = btech.fetchall()
                # print(data)
                for k in range(len(data)):
                    data[k] = data[k][0]
                ll.append(data)
            except:
                print('except')
        su = [sum(x) for x in zip(*ll)]

        for j in range(len(total['roll'])):
            total['roll'][j].append(su[j])

    print(total)
    return total