import pandas as pd
import mysql.connector
from datetime import date, timedelta
import pickle

fs = 'subinfo.pkl'

def studenttAttendance_theory(roll,year,subject):
    at_btech = mysql.connector.connect(user='root', password='', host='localhost', database='theory_btech')
    at_ty = mysql.connector.connect(user='root', password='', host='localhost', database='theory_ty')
    at_sy = mysql.connector.connect(user='root', password='', host='localhost', database='theory_sy')

    btech = at_btech.cursor()
    ty = at_ty.cursor()
    sy = at_sy.cursor()

    total ={}

    if year == 'BTECH':
        attendance = {}
        try:
            sql = 'SELECT * FROM `{}` WHERE roll = "{}"'.format(subject,roll)
            btech.execute(sql)
            data = btech.fetchall()
            data = list(data[0][3:])
            sql = "SHOW COLUMNS FROM `{}`".format(subject)
            btech.execute(sql)
            col = btech.fetchall()
            column = []
            for k in col:
                column.append(k[0])
            column = column[3:]
            # print(data,column)
        except:
            print('except')
        
        for i in range(len(column)):
            if data[i] == 1:
                attendance[column[i]] = 'Present'
            elif data[i] == 0:
                attendance[column[i]] = 'Absent'
            else:
                pass
        total['col'] = []
        total['attendance'] = []

        for i,j in attendance.items():
            total['col'].append(i)
            total['attendance'].append(j)
    
    elif year == 'TY':
        attendance = {}
        try:
            sql = 'SELECT * FROM `{}` WHERE roll = "{}"'.format(subject,roll)
            ty.execute(sql)
            data = ty.fetchall()
            data = list(data[0][3:])
            sql = "SHOW COLUMNS FROM `{}`".format(subject)
            ty.execute(sql)
            col = ty.fetchall()
            column = []
            for k in col:
                column.append(k[0])
            column = column[3:]
            # print(data,column)
        except:
            print('except')
        
        for i in range(len(column)):
            if data[i] == 1:
                attendance[column[i]] = 'Present'
            elif data[i] == 0:
                attendance[column[i]] = 'Absent'
            else:
                pass
        total['col'] = []
        total['attendance'] = []

        for i,j in attendance.items():
            total['col'].append(i)
            total['attendance'].append(j)
    
    elif year == 'SY':
        attendance = {}
        try:
            sql = 'SELECT * FROM `{}` WHERE roll = "{}"'.format(subject,roll)
            sy.execute(sql)
            data = sy.fetchall()
            data = list(data[0][3:])
            sql = "SHOW COLUMNS FROM `{}`".format(subject)
            sy.execute(sql)
            col = sy.fetchall()
            column = []
            for k in col:
                column.append(k[0])
            column = column[3:]
            # print(data,column)
        except:
            print('except')
        
        for i in range(len(column)):
            if data[i] == 1:
                attendance[column[i]] = 'Present'
            elif data[i] == 0:
                attendance[column[i]] = 'Absent'
            else:
                pass
        total['col'] = []
        total['attendance'] = []

        for i,j in attendance.items():
            total['col'].append(i)
            total['attendance'].append(j)

    at_sy.close()
    at_ty.close()
    at_btech.close()
    print(total)
    return total
    
def studenttAttendance_practical(roll,year,subject):
    ap_btech = mysql.connector.connect(user='root', password='', host='localhost', database='practical_btech')
    ap_ty = mysql.connector.connect(user='root', password='', host='localhost', database='practical_ty')
    ap_sy = mysql.connector.connect(user='root', password='', host='localhost', database='practical_sy')
    btechP = ap_btech.cursor()
    tyP = ap_ty.cursor()
    syP = ap_sy.cursor()

    total ={}

    if year == 'BTECH':
        attendance = {}
        try:
            sql = 'SELECT * FROM `{}` WHERE roll = "{}"'.format(subject,roll)
            btechP.execute(sql)
            data = btechP.fetchall()
            data = list(data[0][4:])
            sql = "SHOW COLUMNS FROM `{}`".format(subject)
            btechP.execute(sql)
            col = btechP.fetchall()
            column = []
            for k in col:
                column.append(k[0])
            column = column[4:]
            # print(data,column)
        except:
            print('except')
        
        for i in range(len(column)):
            # print(data[i])
            if data[i] == 2:
                attendance[column[i]] = 'Present'
            elif data[i] == 0:
                attendance[column[i]] = 'Absent'
            else:
                pass
        total['col'] = []
        total['attendance'] = []

        for i,j in attendance.items():
            total['col'].append(i)
            total['attendance'].append(j)

    elif year == 'TY':
        attendance = {}
        try:
            sql = 'SELECT * FROM `{}` WHERE roll = "{}"'.format(subject,roll)
            tyP.execute(sql)
            data = tyP.fetchall()
            data = list(data[0][4:])
            sql = "SHOW COLUMNS FROM `{}`".format(subject)
            tyP.execute(sql)
            col = tyP.fetchall()
            column = []
            for k in col:
                column.append(k[0])
            column = column[4:]
            # print(data,column)
        except:
            print('except')
        
        for i in range(len(column)):
            # print(data[i])
            if data[i] == 2:
                attendance[column[i]] = 'Present'
            elif data[i] == 0:
                attendance[column[i]] = 'Absent'
            else:
                pass
        total['col'] = []
        total['attendance'] = []

        for i,j in attendance.items():
            total['col'].append(i)
            total['attendance'].append(j)
    
    elif year == 'SY':
        attendance = {}
        try:
            sql = 'SELECT * FROM `{}` WHERE roll = "{}"'.format(subject,roll)
            syP.execute(sql)
            data = syP.fetchall()
            data = list(data[0][4:])
            sql = "SHOW COLUMNS FROM `{}`".format(subject)
            syP.execute(sql)
            col = syP.fetchall()
            column = []
            for k in col:
                column.append(k[0])
            column = column[4:]
            # print(data,column)
        except:
            print('except')
        
        for i in range(len(column)):
            # print(data[i])
            if data[i] == 2:
                attendance[column[i]] = 'Present'
            elif data[i] == 0:
                attendance[column[i]] = 'Absent'
            else:
                pass
        total['col'] = []
        total['attendance'] = []

        for i,j in attendance.items():
            total['col'].append(i)
            total['attendance'].append(j)

    print(total)
    ap_sy.close()
    ap_ty.close()
    ap_btech.close()
    return total

def studenttAttendance_defaulter(roll,year) :
    at_btech = mysql.connector.connect(user='root', password='', host='localhost', database='theory_btech')
    at_ty = mysql.connector.connect(user='root', password='', host='localhost', database='theory_ty')
    at_sy = mysql.connector.connect(user='root', password='', host='localhost', database='theory_sy')
    btech = at_btech.cursor()
    ty = at_ty.cursor()
    sy = at_sy.cursor()

    ap_btech = mysql.connector.connect(user='root', password='', host='localhost', database='practical_btech')
    ap_ty = mysql.connector.connect(user='root', password='', host='localhost', database='practical_ty')
    ap_sy = mysql.connector.connect(user='root', password='', host='localhost', database='practical_sy')
    btechP = ap_btech.cursor()
    tyP = ap_ty.cursor()
    syP = ap_sy.cursor()

    fsub = open(fs,'rb')
    subs = pickle.load(fsub)
    total = {}

    if year=='BTECH':
        # for theory
        total['subs'] = []
        total['row'] = []
        total['sessios_happend'] = []
        total['sessios_attended'] = []
        for i in subs['Theory'][year]:
            ll = []
            # print(j)
            ss = i.split()
            sname = ''
            for j in ss:
                sname+=j[0]
            total['subs'].append(sname)
            total[sname] = 0

            sql = "SHOW COLUMNS FROM `{}`".format(i)
            btech.execute(sql)
            col = btech.fetchall()
            column = []
            for k in col:
                column.append(k[0])
            column = column[3:]

            attended = 0
            for j in column:
                sql = 'SELECT {} FROM `{}` WHERE roll = "{}"'.format(j,i,roll)
                btech.execute(sql)
                data = btech.fetchall()
                # print(i,j,data)
                if data[0][0] != -1:
                    attended+=data[0][0]
                    total[sname] +=1  
            total['sessios_attended'].append(attended)
            total['sessios_happend'].append(total[sname])
        
        # for practical 
        for j in subs['Practical'][year]:
            ll = []
            # print(j)
            ss = j.split()
            sname = ''
            for i in ss:
                if i[0]=='(':
                    sname+=i[1]+i[2]
                    # print(sname)
                else:
                    sname+=i[0]
            total['subs'].append(sname)
            total[sname] = 0
            sql = "SHOW COLUMNS FROM `{}`".format(j)
            btechP.execute(sql)
            col = btechP.fetchall()
            column = []
            for k in col:
                column.append(k[0])
            column = column[4:]
            
            attended = 0
            for i in column:
                sql = 'SELECT `{}` FROM `{}` WHERE roll = "{}"'.format(i,j,roll)
                btechP.execute(sql)
                data = btechP.fetchall()
                # print(data)
                # print(j,data)
                if data[0][0] == -1:
                    pass
                else:
                    total[sname] += 2
                    attended+=data[0][0]
            # print(j,column)
            total['sessios_attended'].append(attended)
            total['sessios_happend'].append(total[sname])

        # session count 
        sess_count = [0]
        for j in subs['Theory'][year]:
            ss = j.split()
            sname = ''
            for i in ss:
                sname+=i[0]
            sess_count[0] += total[sname]

        for j in subs['Practical'][year]:
            ss = j.split()
            sname = ''
            for i in ss:
                if i[0]=='(':
                    sname+=i[1]+i[2]
                    # print(sname)
                else:
                    sname+=i[0]
                # print(total[sname])
            sess_count[0] += total[sname]
        
        # print(sess_count)
        session_happend = sum(total['sessios_happend'])
        session_attended = sum(total['sessios_attended'])
        percentage = (session_attended/session_happend)*100
        percentage = round(percentage,2)
        # print(percentage)
        total['sessios_happend'].append(session_happend)
        total['sessios_attended'].append(session_attended)
        total['sessios_happend'].append(100)
        total['sessios_attended'].append(percentage)
        total['subs'].append('Sessions Count')
        total['subs'].append('Percentage')

        return total
            
    elif year == "TY":
        # for theory
        total['subs'] = []
        total['row'] = []
        total['sessios_happend'] = []
        total['sessios_attended'] = []
        for i in subs['Theory'][year]:
            ll = []
            # print(j)
            ss = i.split()
            sname = ''
            for j in ss:
                sname+=j[0]
            total['subs'].append(sname)
            total[sname] = 0

            sql = "SHOW COLUMNS FROM `{}`".format(i)
            ty.execute(sql)
            col = ty.fetchall()
            column = []
            for k in col:
                column.append(k[0])
            column = column[3:]

            attended = 0
            for j in column:
                sql = 'SELECT {} FROM `{}` WHERE roll = "{}"'.format(j,i,roll)
                ty.execute(sql)
                data = ty.fetchall()
                # print(i,j,data)
                if data[0][0] != -1:
                    attended+=data[0][0]
                    total[sname] +=1  
            total['sessios_attended'].append(attended)
            total['sessios_happend'].append(total[sname])
        
        # for practical 
        for j in subs['Practical'][year]:
            ll = []
            # print(j)
            ss = j.split()
            sname = ''
            for i in ss:
                if i[0]=='(':
                    sname+=i[1]+i[2]
                    # print(sname)
                else:
                    sname+=i[0]
            total['subs'].append(sname)
            total[sname] = 0
            sql = "SHOW COLUMNS FROM `{}`".format(j)
            tyP.execute(sql)
            col = tyP.fetchall()
            column = []
            for k in col:
                column.append(k[0])
            column = column[4:]
            
            attended = 0
            for i in column:
                sql = 'SELECT `{}` FROM `{}` WHERE roll = "{}"'.format(i,j,roll)
                tyP.execute(sql)
                data = tyP.fetchall()
                # print(data)
                # print(j,data)
                if data[0][0] == -1:
                    pass
                else:
                    total[sname] += 2
                    attended+=data[0][0]
            # print(j,column)
            total['sessios_attended'].append(attended)
            total['sessios_happend'].append(total[sname])

        # session count 
        sess_count = [0]
        for j in subs['Theory'][year]:
            ss = j.split()
            sname = ''
            for i in ss:
                sname+=i[0]
            sess_count[0] += total[sname]

        for j in subs['Practical'][year]:
            ss = j.split()
            sname = ''
            for i in ss:
                if i[0]=='(':
                    sname+=i[1]+i[2]
                    # print(sname)
                else:
                    sname+=i[0]
                # print(total[sname])
            sess_count[0] += total[sname]
        
        # print(sess_count)
        session_happend = sum(total['sessios_happend'])
        session_attended = sum(total['sessios_attended'])
        percentage = (session_attended/session_happend)*100
        percentage = round(percentage,2)
        # print(percentage)
        total['sessios_happend'].append(session_happend)
        total['sessios_attended'].append(session_attended)
        total['sessios_happend'].append(100)
        total['sessios_attended'].append(percentage)
        total['subs'].append('Sessions Count')
        total['subs'].append('Percentage')

        return total

    elif year == "SY":
        # for theory
        total['subs'] = []
        total['row'] = []
        total['sessios_happend'] = []
        total['sessios_attended'] = []
        for i in subs['Theory'][year]:
            ll = []
            # print(j)
            ss = i.split()
            sname = ''
            for j in ss:
                sname+=j[0]
            total['subs'].append(sname)
            total[sname] = 0

            sql = "SHOW COLUMNS FROM `{}`".format(i)
            sy.execute(sql)
            col = sy.fetchall()
            column = []
            for k in col:
                column.append(k[0])
            column = column[3:]

            attended = 0
            for j in column:
                sql = 'SELECT {} FROM `{}` WHERE roll = "{}"'.format(j,i,roll)
                sy.execute(sql)
                data = sy.fetchall()
                # print(i,j,data)
                if data[0][0] != -1:
                    attended+=data[0][0]
                    total[sname] +=1  
            total['sessios_attended'].append(attended)
            total['sessios_happend'].append(total[sname])
        
        # for practical 
        for j in subs['Practical'][year]:
            ll = []
            # print(j)
            ss = j.split()
            sname = ''
            for i in ss:
                if i[0]=='(':
                    sname+=i[1]+i[2]
                    # print(sname)
                else:
                    sname+=i[0]
            total['subs'].append(sname)
            total[sname] = 0
            sql = "SHOW COLUMNS FROM `{}`".format(j)
            syP.execute(sql)
            col = syP.fetchall()
            column = []
            for k in col:
                column.append(k[0])
            column = column[4:]
            
            attended = 0
            for i in column:
                sql = 'SELECT `{}` FROM `{}` WHERE roll = "{}"'.format(i,j,roll)
                syP.execute(sql)
                data = syP.fetchall()
                # print(data)
                # print(j,data)
                if data[0][0] == -1:
                    pass
                else:
                    total[sname] += 2
                    attended+=data[0][0]
            # print(j,column)
            total['sessios_attended'].append(attended)
            total['sessios_happend'].append(total[sname])

        # session count 
        sess_count = [0]
        for j in subs['Theory'][year]:
            ss = j.split()
            sname = ''
            for i in ss:
                sname+=i[0]
            sess_count[0] += total[sname]

        for j in subs['Practical'][year]:
            ss = j.split()
            sname = ''
            for i in ss:
                if i[0]=='(':
                    sname+=i[1]+i[2]
                    # print(sname)
                else:
                    sname+=i[0]
                # print(total[sname])
            sess_count[0] += total[sname]
        
        # print(sess_count)
        session_happend = sum(total['sessios_happend'])
        session_attended = sum(total['sessios_attended'])
        percentage = (session_attended/session_happend)*100
        percentage = round(percentage,2)
        # print(percentage)
        total['sessios_happend'].append(session_happend)
        total['sessios_attended'].append(session_attended)
        total['sessios_happend'].append(100)
        total['sessios_attended'].append(percentage)
        total['subs'].append('Sessions Count')
        total['subs'].append('Percentage')

        return total