import pandas as pd
# import connection as cn
from routes import mysql_stud
import mysql.connector


def addOtherAttendance(data, count, roll):
    at_btech = mysql.connector.connect(
        user='root', password='', host='localhost', database='theory_btech')
    at_ty = mysql.connector.connect(
        user='root', password='', host='localhost', database='theory_ty')
    at_sy = mysql.connector.connect(
        user='root', password='', host='localhost', database='theory_sy')

    btech = at_btech.cursor()
    ty = at_ty.cursor()
    sy = at_sy.cursor()

    for i in range(len(count)):
        count[i] = int(count[i])

    print(data, count, roll)
    if data[0] == "BTECH":
        date = data[2].replace('-', '_')
        try:
            for i in roll:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(
                    data[3], date, i)
                btech.execute(sql)
                at_btech.commit()

            for i in range(len(roll)):
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}={} WHERE roll={} ".format(
                    data[3], date, count[i], roll[i])
                btech.execute(sql)
                at_btech.commit()

        except:
            print('already exist')

            sql = 'ALTER TABLE `{}` ADD {} int DEFAULT -1'.format(
                data[3], date)
            btech.execute(sql)
            at_btech.commit()

            for i in roll:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(
                    data[3], date, i)
                btech.execute(sql)
                at_btech.commit()

            for i in range(len(roll)):
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}={} WHERE roll={} ".format(
                    data[3], date, count[i], roll[i])
                btech.execute(sql)
                at_btech.commit()
        at_btech.close()


def addattendance_daily(data, present, roll, torp):
    dcse = mysql.connector.connect(
        user='root', password='', host='localhost', database='daily_cse')
    dcse_cur = dcse.cursor()
    cur = mysql_stud.connection.cursor()

    year = data[0]
    div = data[1]
    date = data[2]
    sub = data[3]
    time = data[4]
    batch = data[5]
    tableName = date+'-'+year+'-'+div

    sub = sub.split()
    sname = ''
    for i in sub:
        if i[0] == '(':
            sname += i[1]+i[2]
            # print(sname)
        else:
            sname += i[0]

    tt = {'8:00': 3,
          '9:00': 4,
          '10:15': 5,
          '11:15': 6,
          '1:15': 7,
          '2:15': 8,
          '3:30': 9,
          '4:30': 10}

    print(year, div, date, sub, time, batch, tableName, torp)

    if year == 'BTECH':
        sql = "SHOW TABLES LIKE '%{}%'".format(tableName)
        dcse_cur.execute(sql)
        table_exist = dcse_cur.fetchall()
        total = {}

        if table_exist:
            print('table exist')

            sql = "SHOW COLUMNS FROM `{}`".format(tableName)
            dcse_cur.execute(sql)
            cn = dcse_cur.fetchall()
            col = []
            for kk in cn:
                col.append(kk[0])
                # print(kk[0])
            if torp == "Theory":
                for i in roll:
                    sql = "UPDATE `{}` SET `{}`=0 WHERE roll=%s ".format(
                        tableName, col[tt[time]])
                    val = (i,)
                    dcse_cur.execute(sql, val)
                    dcse.commit()

                for i in present:
                    sql = "UPDATE `{}` SET `{}`=1 WHERE roll=%s ".format(
                        tableName, col[tt[time]])
                    val = (i,)
                    dcse_cur.execute(sql, val)
                    dcse.commit()

                # rename time column name
                try:
                    newcolumn = time+' ('+sname+')'
                    print(newcolumn)
                    sql = 'ALTER TABLE `{}` CHANGE `{}` `{}` INT(11) NOT NULL DEFAULT "-1"'.format(
                        tableName, col[tt[time]], newcolumn)
                    dcse_cur.execute(sql)
                    dcse.commit()
                except:
                    print('column name not exixt')

            elif torp == "Practical":
                print('practical')
                for i in roll:
                    sql = "UPDATE `{}` SET `{}`=0 WHERE roll=%s ".format(
                        tableName, col[tt[time]])
                    val = (i,)
                    dcse_cur.execute(sql, val)
                    dcse.commit()

                    sql = "UPDATE `{}` SET `{}`=0 WHERE roll=%s ".format(
                        tableName, col[tt[time]+1])
                    val = (i,)
                    dcse_cur.execute(sql, val)
                    dcse.commit()

                    sql = "UPDATE `{}` SET `prsub`='{}' WHERE roll = %s".format(
                        tableName, sname)
                    val = (i,)
                    dcse_cur.execute(sql, val)
                    dcse.commit()

                for i in present:
                    sql = "UPDATE `{}` SET `{}`=2 WHERE roll=%s ".format(
                        tableName, col[tt[time]])
                    val = (i,)
                    dcse_cur.execute(sql, val)
                    dcse.commit()
                for i in present:
                    sql = "UPDATE `{}` SET `{}`=2 WHERE roll=%s ".format(
                        tableName, col[tt[time]+1])
                    val = (i,)
                    dcse_cur.execute(sql, val)
                    dcse.commit()

                # rename time column name
                try:
                    newcolumn = time+'(pr)'
                    # print(newcolumn)
                    sql = 'ALTER TABLE `{}` CHANGE `{}` `{}` INT(11) NOT NULL DEFAULT "-1"'.format(
                        tableName, col[tt[time]], newcolumn)
                    dcse_cur.execute(sql)
                    dcse.commit()

                    # times = list(tt.keys())
                    # index = list(tt.values())
                    # p = tt[time]+1
                    # posi = index.index(p)
                    # print(times[posi])

                    # if col[tt[time]+1] == times[posi]:
                    #     sql = "ALTER TABLE `{}` DROP `{}`".format(tableName,col[tt[time]+1])
                    #     dcse_cur.execute(sql)
                    #     dcse.commit()

                except:
                    print('column name not exixt')

        else:
            print('table not exist')
            sql = "CREATE TABLE `{}` (`roll` INT NOT NULL , `name` TEXT NOT NULL , `prsub` TEXT NOT NULL , `8:00` INT NOT NULL DEFAULT '-1', `9:00` INT NOT NULL DEFAULT '-1' , `10:15` INT NOT NULL DEFAULT '-1' , `11:15` INT NOT NULL DEFAULT '-1' , `1:15` INT NOT NULL DEFAULT '-1' , `2:15` INT NOT NULL DEFAULT '-1' , `3:30` INT NOT NULL DEFAULT '-1' , `4:30` INT NOT NULL DEFAULT '-1' , `remark` TEXT NOT NULL ) ENGINE = InnoDB;".format(tableName)
            dcse_cur.execute(sql)

            total['data'] = []

            sql = "SELECT ROLL_NO FROM "+year+" WHERE DIVISION = %s"
            val = (div)
            cur.execute(sql, val)
            studroll = cur.fetchall()
            for k in range(len(studroll)):
                total['data'].append([studroll[k][0]])

            # get student name associated with roll
            sql = "SELECT NAME FROM "+year+" WHERE DIVISION = %s "
            val = (div)
            cur.execute(sql, val)
            studname = cur.fetchall()

            # print(len(studname))
            # print(studname)
            for k in range(len(studname)):
                total['data'][k].append(studname[k][0])
                # print(total['data'][k],studname[k][0])

            # print(total)
            # insert names and roll no in the table
            for k in range(len(total['data'])):
                # print(total['data'][k])
                sql = "INSERT INTO `{}` (`roll`, `name`) VALUES ('{}','{}')".format(
                    tableName, total['data'][k][0], total['data'][k][1])
                dcse_cur.execute(sql)
                dcse.commit()

            sql = "SHOW COLUMNS FROM `{}`".format(tableName)
            dcse_cur.execute(sql)
            cn = dcse_cur.fetchall()
            col = []
            for kk in cn:
                col.append(kk[0])
                # print(kk[0])
            if torp == "Theory":
                for i in roll:
                    sql = "UPDATE `{}` SET `{}`=0 WHERE roll=%s ".format(
                        tableName, col[tt[time]])
                    val = (i,)
                    dcse_cur.execute(sql, val)
                    dcse.commit()

                for i in present:
                    sql = "UPDATE `{}` SET `{}`=1 WHERE roll=%s ".format(
                        tableName, col[tt[time]])
                    val = (i,)
                    dcse_cur.execute(sql, val)
                    dcse.commit()

                # rename time column name
                try:
                    newcolumn = time+' ('+sname+')'
                    print(newcolumn)
                    sql = 'ALTER TABLE `{}` CHANGE `{}` `{}` INT(11) NOT NULL DEFAULT "-1"'.format(
                        tableName, col[tt[time]], newcolumn)
                    dcse_cur.execute(sql)
                    dcse.commit()
                except:
                    print('column name not exixt')

            elif torp == "Practical":
                print('practical')
                for i in roll:
                    sql = "UPDATE `{}` SET `{}`=0 WHERE roll=%s ".format(
                        tableName, col[tt[time]])
                    val = (i,)
                    dcse_cur.execute(sql, val)
                    dcse.commit()

                    sql = "UPDATE `{}` SET `{}`=0 WHERE roll=%s ".format(
                        tableName, col[tt[time]+1])
                    val = (i,)
                    dcse_cur.execute(sql, val)
                    dcse.commit()

                    sql = "UPDATE `{}` SET `prsub`='{}' WHERE roll = %s".format(
                        tableName, sname)
                    val = (i,)
                    dcse_cur.execute(sql, val)
                    dcse.commit()

                for i in present:
                    sql = "UPDATE `{}` SET `{}`=2 WHERE roll=%s ".format(
                        tableName, col[tt[time]])
                    val = (i,)
                    dcse_cur.execute(sql, val)
                    dcse.commit()
                for i in present:
                    sql = "UPDATE `{}` SET `{}`=2 WHERE roll=%s ".format(
                        tableName, col[tt[time]+1])
                    val = (i,)
                    dcse_cur.execute(sql, val)
                    dcse.commit()

                # rename time column name
                try:
                    newcolumn = time+'(pr)'
                    # print(newcolumn)
                    sql = 'ALTER TABLE `{}` CHANGE `{}` `{}` INT(11) NOT NULL DEFAULT "-1"'.format(
                        tableName, col[tt[time]], newcolumn)
                    dcse_cur.execute(sql)
                    dcse.commit()

                    # times = list(tt.keys())
                    # index = list(tt.values())
                    # p = tt[time]+1
                    # posi = index.index(p)
                    # print(times[posi])

                    # if col[tt[time]+1] == times[posi]:
                    #     sql = "ALTER TABLE `{}` DROP `{}`".format(tableName,col[tt[time]+1])
                    #     dcse_cur.execute(sql)
                    #     dcse.commit()

                except:
                    print('column name not exixt')

    dcse.close()


def addAttendance_theory(data, present, roll):
    at_btech = mysql.connector.connect(
        user='root', password='', host='localhost', database='theory_btech')
    at_ty = mysql.connector.connect(
        user='root', password='', host='localhost', database='theory_ty')
    at_sy = mysql.connector.connect(
        user='root', password='', host='localhost', database='theory_sy')

    btech = at_btech.cursor()
    ty = at_ty.cursor()
    sy = at_sy.cursor()

    # print(data,present)
    if data[0] == "BTECH":
        date = data[2].replace('-', '_')
        try:
            for i in roll:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(
                    data[3], date, i)
                btech.execute(sql)
                at_btech.commit()

            for i in present:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=1 WHERE roll={} ".format(
                    data[3], date, i)
                btech.execute(sql)
                at_btech.commit()

        except:
            print('already exist')

            sql = 'ALTER TABLE `{}` ADD {} int DEFAULT -1'.format(
                data[3], date)
            btech.execute(sql)
            at_btech.commit()

            for i in roll:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(
                    data[3], date, i)
                btech.execute(sql)
                at_btech.commit()

            for i in present:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=1 WHERE roll={} ".format(
                    data[3], date, i)
                btech.execute(sql)
                at_btech.commit()
        at_btech.close()

    elif data[0] == "TY":
        date = data[2].replace('-', '_')
        try:
            for i in roll:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(
                    data[3], date, i)
                ty.execute(sql)
                at_ty.commit()

            for i in present:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=1 WHERE roll={} ".format(
                    data[3], date, i)
                ty.execute(sql)
                at_ty.commit()

        except:
            print('already exist')

            sql = 'ALTER TABLE `{}` ADD {} int DEFAULT -1'.format(
                data[3], date)
            ty.execute(sql)
            at_ty.commit()

            for i in roll:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(
                    data[3], date, i)
                ty.execute(sql)
                at_ty.commit()

            for i in present:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=1 WHERE roll={} ".format(
                    data[3], date, i)
                ty.execute(sql)
                at_ty.commit()
        at_ty.close()

    elif data[0] == "SY":
        date = data[2].replace('-', '_')
        try:
            for i in roll:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(
                    data[3], date, i)
                sy.execute(sql)
                at_sy.commit()

            for i in present:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=1 WHERE roll={} ".format(
                    data[3], date, i)
                sy.execute(sql)
                at_sy.commit()

        except:
            print('already exist')

            sql = 'ALTER TABLE `{}` ADD {} int DEFAULT -1'.format(
                data[3], date)
            sy.execute(sql)
            at_sy.commit()

            for i in roll:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(
                    data[3], date, i)
                sy.execute(sql)
                at_sy.commit()

            for i in present:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=1 WHERE roll={} ".format(
                    data[3], date, i)
                sy.execute(sql)
                at_sy.commit()
        at_sy.close()


def addDoubleAttendance_theory(data, present, roll):
    at_btech = mysql.connector.connect(
        user='root', password='', host='localhost', database='theory_btech')
    at_ty = mysql.connector.connect(
        user='root', password='', host='localhost', database='theory_ty')
    at_sy = mysql.connector.connect(
        user='root', password='', host='localhost', database='theory_sy')

    btech = at_btech.cursor()
    ty = at_ty.cursor()
    sy = at_sy.cursor()
    print('data', data)
    if data[0] == "BTECH":
        date = data[2].replace('-', '_')
        for i in present:
            sql = "SELECT `{}` FROM `{}` WHERE roll = {}".format(
                date, data[3], i)
            btech.execute(sql)
            curattendance = btech.fetchone()[0]
            curattendance += 1
            sql = "UPDATE `{}` SET `{}`={} WHERE roll={} ".format(
                data[3], date, curattendance, i)
            btech.execute(sql)
            at_btech.commit()

    elif data[0] == "TY":
        date = data[2].replace('-', '_')
        for i in present:
            sql = "SELECT `{}` FROM `{}` WHERE roll = {}".format(
                date, data[3], i)
            ty.execute(sql)
            curattendance = ty.fetchone()[0]
            curattendance += 1
            sql = "UPDATE `{}` SET `{}`={} WHERE roll={} ".format(
                data[3], date, curattendance, i)
            ty.execute(sql)
            at_ty.commit()

    elif data[0] == "SY":
        date = data[2].replace('-', '_')
        for i in present:
            sql = "SELECT `{}` FROM `{}` WHERE roll = {}".format(
                date, data[3], i)
            sy.execute(sql)
            curattendance = sy.fetchone()[0]
            curattendance += 1
            sql = "UPDATE `{}` SET `{}`={} WHERE roll={} ".format(
                data[3], date, curattendance, i)
            sy.execute(sql)
            at_sy.commit()


def addAttendance_practical(data, present, roll):

    ap_btech = mysql.connector.connect(
        user='root', password='', host='localhost', database='practical_btech')
    ap_ty = mysql.connector.connect(
        user='root', password='', host='localhost', database='practical_ty')
    ap_sy = mysql.connector.connect(
        user='root', password='', host='localhost', database='practical_sy')

    btechP = ap_btech.cursor()
    tyP = ap_ty.cursor()
    syP = ap_sy.cursor()

    if data[0] == "BTECH":
        date = data[2].replace('-', '_')
        print(date)
        try:
            for i in roll:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(
                    data[3], date, i)
                btechP.execute(sql)
                ap_btech.commit()

            for i in present:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=2 WHERE roll={} ".format(
                    data[3], date, i)
                btechP.execute(sql)
                ap_btech.commit()

        except:
            print('already exist')

            sql = 'ALTER TABLE `{}` ADD {} int DEFAULT -1'.format(
                data[3], date)
            btechP.execute(sql)
            ap_btech.commit()

            for i in roll:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(
                    data[3], date, i)
                btechP.execute(sql)
                ap_btech.commit()

            for i in present:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=2 WHERE roll={} ".format(
                    data[3], date, i)
                btechP.execute(sql)
                ap_btech.commit()
        ap_btech.close()

    elif data[0] == "TY":
        date = data[2].replace('-', '_')
        print(date)
        try:
            for i in roll:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(
                    data[3], date, i)
                tyP.execute(sql)
                ap_ty.commit()

            for i in present:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=2 WHERE roll={} ".format(
                    data[3], date, i)
                tyP.execute(sql)
                ap_ty.commit()

        except:
            print('already exist')

            sql = 'ALTER TABLE `{}` ADD {} int DEFAULT -1'.format(
                data[3], date)
            tyP.execute(sql)
            ap_ty.commit()

            for i in roll:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(
                    data[3], date, i)
                tyP.execute(sql)
                ap_ty.commit()

            for i in present:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=2 WHERE roll={} ".format(
                    data[3], date, i)
                tyP.execute(sql)
                ap_ty.commit()
        ap_ty.close()

    elif data[0] == "SY":
        date = data[2].replace('-', '_')
        print(date)
        try:
            for i in roll:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(
                    data[3], date, i)
                syP.execute(sql)
                ap_sy.commit()

            for i in present:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=2 WHERE roll={} ".format(
                    data[3], date, i)
                syP.execute(sql)
                ap_sy.commit()

        except:
            print('already exist')

            sql = 'ALTER TABLE `{}` ADD {} int DEFAULT -1'.format(
                data[3], date)
            syP.execute(sql)
            ap_sy.commit()

            for i in roll:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=0 WHERE roll={} ".format(
                    data[3], date, i)
                syP.execute(sql)
                ap_sy.commit()

            for i in present:
                # print(i,date)
                # print(data[4])
                sql = "UPDATE `{}` SET {}=2 WHERE roll={} ".format(
                    data[3], date, i)
                syP.execute(sql)
                ap_sy.commit()
        ap_sy.close()
