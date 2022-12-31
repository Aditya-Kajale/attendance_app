import pandas as pd
import mysql.connector
from datetime import date, timedelta
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

    # For BTECH -----------------------------------------------
    if year=='BTECH':
        try:
            sql = 'SELECT roll,name,division FROM `'+subject+'` WHERE division = "{}"'.format(division)
            btech.execute(sql)
            data = btech.fetchall()
        except:
            print('subject is not in the perticular year')
            total['pre'] = [year,division,subject]
            return total

        row = []
        for i in data:
            row.append(list(i))
        total['roll'] = row

        new_dates = []
        for i in dates:
            try:    
                sql = 'SELECT {} FROM `{}` WHERE division = "{}"'.format(i,subject,division)
                btech.execute(sql)
                data = btech.fetchall()
                if data[0][0] != -1:
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

    elif year=='TY':
        try:
            sql = 'SELECT roll,name,division FROM `'+subject+'` WHERE division = "{}"'.format(division)
            ty.execute(sql)
            data = ty.fetchall()
        except:
            print('subject is not in the perticular year')
            total['pre'] = [year,division,subject]
            return total

        row = []
        for i in data:
            row.append(list(i))
        total['roll'] = row

        new_dates = []
        for i in dates:
            try:    
                sql = 'SELECT {} FROM `{}` WHERE division = "{}"'.format(i,subject,division)
                ty.execute(sql)
                data = ty.fetchall()
                if data[0][0] != -1:
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
    
    elif year=='SY':
        try:
            sql = 'SELECT roll,name,division FROM `'+subject+'` WHERE division = "{}"'.format(division)
            sy.execute(sql)
            data = sy.fetchall()
        except:
            print('subject is not in the perticular year')
            total['pre'] = [year,division,subject]
            return total

        row = []
        for i in data:
            row.append(list(i))
        total['roll'] = row

        new_dates = []
        for i in dates:
            try:    
                sql = 'SELECT {} FROM `{}` WHERE division = "{}"'.format(i,subject,division)
                sy.execute(sql)
                data = sy.fetchall()
                if data[0][0] != -1:
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
    
    elif year=='FY':
        try:
            sql = 'SELECT roll,name,division FROM `'+subject+'` WHERE division = "{}"'.format(division)
            fy.execute(sql)
            data = fy.fetchall()
        except:
            print('subject is not in the perticular year')
            total['pre'] = [year,division,subject]
            return total

        row = []
        for i in data:
            row.append(list(i))
        total['roll'] = row

        new_dates = []
        for i in dates:
            try:    
                sql = 'SELECT {} FROM `{}` WHERE division = "{}"'.format(i,subject,division)
                fy.execute(sql)
                data = fy.fetchall()
                if data[0][0] != -1:
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
    

    # print(total)
    return total


def classAttendance(year,division,sdate,edate):
    fsub = open(fs,'rb')
    subs = pickle.load(fsub)
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
        sub = subs[year][0]
        sql = 'SELECT roll,name,division FROM `{}` WHERE division = "{}"'.format(sub,division)
        btech.execute(sql)
        data = btech.fetchall()
        row = []
        for i in data:
            row.append(list(i))
        total['roll'] = row
        # print(total)
        total['subs'] = []
        for j in subs[year]:
            ll = []
            total['subs'].append(j)
            # print(j)
            for i in dates:
                try:
                    sql = 'SELECT {} FROM `{}` WHERE division = "{}"'.format(i,j,division)
                    btech.execute(sql)
                    data = btech.fetchall()
                    # print(data)
                    if data[0][0] != -1:
                        new_dates.append(i)
                        for k in range(len(data)):
                            data[k] = data[k][0]
                        ll.append(data)
                except:
                    print('except')

            
            total['dates'] = new_dates
            su = [sum(x) for x in zip(*ll)]
            if len(su) == 0:
                # print(len(total['roll']))
                for l in range(len(total['roll'])):
                    su.append(0)
            # print('su',su)

            for k in range(len(total['roll'])):
                total['roll'][k].append(su[k])

    elif year=='TY':
        try:
            sub = subs[year][0]
            sql = 'SELECT roll,name,division FROM `{}` WHERE division = "{}"'.format(sub,division)
            ty.execute(sql)
            data = ty.fetchall()
        except:
            print('no subject')
            data = []
        row = []
        for i in data:
            row.append(list(i))
        total['roll'] = row
        # print(total)
        total['subs'] = []
        
        for j in subs[year]:
            ll = []
            total['subs'].append(j)
            # print(j)
            for i in dates:
                try:
                    sql = 'SELECT {} FROM `{}` WHERE division = "{}"'.format(i,j,division)
                    ty.execute(sql)
                    data = ty.fetchall()
                    # print(data)
                    if data[0][0] != -1:
                        new_dates.append(i)
                        for k in range(len(data)):
                            data[k] = data[k][0]
                        ll.append(data)
                except:
                    print('except')

            
            total['dates'] = new_dates
            su = [sum(x) for x in zip(*ll)]
            if len(su) == 0:
                # print(len(total['roll']))
                for l in range(len(total['roll'])):
                    su.append(0)
            # print('su',su)

            for k in range(len(total['roll'])):
                total['roll'][k].append(su[k])
    
    elif year=='SY':
        try:
            sub = subs[year][0]
            sql = 'SELECT roll,name,division FROM `{}` WHERE division = "{}"'.format(sub,division)
            sy.execute(sql)
            data = sy.fetchall()
        except:
            print('no subject')
            data = []
        row = []
        for i in data:
            row.append(list(i))
        total['roll'] = row
        # print(total)
        total['subs'] = []
        
        for j in subs[year]:
            ll = []
            total['subs'].append(j)
            # print(j)
            for i in dates:
                try:
                    sql = 'SELECT {} FROM `{}` WHERE division = "{}"'.format(i,j,division)
                    sy.execute(sql)
                    data = sy.fetchall()
                    # print(data)
                    if data[0][0] != -1:
                        new_dates.append(i)
                        for k in range(len(data)):
                            data[k] = data[k][0]
                        ll.append(data)
                except:
                    print('except')

            
            total['dates'] = new_dates
            su = [sum(x) for x in zip(*ll)]
            if len(su) == 0:
                # print(len(total['roll']))
                for l in range(len(total['roll'])):
                    su.append(0)
            # print('su',su)

            for k in range(len(total['roll'])):
                total['roll'][k].append(su[k])
    
    elif year=='FY':
        try:
            sub = subs[year][0]
            sql = 'SELECT roll,name,division FROM `{}` WHERE division = "{}"'.format(sub,division)
            fy.execute(sql)
            data = fy.fetchall()
        except:
            print('no subject')
            data = []
        row = []
        for i in data:
            row.append(list(i))
        total['roll'] = row
        # print(total)
        total['subs'] = []
        
        for j in subs[year]:
            ll = []
            total['subs'].append(j)
            # print(j)
            for i in dates:
                try:
                    sql = 'SELECT {} FROM `{}` WHERE division = "{}"'.format(i,j,division)
                    fy.execute(sql)
                    data = fy.fetchall()
                    # print(data)
                    if data[0][0] != -1:
                        new_dates.append(i)
                        for k in range(len(data)):
                            data[k] = data[k][0]
                        ll.append(data)
                except:
                    print('except')

            
            total['dates'] = new_dates
            su = [sum(x) for x in zip(*ll)]
            if len(su) == 0:
                # print(len(total['roll']))
                for l in range(len(total['roll'])):
                    su.append(0)
            # print('su',su)

            for k in range(len(total['roll'])):
                total['roll'][k].append(su[k])
    # print(new_dates)
    # print(total)
    return total

def defaulterData(year,division,sdate,edate,defaulter):
    fsub = open(fs,'rb')
    subs = pickle.load(fsub)
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
        try:
            sub = subs[year][0]
            sql = 'SELECT roll,name,division FROM `{}` WHERE division = "{}"'.format(sub,division)
            btech.execute(sql)
            data = btech.fetchall()
        except:
            print('no subject')
            data = []
        row = []
        for i in data:
            row.append(list(i))
        total['roll'] = row
        # print(total)
        total['subs'] = []
        
        for j in subs[year]:
            ll = []
            total['subs'].append(j)
            # print(j)
            total[j] = 0
            for i in dates:
                try:
                    sql = 'SELECT {} FROM `{}` WHERE division = "{}"'.format(i,j,division)
                    btech.execute(sql)
                    data = btech.fetchall()
                    print(data)
                    if data[0][0] != -1:
                        new_dates.append(i)
                        total[j] +=1
                        print(data)
                        for k in range(len(data)):
                            data[k] = data[k][0]
                        ll.append(data)
                except:
                    print('except')

            
            total['dates'] = new_dates
            su = [sum(x) for x in zip(*ll)]
            if len(su) == 0:
                # print(len(total['roll']))
                for l in range(len(total['roll'])):
                    su.append(0)
            # print('su',su)

            for k in range(len(total['roll'])):
                total['roll'][k].append(su[k])
            
        # for the defaulter column part
        # Total Sessions
        sess_count=0
        for i in subs[year]:
            sess_count += total[i]

        # Session Attended
        for i in range(len(total['roll'])):
            # print(total['roll'][i])
            cnt = 0
            for j in range(3,len(total['roll'][i])):
                # print(total['roll'][i][j])
                cnt+=total['roll'][i][j]
            # print(cnt)
            percentage = 0
            try:
                percentage = (cnt/sess_count)*100
                percentage = round(percentage,2)
            except:
                print('division error')
            total['roll'][i].append(cnt)
            total['roll'][i].append(sess_count)
            total['roll'][i].append(percentage)

        # attendance percentage 
        

        total['subs'].append('Session Attended')
        total['subs'].append('Total Sessions')
        total['subs'].append('Attendance Percentage')
        total['defaulter'] = int(defaulter)
        #     print(new_dates)

    elif year=='TY':
        try:
            sub = subs[year][0]
            sql = 'SELECT roll,name,division FROM `{}` WHERE division = "{}"'.format(sub,division)
            ty.execute(sql)
            data = ty.fetchall()
        except:
            print('no subject')
            data = []
        row = []
        for i in data:
            row.append(list(i))
        total['roll'] = row
        # print(total)
        total['subs'] = []
        
        for j in subs[year]:
            ll = []
            total['subs'].append(j)
            # print(j)
            total[j] = 0
            for i in dates:
                try:
                    sql = 'SELECT {} FROM `{}` WHERE division = "{}"'.format(i,j,division)
                    ty.execute(sql)
                    data = ty.fetchall()
                    print(data)
                    if data[0][0] != -1:
                        new_dates.append(i)
                        total[j] +=1
                        print(data)
                        for k in range(len(data)):
                            data[k] = data[k][0]
                        ll.append(data)
                except:
                    print('except')

            
            total['dates'] = new_dates
            su = [sum(x) for x in zip(*ll)]
            if len(su) == 0:
                # print(len(total['roll']))
                for l in range(len(total['roll'])):
                    su.append(0)
            # print('su',su)

            for k in range(len(total['roll'])):
                total['roll'][k].append(su[k])
            
        # for the defaulter column part
        # Total Sessions
        sess_count=0
        for i in subs[year]:
            sess_count += total[i]

        # Session Attended
        for i in range(len(total['roll'])):
            # print(total['roll'][i])
            cnt = 0
            for j in range(3,len(total['roll'][i])):
                # print(total['roll'][i][j])
                cnt+=total['roll'][i][j]
            # print(cnt)
            percentage = 0
            try:
                percentage = (cnt/sess_count)*100
                percentage = round(percentage,2)
            except:
                print('division error')
            total['roll'][i].append(cnt)
            total['roll'][i].append(sess_count)
            total['roll'][i].append(percentage)

        # attendance percentage 
        

        total['subs'].append('Session Attended')
        total['subs'].append('Total Sessions')
        total['subs'].append('Attendance Percentage')
        total['defaulter'] = int(defaulter)
        #     print(new_dates)

    elif year=='SY':
        try:
            sub = subs[year][0]
            sql = 'SELECT roll,name,division FROM `{}` WHERE division = "{}"'.format(sub,division)
            sy.execute(sql)
            data = sy.fetchall()
        except:
            print('no subject')
            data = []
        row = []
        for i in data:
            row.append(list(i))
        total['roll'] = row
        # print(total)
        total['subs'] = []
        
        for j in subs[year]:
            ll = []
            total['subs'].append(j)
            # print(j)
            total[j] = 0
            for i in dates:
                try:
                    sql = 'SELECT {} FROM `{}` WHERE division = "{}"'.format(i,j,division)
                    sy.execute(sql)
                    data = sy.fetchall()
                    print(data)
                    if data[0][0] != -1:
                        new_dates.append(i)
                        total[j] +=1
                        print(data)
                        for k in range(len(data)):
                            data[k] = data[k][0]
                        ll.append(data)
                except:
                    print('except')

            
            total['dates'] = new_dates
            su = [sum(x) for x in zip(*ll)]
            if len(su) == 0:
                # print(len(total['roll']))
                for l in range(len(total['roll'])):
                    su.append(0)
            # print('su',su)

            for k in range(len(total['roll'])):
                total['roll'][k].append(su[k])
            
        # for the defaulter column part
        # Total Sessions
        sess_count=0
        for i in subs[year]:
            sess_count += total[i]

        # Session Attended
        for i in range(len(total['roll'])):
            # print(total['roll'][i])
            cnt = 0
            for j in range(3,len(total['roll'][i])):
                # print(total['roll'][i][j])
                cnt+=total['roll'][i][j]
            # print(cnt)
            percentage = 0
            try:
                percentage = (cnt/sess_count)*100
                percentage = round(percentage,2)
            except:
                print('division error')
            total['roll'][i].append(cnt)
            total['roll'][i].append(sess_count)
            total['roll'][i].append(percentage)

        # attendance percentage 
        

        total['subs'].append('Session Attended')
        total['subs'].append('Total Sessions')
        total['subs'].append('Attendance Percentage')
        total['defaulter'] = int(defaulter)
        #     print(new_dates)

    elif year=='FY':
        try:
            sub = subs[year][0]
            sql = 'SELECT roll,name,division FROM `{}` WHERE division = "{}"'.format(sub,division)
            fy.execute(sql)
            data = fy.fetchall()
        except:
            print('no subject')
            data = []
        row = []
        for i in data:
            row.append(list(i))
        total['roll'] = row
        # print(total)
        total['subs'] = []
        
        for j in subs[year]:
            ll = []
            total['subs'].append(j)
            # print(j)
            total[j] = 0
            for i in dates:
                try:
                    sql = 'SELECT {} FROM `{}` WHERE division = "{}"'.format(i,j,division)
                    fy.execute(sql)
                    data = fy.fetchall()
                    print(data)
                    if data[0][0] != -1:
                        new_dates.append(i)
                        total[j] +=1
                        print(data)
                        for k in range(len(data)):
                            data[k] = data[k][0]
                        ll.append(data)
                except:
                    print('except')

            
            total['dates'] = new_dates
            su = [sum(x) for x in zip(*ll)]
            if len(su) == 0:
                # print(len(total['roll']))
                for l in range(len(total['roll'])):
                    su.append(0)
            # print('su',su)

            for k in range(len(total['roll'])):
                total['roll'][k].append(su[k])
            
        # for the defaulter column part
        # Total Sessions
        sess_count=0
        for i in subs[year]:
            sess_count += total[i]

        # Session Attended
        for i in range(len(total['roll'])):
            # print(total['roll'][i])
            cnt = 0
            for j in range(3,len(total['roll'][i])):
                # print(total['roll'][i][j])
                cnt+=total['roll'][i][j]
            # print(cnt)
            percentage = 0
            try:
                percentage = (cnt/sess_count)*100
                percentage = round(percentage,2)
            except:
                print('division error')
            total['roll'][i].append(cnt)
            total['roll'][i].append(sess_count)
            total['roll'][i].append(percentage)

        # attendance percentage 
        

        total['subs'].append('Session Attended')
        total['subs'].append('Total Sessions')
        total['subs'].append('Attendance Percentage')
        total['defaulter'] = int(defaulter)
        #     print(new_dates)

    # print(total)
    return total