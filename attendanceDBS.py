import pandas as pd
import mysql.connector
from datetime import date, timedelta
import pickle

fs = 'subinfo.pkl'


def subjectAttendance_theory(year, division, subject, sdate, edate):
    at_btech = mysql.connector.connect(
        user='root', password='', host='localhost', database='theory_btech')
    at_ty = mysql.connector.connect(
        user='root', password='', host='localhost', database='theory_ty')
    at_sy = mysql.connector.connect(
        user='root', password='', host='localhost', database='theory_sy')

    btech = at_btech.cursor()
    ty = at_ty.cursor()
    sy = at_sy.cursor()

    total = {}
    sdate = list(map(int, sdate.split('-')))
    edate = list(map(int, edate.split('-')))
    sdate = date(sdate[0], sdate[1], sdate[2])
    edate = date(edate[0], edate[1], edate[2])
    a = [sdate+timedelta(days=x) for x in range((edate-sdate).days)]
    dates = []
    for i in a:
        ss = i.strftime("%Y_%m_%d")
        dates.append(ss)

    # For BTECH -----------------------------------------------
    if year == 'BTECH':
        try:
            sql = 'SELECT roll,name,division FROM `'+subject + \
                '` WHERE division = "{}"'.format(division)
            btech.execute(sql)
            data = btech.fetchall()
        except:
            print('subject is not in the perticular year')
            total['pre'] = [year, division, subject]
            return total

        row = []
        for i in data:
            row.append(list(i))
        total['roll'] = row

        new_dates = []
        for i in dates:
            try:
                sql = 'SELECT {} FROM `{}` WHERE division = "{}"'.format(
                    i, subject, division)
                btech.execute(sql)
                data = btech.fetchall()
                # new------
                temp = []
                for pp in data:
                    temp.append(pp[0])
                total[i] = []
                if 1 in temp:
                    for cc in data:
                        if cc[0] == -1:
                            total[i].append((0,))
                        else:
                            total[i].append(cc)
                    new_dates.append(i)
                print(total[i])
                # ----------------------
                # if data[0][0] != -1:
                #     total[i] = data
                # print(data)
            except:
                print('except')

        total['dates'] = new_dates

        for i in range(len(total['dates'])):
            for j in range(len(total['roll'])):
                total['roll'][j].append(total[total['dates'][i]][j][0])

        total['pre'] = [year, division, subject]

    elif year == "TY":
        try:
            sql = 'SELECT roll,name,division FROM `'+subject + \
                '` WHERE division = "{}"'.format(division)
            ty.execute(sql)
            data = ty.fetchall()
        except:
            print('subject is not in the perticular year')
            total['pre'] = [year, division, subject]
            return total

        row = []
        for i in data:
            row.append(list(i))
        total['roll'] = row

        new_dates = []
        for i in dates:
            try:
                sql = 'SELECT {} FROM `{}` WHERE division = "{}"'.format(
                    i, subject, division)
                ty.execute(sql)
                data = ty.fetchall()
                if data[0][0] != -1:
                    total[i] = data
                    new_dates.append(i)
            except:
                print('except')

        total['dates'] = new_dates

        for i in range(len(total['dates'])):
            for j in range(len(total['roll'])):
                total['roll'][j].append(total[total['dates'][i]][j][0])

        total['pre'] = [year, division, subject]

    elif year == "SY":
        try:
            sql = 'SELECT roll,name,division FROM `'+subject + \
                '` WHERE division = "{}"'.format(division)
            sy.execute(sql)
            data = sy.fetchall()
        except:
            print('subject is not in the perticular year')
            total['pre'] = [year, division, subject]
            return total

        row = []
        for i in data:
            row.append(list(i))
        total['roll'] = row

        new_dates = []
        for i in dates:
            try:
                sql = 'SELECT {} FROM `{}` WHERE division = "{}"'.format(
                    i, subject, division)
                sy.execute(sql)
                data = sy.fetchall()
                if data[0][0] != -1:
                    total[i] = data
                    new_dates.append(i)
            except:
                print('except')

        total['dates'] = new_dates

        for i in range(len(total['dates'])):
            for j in range(len(total['roll'])):
                total['roll'][j].append(total[total['dates'][i]][j][0])

        total['pre'] = [year, division, subject]

    at_sy.close()
    at_ty.close()
    at_btech.close()

    # print(total)
    return total

# For practical data ---------------------------------------------------------


def subjectAttendance_practical(year, division, subject, batch, sdate, edate):
    ap_btech = mysql.connector.connect(
        user='root', password='', host='localhost', database='practical_btech')
    ap_ty = mysql.connector.connect(
        user='root', password='', host='localhost', database='practical_ty')
    ap_sy = mysql.connector.connect(
        user='root', password='', host='localhost', database='practical_sy')
    btechP = ap_btech.cursor()
    tyP = ap_ty.cursor()
    syP = ap_sy.cursor()

    total = {}
    sdate = list(map(int, sdate.split('-')))
    edate = list(map(int, edate.split('-')))
    sdate = date(sdate[0], sdate[1], sdate[2])
    edate = date(edate[0], edate[1], edate[2])
    a = [sdate+timedelta(days=x) for x in range((edate-sdate).days)]
    dates = []
    for i in a:
        ss = i.strftime("%Y_%m_%d")
        dates.append(ss)

    if year == 'BTECH':
        try:
            sql = 'SELECT roll,name,division,batch FROM `' + \
                subject+'` WHERE batch = "{}"'.format(batch)
            btechP.execute(sql)
            data = btechP.fetchall()
        except:
            print('subject is not in the perticular year')
            total['pre'] = [year, division, subject]
            return total

        row = []
        for i in data:
            row.append(list(i))
        total['roll'] = row

        new_dates = []
        for i in dates:
            try:
                sql = 'SELECT {} FROM `{}` WHERE batch = "{}"'.format(
                    i, subject, batch)
                btechP.execute(sql)
                data = btechP.fetchall()
                # print(data)
                if data[0][0] != -1:
                    total[i] = data
                    new_dates.append(i)
            except:
                print('except')

        total['dates'] = new_dates

        for i in range(len(total['dates'])):
            for j in range(len(total['roll'])):
                total['roll'][j].append(total[total['dates'][i]][j][0])

        total['pre'] = [year, division, subject, batch, sdate, edate]

    elif year == "TY":
        try:
            sql = 'SELECT roll,name,division,batch FROM `' + \
                subject+'` WHERE batch = "{}"'.format(batch)
            tyP.execute(sql)
            data = tyP.fetchall()
        except:
            print('subject is not in the perticular year')
            total['pre'] = [year, division, subject]
            return total

        row = []
        for i in data:
            row.append(list(i))
        total['roll'] = row

        new_dates = []
        for i in dates:
            try:
                sql = 'SELECT {} FROM `{}` WHERE batch = "{}"'.format(
                    i, subject, batch)
                tyP.execute(sql)
                data = tyP.fetchall()
                # print(data)
                if data[0][0] != -1:
                    total[i] = data
                    new_dates.append(i)
            except:
                print('except')

        total['dates'] = new_dates

        for i in range(len(total['dates'])):
            for j in range(len(total['roll'])):
                total['roll'][j].append(total[total['dates'][i]][j][0])

        total['pre'] = [year, division, subject, batch, sdate, edate]

    elif year == "SY":
        try:
            sql = 'SELECT roll,name,division,batch FROM `' + \
                subject+'` WHERE batch = "{}"'.format(batch)
            syP.execute(sql)
            data = syP.fetchall()
        except:
            print('subject is not in the perticular year')
            total['pre'] = [year, division, subject]
            return total

        row = []
        for i in data:
            row.append(list(i))
        total['roll'] = row

        new_dates = []
        for i in dates:
            try:
                sql = 'SELECT {} FROM `{}` WHERE batch = "{}"'.format(
                    i, subject, batch)
                syP.execute(sql)
                data = syP.fetchall()
                # print(data)
                if data[0][0] != -1:
                    total[i] = data
                    new_dates.append(i)
            except:
                print('except')

        total['dates'] = new_dates

        for i in range(len(total['dates'])):
            for j in range(len(total['roll'])):
                total['roll'][j].append(total[total['dates'][i]][j][0])

        total['pre'] = [year, division, subject, batch, sdate, edate]

    ap_sy.close()
    ap_ty.close()
    ap_btech.close()

    return total

# for class attendance ------------------------------------------------------


def classAttendance(year, division, sdate, edate):
    at_btech = mysql.connector.connect(
        user='root', password='', host='localhost', database='theory_btech')
    at_ty = mysql.connector.connect(
        user='root', password='', host='localhost', database='theory_ty')
    at_sy = mysql.connector.connect(
        user='root', password='', host='localhost', database='theory_sy')
    btech = at_btech.cursor()
    ty = at_ty.cursor()
    sy = at_sy.cursor()

    ap_btech = mysql.connector.connect(
        user='root', password='', host='localhost', database='practical_btech')
    ap_ty = mysql.connector.connect(
        user='root', password='', host='localhost', database='practical_ty')
    ap_sy = mysql.connector.connect(
        user='root', password='', host='localhost', database='practical_sy')
    btechP = ap_btech.cursor()
    tyP = ap_ty.cursor()
    syP = ap_sy.cursor()

    fsub = open(fs, 'rb')
    subs = pickle.load(fsub)
    total = {}

    total['pre'] = [year, division, sdate, edate]
    sdate = list(map(int, sdate.split('-')))
    edate = list(map(int, edate.split('-')))
    sdate = date(sdate[0], sdate[1], sdate[2])
    edate = date(edate[0], edate[1], edate[2])
    a = [sdate+timedelta(days=x) for x in range((edate-sdate).days)]
    dates = []
    for i in a:
        ss = i.strftime("%Y_%m_%d")
        dates.append(ss)

    new_dates = []

    if year == 'BTECH':
        # for theory-----------------------------
        try:
            sub = subs['Theory'][year][0]
            sql = 'SELECT roll,name,division FROM `{}` WHERE division = "{}"'.format(
                sub, division)
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
            total['subs'].append(j)
            # print(j)
            for i in dates:
                try:
                    sql = 'SELECT {} FROM `{}` WHERE division = "{}"'.format(
                        i, j, division)
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
                    sql = 'SELECT {} FROM `{}` WHERE division = "{}"'.format(
                        i, j, division)
                    btechP.execute(sql)
                    data = btechP.fetchall()
                    # print(data)
                    for k in range(len(data)):
                        data[k] = data[k][0]
                    # print(data,i)

                    # for sessions happend storng in per subject list in total
                    for c in range(len(data)):
                        if len(total[j]) != len(data):
                            if data[c] == -1:
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
                if su[k] == -1:
                    # print(su[k])
                    total['roll'][k].append(0)
                else:
                    total['roll'][k].append(su[k])

    elif year == "TY":
        try:
            sub = subs['Theory'][year][0]
            sql = 'SELECT roll,name,division FROM `{}` WHERE division = "{}"'.format(
                sub, division)
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
        for j in subs['Theory'][year]:
            ll = []
            total['subs'].append(j)
            # print(j)
            for i in dates:
                try:
                    sql = 'SELECT {} FROM `{}` WHERE division = "{}"'.format(
                        i, j, division)
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

        # for practical ---------------------------------------------------
        for j in subs['Practical'][year]:
            ll = []
            total['subs'].append(j)
            # print(j)

            total[j] = []
            for i in dates:
                try:
                    sql = 'SELECT {} FROM `{}` WHERE division = "{}"'.format(
                        i, j, division)
                    tyP.execute(sql)
                    data = tyP.fetchall()
                    # print(data)
                    for k in range(len(data)):
                        data[k] = data[k][0]
                    # print(data,i)

                    # for sessions happend storng in per subject list in total
                    for c in range(len(data)):
                        if len(total[j]) != len(data):
                            if data[c] == -1:
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
                if su[k] == -1:
                    # print(su[k])
                    total['roll'][k].append(0)
                else:
                    total['roll'][k].append(su[k])

    elif year == "SY":
        try:
            sub = subs['Theory'][year][0]
            sql = 'SELECT roll,name,division FROM `{}` WHERE division = "{}"'.format(
                sub, division)
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
        for j in subs['Theory'][year]:
            ll = []
            total['subs'].append(j)
            # print(j)
            for i in dates:
                try:
                    sql = 'SELECT {} FROM `{}` WHERE division = "{}"'.format(
                        i, j, division)
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

        # for practical ---------------------------------------------------
        for j in subs['Practical'][year]:
            ll = []
            total['subs'].append(j)
            # print(j)

            total[j] = []
            for i in dates:
                try:
                    sql = 'SELECT {} FROM `{}` WHERE division = "{}"'.format(
                        i, j, division)
                    syP.execute(sql)
                    data = syP.fetchall()
                    # print(data)
                    for k in range(len(data)):
                        data[k] = data[k][0]
                    # print(data,i)

                    # for sessions happend storng in per subject list in total
                    for c in range(len(data)):
                        if len(total[j]) != len(data):
                            if data[c] == -1:
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
                if su[k] == -1:
                    # print(su[k])
                    total['roll'][k].append(0)
                else:
                    total['roll'][k].append(su[k])

    at_btech.close()
    at_sy.close()
    at_ty.close()

    ap_btech.close()
    ap_sy.close()
    ap_ty.close()
    # print(new_dates)
    # print(total)
    return total


def defaulterData(year, division, sdate, edate, defaulter):
    at_btech = mysql.connector.connect(
        user='root', password='', host='localhost', database='theory_btech')
    at_ty = mysql.connector.connect(
        user='root', password='', host='localhost', database='theory_ty')
    at_sy = mysql.connector.connect(
        user='root', password='', host='localhost', database='theory_sy')
    btech = at_btech.cursor()
    ty = at_ty.cursor()
    sy = at_sy.cursor()

    ap_btech = mysql.connector.connect(
        user='root', password='', host='localhost', database='practical_btech')
    ap_ty = mysql.connector.connect(
        user='root', password='', host='localhost', database='practical_ty')
    ap_sy = mysql.connector.connect(
        user='root', password='', host='localhost', database='practical_sy')
    btechP = ap_btech.cursor()
    tyP = ap_ty.cursor()
    syP = ap_sy.cursor()

    fsub = open(fs, 'rb')
    subs = pickle.load(fsub)
    total = {}
    total['pre'] = [year, division, sdate, edate]
    sdate = list(map(int, sdate.split('-')))
    edate = list(map(int, edate.split('-')))
    sdate = date(sdate[0], sdate[1], sdate[2])
    edate = date(edate[0], edate[1], edate[2])
    a = [sdate+timedelta(days=x) for x in range((edate-sdate).days)]
    dates = []
    for i in a:
        ss = i.strftime("%Y_%m_%d")
        dates.append(ss)

    new_dates = []

    if year == 'BTECH':
        # for theory----------------------------------
        try:
            sub = subs['Theory'][year][0]
            sql = 'SELECT roll,name,division FROM `{}` WHERE division = "{}"'.format(
                sub, division)
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
        total['cnt'] = []

        supsdd = []

        for j in subs['Theory'][year]:
            ll = []
            dd = []
            # print(j)
            ss = j.split()
            sname = ''
            for i in ss:
                sname += i[0]

            total[sname] = 0
            for i in dates:
                try:
                    sql = 'SELECT {} FROM `{}` WHERE division = "{}"'.format(
                        i, j, division)
                    btech.execute(sql)
                    data = btech.fetchall()
                    temp = []
                    for cc in data:
                        temp.append(cc[0])

                    if any(tenz > 0 for tenz in temp):
                        for k in range(len(data)):
                            data[k] = data[k][0]
                        yay = []
                        for huh in data:
                            if huh == -1:
                                yay.append(-1)
                            elif huh != -1:
                                yay.append(0)
                        dd.append(yay)

                        for heh in range(len(data)):
                            if data[heh] == -1:
                                data[heh] = 0
                        ll.append(data)

                        if 'other attendance' not in j.lower():
                            total[sname] += 1
                except:
                    print('except')

            if total[sname] != 0 or 'other attendance' in j.lower():
                total['subs'].append(sname)
                su = [sum(x) for x in zip(*ll)]
                if len(su) == 0:
                    for l in range(len(total['roll'])):
                        su.append(0)
                sdd = [sum(x) for x in zip(*dd)]

                if len(sdd) == 0:
                    for l in range(len(total['roll'])):
                        sdd.append(0)

                if len(supsdd) == 0:
                    supsdd = sdd
                else:
                    supsdd = [sum(i) for i in zip(supsdd, sdd)]
                for k in range(len(total['roll'])):
                    total['roll'][k].append(su[k])

                total['cnt'].append(total[sname])
        print(supsdd)
        # For practical-------------------------------------------
        for j in subs['Practical'][year]:
            ll = []
            # print(j)
            ss = j.split()
            sname = ''
            for i in ss:
                if i[0] == '(':
                    sname += i[1]+i[2]
                    # print(sname)
                else:
                    sname += i[0]
            total[sname] = [0 for i in range(len(total['roll']))]

            for i in dates:
                try:
                    sql = 'SELECT {} FROM `{}` WHERE division = "{}"'.format(
                        i, j, division)
                    btechP.execute(sql)
                    data = btechP.fetchall()
                    for k in range(len(data)):
                        data[k] = data[k][0]

                    # for sessions happend storng in per subject list in total
                    for c in range(len(data)):
                        if len(total[sname]) != len(data):
                            if data[c] == -1:
                                pass
                            else:
                                total[sname][c] = 2
                        else:
                            if data[c] == -1:
                                pass
                            else:
                                total[sname][c] += 2
                    for kj in range(len(data)):
                        if data[kj] == -1:
                            data[kj] = 0

                    ll.append(data)
                except:
                    print('except')

            if any(i != 0 for i in total[sname]):
                # print(j, total[sname])
                total['subs'].append(sname)
                su = [sum(x) for x in zip(*ll)]
                # print('su',su)
                if len(su) == 0:
                    for l in range(len(total['roll'])):
                        su.append(0)

                for k in range(len(total['roll'])):
                    if su[k] == -1:
                        total['roll'][k].append(0)
                    else:
                        total['roll'][k].append(su[k])

        sess_count = [0 for i in range(len(total['roll']))]
        # print(sess_count)
        for j in subs['Theory'][year]:
            ss = j.split()
            sname = ''
            for i in ss:
                sname += i[0]
            for kk in range(len(sess_count)):
                sess_count[kk] += total[sname]
        # print(sess_count)
        for j in subs['Practical'][year]:
            ss = j.split()
            sname = ''
            for i in ss:
                if i[0] == '(':
                    sname += i[1]+i[2]
                    # print(sname)
                else:
                    sname += i[0]
            for kk in range(len(total['roll'])):
                # print(total[sname])
                sess_count[kk] += total[sname][kk]

        # new ----------------
        # for i in range(len(total['roll'])):
        #     # print(total['roll'][i])
        #     for jcb in range(3, len(total['roll'][i])):
        #         if total['roll'][i][jcb] < 0:
        #             # print(total['roll'][i][jcb])
        #             sess_count[i] += total['roll'][i][jcb]
            # print(sess_count[i])

        # Session Attended
        for i in range(len(total['roll'])):
            # print(total['roll'][i])
            cnt = 0
            for j in range(3, len(total['roll'][i])):
                cnt += total['roll'][i][j]
            percentage = 0
            sess_count[i] += supsdd[i]
            try:
                percentage = (cnt/sess_count[i])*100
                percentage = round(percentage, 2)
                if percentage > 100:
                    percentage = 100.0
                    cnt = sess_count[i]
            except:
                print('division error')

            total['roll'][i].append(cnt)
            total['roll'][i].append(sess_count[i])
            total['roll'][i].append(percentage)

        # attendance percentage

        total['subs'].append('Session Attended')
        total['subs'].append('Total Sessions')
        total['subs'].append('Attendance Percentage')
        total['defaulter'] = int(defaulter)

    elif year == "TY":
        # for theory----------------------------------
        try:
            sub = subs['Theory'][year][0]
            sql = 'SELECT roll,name,division FROM `{}` WHERE division = "{}"'.format(
                sub, division)
            ty.execute(sql)
            data = ty.fetchall()
        except:
            print('no subject')
            data = []
        row = []
        for i in data:
            row.append(list(i))
        total['roll'] = row
        total['subs'] = []

        for j in subs['Theory'][year]:
            ll = []
            ss = j.split()
            sname = ''
            for i in ss:
                sname += i[0]
            total['subs'].append(sname)
            total[sname] = 0
            for i in dates:
                try:
                    sql = 'SELECT {} FROM `{}` WHERE division = "{}"'.format(
                        i, j, division)
                    ty.execute(sql)
                    data = ty.fetchall()
                    temp = []
                    for cc in data:
                        temp.append(cc[0])

                    if any(tenz > 0 for tenz in temp):
                        for k in range(len(data)):
                            data[k] = data[k][0]
                        ll.append(data)
                        if j != 'other attendance':
                            total[sname] += 1
                except:
                    print('except')

            if total[sname] != 0:
                total['subs'].append(sname)
                su = [sum(x) for x in zip(*ll)]
                if len(su) == 0:
                    for l in range(len(total['roll'])):
                        su.append(0)
                # print('su',su)

                for k in range(len(total['roll'])):
                    if su[k] == -1:
                        total['roll'][k].append(0)
                    else:
                        total['roll'][k].append(su[k])

        # For practical-------------------------------------------
        for j in subs['Practical'][year]:
            ll = []
            # print(j)
            ss = j.split()
            sname = ''
            for i in ss:
                sname += i[0]
            total['subs'].append(sname)
            total[sname] = [0 for i in range(len(total['roll']))]
            for i in dates:
                try:
                    sql = 'SELECT {} FROM `{}` WHERE division = "{}"'.format(
                        i, j, division)
                    tyP.execute(sql)
                    data = tyP.fetchall()
                    for k in range(len(data)):
                        data[k] = data[k][0]

                    # for sessions happend storng in per subject list in total
                    for c in range(len(data)):
                        if len(total[sname]) != len(data):
                            if data[c] == -1:
                                pass
                            else:
                                total[sname][c] = 2
                        else:
                            if data[c] == -1:
                                pass
                            else:
                                total[sname][c] += 2
                    for kj in range(len(data)):
                        if data[kj] == -1:
                            data[kj] = 0

                    ll.append(data)
                except:
                    print('except')
            su = [sum(x) for x in zip(*ll)]
            if len(su) == 0:
                for l in range(len(total['roll'])):
                    su.append(0)

            for k in range(len(total['roll'])):
                if su[k] == -1:
                    total['roll'][k].append(0)
                else:
                    total['roll'][k].append(su[k])

        sess_count = [0 for i in range(len(total['roll']))]
        for j in subs['Theory'][year]:
            ss = j.split()
            sname = ''
            for i in ss:
                sname += i[0]
            for kk in range(len(sess_count)):
                sess_count[kk] += total[sname]

        for j in subs['Practical'][year]:
            ss = j.split()
            sname = ''
            for i in ss:
                if i[0] == '(':
                    sname += i[1]+i[2]
                    # print(sname)
                else:
                    sname += i[0]
            for kk in range(len(total['roll'])):
                print(total[sname])
                sess_count[kk] += total[sname][kk]

        # Session Attended
        for i in range(len(total['roll'])):
            cnt = 0
            for j in range(3, len(total['roll'][i])):
                cnt += total['roll'][i][j]
            percentage = 0
            try:
                percentage = (cnt/sess_count[i])*100
                percentage = round(percentage, 2)
            except:
                print('division error')

            total['roll'][i].append(cnt)
            total['roll'][i].append(sess_count[i])
            total['roll'][i].append(percentage)

        # attendance percentage

        total['subs'].append('Session Attended')
        total['subs'].append('Total Sessions')
        total['subs'].append('Attendance Percentage')
        total['defaulter'] = int(defaulter)

    elif year == "SY":
        # for theory----------------------------------
        try:
            sub = subs['Theory'][year][0]
            sql = 'SELECT roll,name,division FROM `{}` WHERE division = "{}"'.format(
                sub, division)
            sy.execute(sql)
            data = sy.fetchall()
        except:
            print('no subject')
            data = []
        row = []
        for i in data:
            row.append(list(i))
        total['roll'] = row
        total['subs'] = []

        for j in subs['Theory'][year]:
            ll = []
            ss = j.split()
            sname = ''
            for i in ss:
                sname += i[0]
            total['subs'].append(sname)
            total[sname] = 0
            for i in dates:
                try:
                    sql = 'SELECT {} FROM `{}` WHERE division = "{}"'.format(
                        i, j, division)
                    sy.execute(sql)
                    data = sy.fetchall()
                    print(data)
                    if data[0][0] != -1:
                        total[sname] += 1
                        print(data)
                        for k in range(len(data)):
                            data[k] = data[k][0]
                        ll.append(data)
                except:
                    print('except')

            su = [sum(x) for x in zip(*ll)]
            if len(su) == 0:
                for l in range(len(total['roll'])):
                    su.append(0)

            for k in range(len(total['roll'])):
                total['roll'][k].append(su[k])

        # For practical-------------------------------------------
        for j in subs['Practical'][year]:
            ll = []
            # print(j)
            ss = j.split()
            sname = ''
            for i in ss:
                sname += i[0]
            total['subs'].append(sname)
            total[sname] = [0 for i in range(len(total['roll']))]
            for i in dates:
                try:
                    sql = 'SELECT {} FROM `{}` WHERE division = "{}"'.format(
                        i, j, division)
                    syP.execute(sql)
                    data = syP.fetchall()
                    for k in range(len(data)):
                        data[k] = data[k][0]

                    # for sessions happend storng in per subject list in total
                    for c in range(len(data)):
                        if len(total[sname]) != len(data):
                            if data[c] == -1:
                                pass
                            else:
                                total[sname][c] = 2
                        else:
                            if data[c] == -1:
                                pass
                            else:
                                total[sname][c] += 2
                    for kj in range(len(data)):
                        if data[kj] == -1:
                            data[kj] = 0

                    ll.append(data)
                except:
                    print('except')
            su = [sum(x) for x in zip(*ll)]
            if len(su) == 0:
                for l in range(len(total['roll'])):
                    su.append(0)

            for k in range(len(total['roll'])):
                if su[k] == -1:
                    total['roll'][k].append(0)
                else:
                    total['roll'][k].append(su[k])

        sess_count = [0 for i in range(len(total['roll']))]
        for j in subs['Theory'][year]:
            ss = j.split()
            sname = ''
            for i in ss:
                sname += i[0]
            for kk in range(len(sess_count)):
                sess_count[kk] += total[sname]

        for j in subs['Practical'][year]:
            ss = j.split()
            sname = ''
            for i in ss:
                sname += i[0]
            for kk in range(len(total['roll'])):
                print(total[sname])
                sess_count[kk] += total[sname][kk]

        # Session Attended
        for i in range(len(total['roll'])):
            cnt = 0
            for j in range(3, len(total['roll'][i])):
                cnt += total['roll'][i][j]
            percentage = 0
            try:
                percentage = (cnt/sess_count[i])*100
                percentage = round(percentage, 2)
            except:
                print('division error')

            total['roll'][i].append(cnt)
            total['roll'][i].append(sess_count[i])
            total['roll'][i].append(percentage)

        # attendance percentage

        total['subs'].append('Session Attended')
        total['subs'].append('Total Sessions')
        total['subs'].append('Attendance Percentage')
        total['defaulter'] = int(defaulter)

    at_btech.close()
    at_sy.close()
    at_ty.close()

    ap_btech.close()
    ap_sy.close()
    ap_ty.close()

    # print(total)
    return total
