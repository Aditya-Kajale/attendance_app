import pandas as pd
import mysql.connector
from datetime import date, timedelta
import pickle



ap_btech = mysql.connector.connect(user='root', password='', host='localhost', database='practical_btech')
ap_ty = mysql.connector.connect(user='root', password='', host='localhost', database='practical_ty')
ap_sy = mysql.connector.connect(user='root', password='', host='localhost', database='practical_sy')
ap_fy = mysql.connector.connect(user='root', password='', host='localhost', database='practical_fy')
btechP = ap_btech.cursor()
tyP = ap_ty.cursor()
syP = ap_sy.cursor()
fyP = ap_fy.cursor()

fs = 'subinfo.pkl'


def subjectAttendance_theory (year,division,subject,sdate,edate):
    at_btech = mysql.connector.connect(user='root', password='', host='localhost', database='theory_btech')
    at_ty = mysql.connector.connect(user='root', password='', host='localhost', database='theory_ty')
    at_sy = mysql.connector.connect(user='root', password='', host='localhost', database='theory_sy')
    at_fy = mysql.connector.connect(user='root', password='', host='localhost', database='theory_fy')
    btech = at_btech.cursor()
    ty = at_ty.cursor()
    sy = at_sy.cursor()
    fy = at_fy.cursor()

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

        total['dates'] = new_dates

        for i in range(len(total['dates'])):
            for j in range(len(total['roll'])):
                total['roll'][j].append(total[total['dates'][i]][j][0])

        total['pre'] = [year,division,subject]
        at_btech.close()

    # print(total)
    return total

# For practical data ---------------------------------------------------------

def subjectAttendance_practical(year,division,subject,batch,sdate,edate):
    ap_btech = mysql.connector.connect(user='root', password='', host='localhost', database='practical_btech')
    ap_ty = mysql.connector.connect(user='root', password='', host='localhost', database='practical_ty')
    ap_sy = mysql.connector.connect(user='root', password='', host='localhost', database='practical_sy')
    ap_fy = mysql.connector.connect(user='root', password='', host='localhost', database='practical_fy')
    btechP = ap_btech.cursor()
    tyP = ap_ty.cursor()
    syP = ap_sy.cursor()
    fyP = ap_fy.cursor()

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

    if year=='BTECH':
        try:
            sql = 'SELECT roll,name,division,batch FROM `'+subject+'` WHERE batch = "{}"'.format(batch)
            btechP.execute(sql)
            data = btechP.fetchall()
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
                sql = 'SELECT {} FROM `{}` WHERE batch = "{}"'.format(i,subject,batch)
                btechP.execute(sql)
                data = btechP.fetchall()
                print(data)
                if data[0][0] != -1:
                    total[i] = data
                    new_dates.append(i)
            except:
                print('except')

        total['dates'] = new_dates

        for i in range(len(total['dates'])):
            for j in range(len(total['roll'])):
                total['roll'][j].append(total[total['dates'][i]][j][0])

        total['pre'] = [year,division,subject,batch,sdate,edate]
        ap_btech.close()

    return total

# for class attendance ------------------------------------------------------
def classAttendance(year,division,sdate,edate):
    at_btech = mysql.connector.connect(user='root', password='', host='localhost', database='theory_btech')
    at_ty = mysql.connector.connect(user='root', password='', host='localhost', database='theory_ty')
    at_sy = mysql.connector.connect(user='root', password='', host='localhost', database='theory_sy')
    at_fy = mysql.connector.connect(user='root', password='', host='localhost', database='theory_fy')
    btech = at_btech.cursor()
    ty = at_ty.cursor()
    sy = at_sy.cursor()
    fy = at_fy.cursor()

    ap_btech = mysql.connector.connect(user='root', password='', host='localhost', database='practical_btech')
    ap_ty = mysql.connector.connect(user='root', password='', host='localhost', database='practical_ty')
    ap_sy = mysql.connector.connect(user='root', password='', host='localhost', database='practical_sy')
    ap_fy = mysql.connector.connect(user='root', password='', host='localhost', database='practical_fy')
    btechP = ap_btech.cursor()
    tyP = ap_ty.cursor()
    syP = ap_sy.cursor()
    fyP = ap_fy.cursor()

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
        # for theory-----------------------------
        sub = subs['Theory'][year][0]
        sql = 'SELECT roll,name,division FROM `{}` WHERE division = "{}"'.format(sub,division)
        btech.execute(sql)
        data = btech.fetchall()
        row = []
        for i in data:
            row.append(list(i))
        total['roll'] = row
        # print(total)
        total['subs'] = []
        for j in subs['Theory'][year]:
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

        # for practical --------------------------------------------------- 
        for j in subs['Practical'][year]:
            ll = []
            total['subs'].append(j)
            # print(j)

            total[j] = []
            for i in dates:
                try:
                    sql = 'SELECT {} FROM `{}` WHERE division = "{}"'.format(i,j,division)
                    btechP.execute(sql)
                    data = btechP.fetchall()
                    # print(data)
                    for k in range(len(data)):
                        data[k] = data[k][0]
                    # print(data,i)

                    # for sessions happend storng in per subject list in total 
                    for c in range(len(data)):
                        if len(total[j]) != len(data):
                            if  data[c] == -1:
                                total[j].append(0)
                            else:
                                total[j].append(2)
                        else:
                            if data[c] == -1:
                                pass
                            else:
                                total[j][c] += 2
                    # print(total[j])
                    for kj in range(len(data)):
                        if data[kj] == -1:
                            data[kj] = 0

                    ll.append(data)
                except:
                    print('except')
            su = [sum(x) for x in zip(*ll)]
            # print('su',su)
            if len(su) == 0:
                # print(len(total['roll']))
                for l in range(len(total['roll'])):
                    su.append(0)

            for k in range(len(total['roll'])):
                if su[k] ==-1:
                    # print(su[k])
                    total['roll'][k].append(0)
                else:
                    total['roll'][k].append(su[k])
    at_btech.close()
    ap_btech.close()

    # print(new_dates)
    # print(total)
    return total

def defaulterData(year,division,sdate,edate,defaulter):
    at_btech = mysql.connector.connect(user='root', password='', host='localhost', database='theory_btech')
    at_ty = mysql.connector.connect(user='root', password='', host='localhost', database='theory_ty')
    at_sy = mysql.connector.connect(user='root', password='', host='localhost', database='theory_sy')
    at_fy = mysql.connector.connect(user='root', password='', host='localhost', database='theory_fy')
    btech = at_btech.cursor()
    ty = at_ty.cursor()
    sy = at_sy.cursor()
    fy = at_fy.cursor()

    ap_btech = mysql.connector.connect(user='root', password='', host='localhost', database='practical_btech')
    ap_ty = mysql.connector.connect(user='root', password='', host='localhost', database='practical_ty')
    ap_sy = mysql.connector.connect(user='root', password='', host='localhost', database='practical_sy')
    ap_fy = mysql.connector.connect(user='root', password='', host='localhost', database='practical_fy')
    btechP = ap_btech.cursor()
    tyP = ap_ty.cursor()
    syP = ap_sy.cursor()
    fyP = ap_fy.cursor()

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
        # for theory----------------------------------
        try:
            sub = subs['Theory'][year][0]
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
        
        for j in subs['Theory'][year]:
            ll = []
            # print(j)
            ss = j.split()
            sname = ''
            for i in ss:
                sname+=i[0]
            total['subs'].append(sname)
            total[sname] = 0
            for i in dates:
                try:
                    sql = 'SELECT {} FROM `{}` WHERE division = "{}"'.format(i,j,division)
                    btech.execute(sql)
                    data = btech.fetchall()
                    print(data)
                    if data[0][0] != -1:
                        total[sname] +=1
                        print(data)
                        for k in range(len(data)):
                            data[k] = data[k][0]
                        ll.append(data)
                except:
                    print('except')

            su = [sum(x) for x in zip(*ll)]
            if len(su) == 0:
                # print(len(total['roll']))
                for l in range(len(total['roll'])):
                    su.append(0)
            # print('su',su)

            for k in range(len(total['roll'])):
                total['roll'][k].append(su[k])
        
        # For practical-------------------------------------------
        for j in subs['Practical'][year]:
            ll = []
            # print(j)
            ss = j.split()
            sname = ''
            for i in ss:
                sname+=i[0]
            total['subs'].append(sname)
            total[sname] = [0 for i in range(len(total['roll']))]
            for i in dates:
                try:
                    sql = 'SELECT {} FROM `{}` WHERE division = "{}"'.format(i,j,division)
                    btechP.execute(sql)
                    data = btechP.fetchall()
                    # print(data)
                    for k in range(len(data)):
                        data[k] = data[k][0]
                    # print(data,i)

                    # for sessions happend storng in per subject list in total 
                    for c in range(len(data)):
                        if len(total[sname]) != len(data):
                            if  data[c] == -1:
                                pass
                            else:
                                total[sname][c] = 2
                        else:
                            if data[c] == -1:
                                pass
                            else:
                                total[sname][c] += 2
                    # print(total[j])
                    for kj in range(len(data)):
                        if data[kj] == -1:
                            data[kj] = 0

                    ll.append(data)
                except:
                    print('except')
            su = [sum(x) for x in zip(*ll)]
            # print('su',su)
            if len(su) == 0:
                # print(len(total['roll']))
                for l in range(len(total['roll'])):
                    su.append(0)

            for k in range(len(total['roll'])):
                if su[k] ==-1:
                    # print(su[k])
                    total['roll'][k].append(0)
                else:
                    total['roll'][k].append(su[k])
            
            # print(total)
        # print(total)

        
        # for the defaulter column part
        # Total Sessions happened
        sess_count=[0 for i in range(len(total['roll'])) ]
        # print(sess_count)
        for j in subs['Theory'][year]:
            ss = j.split()
            sname = ''
            for i in ss:
                sname+=i[0]
            for kk in range(len(sess_count)):
                sess_count[kk] += total[sname]
            # print(total)

        for j in subs['Practical'][year]:
            ss = j.split()
            sname = ''
            for i in ss:
                sname+=i[0]
            for kk in range(len(total['roll'])):
                print(total[sname])
                sess_count[kk] += total[sname][kk]
                # print(total[i][kk],i)
            # print(total)
        # print(sess_count)

        # Session Attended
        for i in range(len(total['roll'])):
            # print(total['roll'][i])
            cnt = 0
            for j in range(3,len(total['roll'][i])):
                # print(total['roll'][i][j])
                cnt+=total['roll'][i][j]
            percentage = 0
            try:
                percentage = (cnt/sess_count[i])*100
                percentage = round(percentage,2)
            except:
                print('division error')
            # print(cnt)
            # print(sess_count)
            # print(percentage)
            total['roll'][i].append(cnt)
            total['roll'][i].append(sess_count[i])
            total['roll'][i].append(percentage)

        # attendance percentage 
        

        total['subs'].append('Session Attended')
        total['subs'].append('Total Sessions')
        total['subs'].append('Attendance Percentage')
        total['defaulter'] = int(defaulter)
        #     print(new_dates)
    at_btech.close()
    ap_btech.close()

    # print(total)
    return total