import pandas as pd
from routes import mysql_stud
import mysql.connector
import pickle

fs = 'subinfo.pkl'


def addInSubject(roll, name, year, div):
    at_btech = mysql.connector.connect(
        user='root', password='', host='localhost', database='theory_btech')
    at_ty = mysql.connector.connect(
        user='root', password='', host='localhost', database='theory_ty')
    at_sy = mysql.connector.connect(
        user='root', password='', host='localhost', database='theory_sy')

    btech = at_btech.cursor()
    ty = at_ty.cursor()
    sy = at_sy.cursor()

    fsub = open(fs, 'rb')
    subs_btech = pickle.load(fsub)

    # print(year)
    if year == "BTECH":
        for i in subs_btech['Theory'][year]:
            sql = "INSERT INTO "+"`"+i+"`" + \
                " (roll,name,division) VALUES (%s,%s,%s)"
            values = (str(roll), name, div)
            btech.execute(sql, values)
            at_btech.commit()
        at_btech.close()

    elif year == 'TY':
        for i in subs_btech['Theory'][year]:
            sql = "INSERT INTO "+"`"+i+"`" + \
                " (roll,name,division) VALUES (%s,%s,%s)"
            values = (str(roll), name, div)
            ty.execute(sql, values)
            at_ty.commit()
        at_ty.close()

    elif year == 'SY':
        for i in subs_btech['Theory'][year]:
            sql = "INSERT INTO "+"`"+i+"`" + \
                " (roll,name,division) VALUES (%s,%s,%s)"
            values = (str(roll), name, div)
            sy.execute(sql, values)
            at_sy.commit()
        at_sy.close()


# ------------for practical -------------
def addInPractical(roll, name, year, div, batch):
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
    subs_btech = pickle.load(fsub)

    if year == "BTECH":
        for i in subs_btech['Practical'][year]:
            sql = "INSERT INTO "+"`"+i+"`" + \
                " (roll,name,division,batch) VALUES (%s,%s,%s,%s)"
            values = (str(roll), name, div, batch)
            btechP.execute(sql, values)
            ap_btech.commit()
        ap_btech.close()

    elif year == 'TY':
        for i in subs_btech['Practical'][year]:
            sql = "INSERT INTO "+"`"+i+"`" + \
                " (roll,name,division,batch) VALUES (%s,%s,%s,%s)"
            values = (str(roll), name, div, batch)
            tyP.execute(sql, values)
            ap_ty.commit()
        ap_ty.close()

    elif year == 'SY':
        for i in subs_btech['Practical'][year]:
            sql = "INSERT INTO "+"`"+i+"`" + \
                " (roll,name,division,batch) VALUES (%s,%s,%s,%s)"
            values = (str(roll), name, div, batch)
            syP.execute(sql, values)
            ap_sy.commit()
        ap_sy.close()


def addLoginInfo(roll, name, year):
    # print('in ad in login')
    logindbs = mysql.connector.connect(
        user='root', password='', host='localhost', database='login')
    lo_cur = logindbs.cursor()
    authoritiy = 'student'
    username = name.split()[0]
    password = str(roll)
    email = year+'@gmail.com'
    # print(type(authoritiy),type(username),type(password),type(email))
    lo_cur.execute('INSERT INTO account VALUES (%s, %s, %s, %s, %s)',
                   (roll, authoritiy, username, password, email,))
    logindbs.commit()


def parseCSV(filePath, year, div):
    cur = mysql_stud.connection.cursor()
    col_names = ['roll', 'name', 'batch', 'sphone', 'pphone']
    csvData = pd.read_csv(filePath, names=col_names, header=None)
    # print(csvData)
    for i, row in csvData.iterrows():
        # print(row)
        try:
            sql = "INSERT INTO " + year + \
                " (ROLL_NO, NAME, YEAR, DIVISION, BATCH, SPHONE, PPHONE) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            value = (row['roll'], row['name'], year, div,
                     row['batch'], row['sphone'], row['pphone'])
            # print(value)
            cur.execute(sql, value)
            mysql_stud.connection.commit()
            addInSubject(row['roll'], row['name'], year, div)
            addInPractical(row['roll'], row['name'], year, div, row['batch'])
            addLoginInfo(row['roll'], row['name'], year)
        except:
            print('PRN already exist')
