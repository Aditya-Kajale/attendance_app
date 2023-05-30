from flask import Flask, render_template, request, redirect, url_for, session
from addClass import *
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from flask_paranoid import Paranoid
import mysql.connector
import os
import re
import pickle
import json

f = 'fcinfo.pkl'
fs = 'subinfo.pkl'


class Faculty:
    # Constructor
    def __init__(self, id, name, subject, authority):
        self.id = id
        self.name = name
        self.subject = subject
        self.authority = authority

    # Function to create and append new student
    def accept(self, id, Name, Subject, authority):
        ob = Faculty(id, Name, Subject, authority)
        ls.append(ob)
        fwobj = open(f, 'wb')
        pickle.dump(ls, fwobj)

    # Function to display student details
    def display(self):
        frobj = open(f, 'rb')
        ff = pickle.load(frobj)
        print(ff)

    # Search Function
    def search(self, rn):
        for i in range(len(ls)):
            if (ls[i].name == rn):
                return i

    # Delete Function
    def delete(self, rn):
        i = obj.search(rn)
        print(i)
        del ls[i]
        fwobj = open(f, 'wb')
        pickle.dump(ls, fwobj)

    # Update Function
    def update(self, rn, No):
        i = obj.search(rn)
        roll = No
        ls[i].id = roll

    def getSubject(self, rn):
        i = obj.search(rn)
        return ls[i].subject

    def getName(self, rn):
        i = obj.search(rn)
        print(i)
        return ls[i].name


try:
    frobj = open(f, 'rb')
    ff = pickle.load(frobj)
    fsub = open(fs, 'rb')
    subs = pickle.load(fsub)
    ls = ff
except:
    ls = []
    subs = []

# print(1,ls[0].name)
obj = Faculty(0, '', {}, '')

app = Flask(__name__)
app.config.update(
    # SESSION_COOKIE_SECURE=True,
    DEBUG=True,
    REMEMBER_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_HTTPONLY=True
)
paranoid = Paranoid(app)
paranoid.redirect_view = '/'

app.secret_key = 'your secret key'
# for the student database
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root@123"
app.config["MYSQL_DB"] = "students"
mysql_stud = MySQL(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'adityakajale@dietms.org'
app.config['MAIL_PASSWORD'] = '9763836736'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# log in and logout ----------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        logindbs = mysql.connector.connect(
            user='root', password='root@123', host='localhost', database='login')
        lo_cur = logindbs.cursor()
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        username = username.split()[0]
        # print(type(username),type(password))
        sql = "SELECT * FROM account WHERE username = %s "
        val = (username,)
        lo_cur.execute(sql, val)
        print(lo_cur.statement)
        account = lo_cur.fetchall()
        print(account)
        if account:
            if password == account[0][3]:
                pass
            else:
                account = []
        logindbs.close()
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account[0][0]
            session['authority'] = account[0][1]
            session['username'] = account[0][2]
            if session['authority'] != 'student' and session['username'] != 'master':
                session['SUB'] = account[0][-1]
                session['SUB'] = json.loads(session['SUB'])
            # print(type(session['SUB']))

            # Redirect to home page
            if session['authority'] == 'admin' or session['authority'] == 'yearcoordinator':
                return redirect(url_for('adminHome'))
            elif session['authority'] == 'examcoordinator':
                return redirect(url_for('examhome'))
            elif session['authority'] == 'master':
                return redirect(url_for('masterHome'))
            elif session['authority'] == 'student':
                cur = mysql_stud.connection.cursor()
                year = account[0][4].split('@')[0]
                session['year'] = year
                sql = "SELECT `DIVISION` FROM `{}` WHERE `ROLL_NO`='{}'".format(
                    year, session['id'])
                cur.execute(sql)
                div = cur.fetchone()
                session['division'] = div[0]
                return redirect(url_for('studentHome'))
            else:
                return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)


@app.route('/forgetPass', methods=['POST', 'GET'])
def forgetPass():
    logindbs = mysql.connector.connect(
        user='root', password='root@123', host='localhost', database='login')
    lo_cur = logindbs.cursor()
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        sql = 'SELECT * FROM account WHERE username = %s'
        val = (username,)
        lo_cur.execute(sql, val)
        account = lo_cur.fetchall()
        if account:
            auth = account[0][1]
            if auth == 'student':
                msg = 'Students cant receive mails.'
                return render_template('forgetPass.html', msg=msg)
            print(account)
            message = Message('Attendance App', sender='adityakajale@dietms.org',
                              recipients=[account[0][4]])
            message.body = '''Your login credential are - \n\nID = {} \nUsername = {} \nPassword = {} \nemail = {} \n\nThank you.'''.format(
                account[0][0], account[0][2], account[0][3], account[0][4])
            mail.send(message)
            print(message)
            msg = 'Your credentials are sent to your email'
            render_template('forgetPass.html', msg=msg)
        else:
            msg = 'This username dosen`t exist'
            return render_template('forgetPass.html', msg=msg)

    logindbs.close()
    return render_template('forgetPass.html', msg=msg)


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     logindbs = mysql.connector.connect(
#         user='root', password='root@123', host='localhost', database='login')
#     lo_cur = logindbs.cursor()
#     # Output message if something goes wrong...
#     msg = ''
#     # Check if "username", "password" and "email" POST requests exist (user submitted form)
#     if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
#         # Create variables for easy access
#         id = request.form['id']
#         authoritiy = request.form['authoritiy']
#         username = request.form['username']
#         password = request.form['password']
#         email = request.form['email']
#         # print(username,password,email,authorities)

#         sql = 'SELECT * FROM account WHERE username = "{}"'.format(username)
#         lo_cur.execute(sql)
#         account = lo_cur.fetchall()

#         if account:
#             msg = 'Account already exists!'
#         elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
#             msg = 'Invalid email address!'
#         elif not re.match(r'[A-Za-z0-9]+', username):
#             msg = 'Username must contain only characters and numbers!'
#         elif not username or not password or not email:
#             msg = 'Please fill out the form!'
#         else:
#             # Account doesnt exists and the form data is valid, now insert new account into accounts table
#             sub = '{"BTECH":{"A":{"THEORY":{},"PRACTICAL":{}},"B":{"THEORY":{},"PRACTICAL":{}}},"TY":{"A":{"THEORY":{},"PRACTICAL":{}},"B":{"THEORY":{},"PRACTICAL":{}}},"SY":{"A":{"THEORY":{},"PRACTICAL":{}},"B":{"THEORY":{},"PRACTICAL":{}}}}'
#             obj.accept(id, username, {"Theory": [],
#                        "Practical": []}, authoritiy)
#             lo_cur.execute('INSERT INTO account VALUES (%s, %s, %s, %s, %s, %s)',
#                            (id, authoritiy, username, password, email, sub))
#             logindbs.commit()
#             msg = 'You have successfully registered!'

#     elif request.method == 'POST':
#         msg = 'Please fill out the form!'

#     logindbs.close()
#     return render_template('register.html', msg=msg)


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    if 'loggedin' in session:
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('usrename', None)
        session.pop('authority', None)
        session.clear()
        return redirect(url_for('login'))
    return redirect(url_for('login'))


@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session and session['authority'] == 'Faculty':
        # We need all the account info for the user so we can display it on the profile page
        logindbs = mysql.connector.connect(
            user='root', password='root@123', host='localhost', database='login')
        lo_cur = logindbs.cursor()
        lo_cur.execute('SELECT * FROM account WHERE username = %s',
                       (session['username'],))
        account = lo_cur.fetchone()
        # Show the profile page with account info
        logindbs.close()
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session and session['authority'] == 'Faculty':
        import homeinfo
        all = {}
        all['username'] = session['username']
        all['subs'] = session['SUB']
        count = homeinfo.getleccount(all['subs'])
        all['count'] = count
        return render_template('home.html', data=all)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# Master Pages ----------------------------------------------------------------
@app.route('/masterHome')
def masterHome():
    if 'loggedin' in session and session['authority'] == 'master':
        return render_template('masterhome.html', username=session['username'])
    return redirect(url_for('login'))


@app.route('/masterprofile')
def masterprofile():
    if 'loggedin' in session and session['authority'] == 'master':
        logindbs = mysql.connector.connect(
            user='root', password='root@123', host='localhost', database='login')
        lo_cur = logindbs.cursor()
        lo_cur.execute('SELECT * FROM account WHERE id = %s', (session['id'],))
        account = lo_cur.fetchone()
        logindbs.close()
        return render_template('masterprofile.html', account=account)
    return redirect(url_for('login'))


@app.route('/masterclean')
def masterclean():
    if 'loggedin' in session and session['authority'] == 'master':
        return render_template('masterclean.html')
    return redirect(url_for('login'))


@app.route('/cleandata', methods=['GET', 'POST'])
def cleandata():
    if 'loggedin' in session and session['authority'] == 'master':
        import cleandata
        year = request.form.get('year')
        cleandata.cleandata(year)
        return redirect(url_for('masterclean'))
    return redirect(url_for('login'))


# student Pages ------------------------------------------------------------
@app.route('/studenthome')
def studentHome():
    if 'loggedin' in session and session['authority'] == 'student':
        return render_template('studenthome.html', username=session['username'])
    return redirect(url_for('login'))


@app.route('/studentprofile')
def studentprofile():
    if 'loggedin' in session and session['authority'] == 'student':
        logindbs = mysql.connector.connect(
            user='root', password='root@123', host='localhost', database='login')
        lo_cur = logindbs.cursor()
        lo_cur.execute('SELECT * FROM account WHERE id = %s', (session['id'],))
        account = lo_cur.fetchone()
        logindbs.close()
        return render_template('studentprofile.html', account=account)
    return redirect(url_for('login'))


@app.route('/studenttheory')
def studenttheory():
    if 'loggedin' in session and session['authority'] == 'student':
        total = {}
        year = session['year']
        print(session['year'], subs)
        total['subs'] = subs['Theory'][year]
        return render_template('studenttheory.html', total=total)
    return redirect(url_for('login'))


@app.route('/studenttheoryshow', methods=['GET', 'POST'])
def studenttheoryshow():
    if 'loggedin' in session and session['authority'] == 'student':
        import studentattendance
        total = {}
        year = session['year']
        roll = session['id']
        total['name'] = session['username']
        subject = request.form.get('subject')
        total['subject'] = subject
        total['data'] = studentattendance.studenttAttendance_theory(
            roll, year, subject)
        return render_template('studenttheoryshow.html', total=total)
    return redirect(url_for('login'))


@app.route('/studentpractical')
def studentpractical():
    if 'loggedin' in session and session['authority'] == 'student':
        total = {}
        year = session['year']
        # print(session['year'],subs)
        total['subs'] = subs['Practical'][year]
        return render_template('studentpractical.html', total=total)
    return redirect(url_for('login'))


@app.route('/studentpracticalshow', methods=['GET', 'POST'])
def studentpracticalshow():
    if 'loggedin' in session and session['authority'] == 'student':
        import studentattendance
        total = {}
        year = session['year']
        roll = session['id']
        total['name'] = session['username']
        subject = request.form.get('subject')
        total['subject'] = subject
        total['data'] = studentattendance.studenttAttendance_practical(
            roll, year, subject)
        return render_template('studentpracticalshow.html', total=total)
    return redirect(url_for('login'))


@app.route('/studentdefaulter')
def studentdefaulter():
    if 'loggedin' in session and session['authority'] == 'student':
        import studentattendance
        total = {}
        year = session['year']
        roll = session['id']
        total['name'] = session['username']
        total['data'] = studentattendance.studenttAttendance_defaulter(
            roll, year)
        return render_template('studentdefaulter.html', total=total)
    return redirect(url_for('login'))


@app.route('/studentmarks')
def studentmarks():
    if 'loggedin' in session and session['authority'] == 'student':
        import studentmarks
        ca1 = studentmarks.getmarks(
            'CA1', session['year'], session['division'], session['id'])
        midsem = studentmarks.getmarks(
            'MIDSEM', session['year'], session['division'], session['id'])
        ca2 = studentmarks.getmarks(
            'CA2', session['year'], session['division'], session['id'])
        session['marks'] = {'CA1': ca1,
                            'MIDSEM': midsem, 'CA2': ca2}
        return render_template('studentmarks.html', data=session['marks'])
    return redirect(url_for('login'))


@app.route('/studentgrievances', methods=['GET', 'POST'])
def studentgrievances():
    if 'loggedin' in session and session['authority'] == 'student':
        if request.method == 'POST':
            marks = mysql.connector.connect(
                user='root', password='root@123', host='localhost', database='marks')
            markCur = marks.cursor()
            session['grievance'] = [request.form.get('examtype'), request.form.get(
                'subject'), request.form.get('grievancemarks')]
            sql = "INSERT INTO `grievance` (`Roll`, `Examtype`,`Year`,`Division`, `Subject`, `Marks`) VALUES ('{}','{}','{}','{}','{}','{}')".format(
                session['id'], session['grievance'][0], session['year'], session['division'], session['grievance'][1], session['grievance'][2])
            markCur.execute(sql)
            marks.commit()
            marks.close()
            return redirect(url_for('studentgrievances'))
        else:
            marks = mysql.connector.connect(
                user='root', password='root@123', host='localhost', database='marks')
            markCur = marks.cursor()
            total = {}
            total['subs'] = subs['Theory'][session['year']]
            sql = "SELECT * FROM `grievance` WHERE `Roll`='{}'".format(
                session['id'])
            markCur.execute(sql)
            total['data'] = markCur.fetchall()
            sql = "SHOW COLUMNS FROM `grievance`"
            markCur.execute(sql)
            cols = markCur.fetchall()
            column = []
            for i in cols:
                column.append(i[0])
            total['col'] = column
            marks.close()
            return render_template('studentgrievances.html', total=total)
    return redirect(url_for('login'))


# Admin Pages -----------------------------------------------------------------
@app.route('/adminHome')
def adminHome():
    if 'loggedin' in session and ((session['authority'] == 'yearcoordinator' or session['authority'] == 'admin')):
        name = []
        subs = []
        for i in ls:
            name.append(i.name)
            subs.append(i.subject)
            print(name, subs)
        all = [name, subs]
        return render_template('adminhome.html', ls=all)
    return redirect(url_for('login'))


@app.route('/manageFaculty')
def manageFaculty():
    if 'loggedin' in session and (session['authority'] == 'yearcoordinator' or session['authority'] == 'admin'):
        faculty = []
        logindbs = mysql.connector.connect(
            user='root', password='root@123', host='localhost', database='login')
        lo_cur = logindbs.cursor()
        # for i in ls:
        #     faculty.append(i.name)
        # print(session['SUB'])
        # new
        sql = "SELECT * FROM `account` WHERE `authorities` = 'yearcoordinator' OR `authorities` = 'Faculty'"
        lo_cur.execute(sql)
        dt = lo_cur.fetchall()
        # print(dt)
        for i in dt:
            faculty.append(i[2])
        session['managefc'] = dt
        print(dt)
        logindbs.close()
        return render_template('managefaculty.html', faculty=faculty)
    return redirect(url_for('login'))


@app.route('/selectSubject', methods=['GET', 'POST'])
def selectSubject():
    if 'loggedin' in session and (session['authority'] == 'yearcoordinator' or session['authority'] == 'admin'):
        fsub = open(fs, 'rb')
        subs = pickle.load(fsub)

        faculty = request.form.get('faculty')
        session['fc'] = faculty

        for i in session['managefc']:
            if i[2] == faculty:
                session['fcdetails'] = i
                auth = i[1]

        if auth == 'yearcoordinator':
            for i in ls:
                if i.name == faculty:
                    fsubs = i.subject

            all = {}
            all['rem_subs_th'] = []
            all['rem_subs_pr'] = []
            all['fc'] = faculty
            all['subs_have'] = fsubs

            all['len_sub_th'] = len(all['subs_have']['Theory'])
            all['len_sub_pr'] = len(all['subs_have']['Practical'])

            # print(all['subs_have']['Practical'])
            for i in subs['Theory']:
                for j in subs['Theory'][i]:
                    if j not in all['subs_have']['Theory']:
                        all['rem_subs_th'].append(j)

            for i in subs['Practical']:
                for j in subs['Practical'][i]:
                    if j not in all['subs_have']['Practical']:
                        all['rem_subs_pr'].append(j)
            return render_template('selectSubject.html', all=all)
        # new view for faculty subject selection
        elif auth == 'Faculty':
            all = {}
            all['fc'] = faculty
            all['subs'] = subs
            all['fcsub'] = session['fcdetails']
            all['fcsub'] = json.loads(all['fcsub'][-1])
            print(all['fcsub'])
            return render_template('selectSubjectFaculty.html', dict=all)

    return redirect(url_for('login'))


@app.route('/assignSubjectFaculty', methods=['GET', 'POST'])
def assignSubjectFaculty():
    if 'loggedin' in session and (session['authority'] == 'yearcoordinator' or session['authority'] == 'admin'):
        import managefaculty
        if request.method == 'POST':
            divs = request.form.getlist('division')
            br = request.form.getlist('branch')
            managefaculty.assignSubjectToFaculty(
                divs, br, session['fcdetails'])
        return redirect(url_for('manageFaculty'))
    return redirect(url_for('login'))


@app.route('/assignSubject', methods=['GET', 'POST'])
def assignSubject():
    if 'loggedin' in session and (session['authority'] == 'yearcoordinator' or session['authority'] == 'admin'):
        subs_th = request.form.getlist('subs_th')
        subs_pr = request.form.getlist('subs_pr')
        fc = session['fc']
        print(subs_th, subs_pr)

        for i in ls:
            if i.name == fc:
                i.subject['Theory'] = subs_th
                i.subject['Practical'] = subs_pr

        fwobj = open(f, 'wb')
        pickle.dump(ls, fwobj)
        return redirect(url_for('manageFaculty'))
    return redirect(url_for('login'))


@app.route('/registerFaculty', methods=['GET', 'POST'])
def registerFaculty():
    if 'loggedin' in session and (session['authority'] == 'yearcoordinator' or session['authority'] == 'admin'):
        # Output message if something goes wrong...
        msg = ''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
            logindbs = mysql.connector.connect(
                user='root', password='root@123', host='localhost', database='login')
            lo_cur = logindbs.cursor()
            # Create variables for easy access
            id = request.form['id']
            authoritiy = request.form['authoritiy']
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']

            sql = 'SELECT * FROM account WHERE username = "{}"'.format(
                username)
            lo_cur.execute(sql)
            account = lo_cur.fetchall()

            if account:
                msg = 'Account already exists!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            elif not username or not password or not email:
                msg = 'Please fill out the form!'
            else:
                # Account doesnt exists and the form data is valid, now insert new account into accounts table
                sub = '{"BTECH":{"A":{"THEORY":{},"PRACTICAL":{}},"B":{"THEORY":{},"PRACTICAL":{}}},"TY":{"A":{"THEORY":{},"PRACTICAL":{}},"B":{"THEORY":{},"PRACTICAL":{}}},"SY":{"A":{"THEORY":{},"PRACTICAL":{}},"B":{"THEORY":{},"PRACTICAL":{}}}}'
                obj.accept(id, username, {"Theory": [],
                                          "Practical": []}, authoritiy)
                lo_cur.execute('INSERT INTO account VALUES (%s, %s, %s, %s, %s, %s)',
                               (id, authoritiy, username, password, email, sub))
                logindbs.commit()
                msg = 'You have successfully registered!'
                logindbs.commit()

        elif request.method == 'POST':
            msg = 'Please fill out the form!'

        logindbs.close()
        return redirect(url_for('manageFaculty', msg=msg))
    return redirect(url_for('login'))


@app.route('/removeFaculty', methods=['GET', 'POST'])
def removeFaculty():
    if 'loggedin' in session and (session['authority'] == 'yearcoordinator' or session['authority'] == 'admin'):
        import removeFaculty
        faculty = request.form.get('faculty')
        id = None
        for i in ls:
            if i.name == faculty:
                id = i.id
        removeFaculty.removeFaculty(faculty, id)
        obj.delete(faculty)
        return redirect(url_for('manageFaculty'))
    return redirect(url_for('login'))


@app.route('/manageSubject', methods=['GET', 'POST'])
def manageSubject():
    if 'loggedin' in session and (session['authority'] == 'yearcoordinator' or session['authority'] == 'admin'):
        if request.method == 'POST':
            fsub = open(fs, 'rb')
            subs = pickle.load(fsub)
            all = {}
            year = request.form.get('year')
            subtype = request.form.get('subtype')
            all['year'] = year
            all['subs'] = subs[subtype][year]
            all['subtype'] = subtype
            session['year_for_subject'] = year
            session['subtype'] = subtype
            return render_template('manageSubject2.html', all=all)
        return render_template('manageSubject1.html')
    return redirect(url_for('login'))


@app.route('/addsubject', methods=['GET', 'POST'])
def addSubject():
    if 'loggedin' in session and (session['authority'] == 'yearcoordinator' or session['authority'] == 'admin'):
        import addSubject
        subject = request.form.get('subject')
        year = session['year_for_subject']
        subtype = session['subtype']
        addSubject.addsubject(subtype, year, subject)
        return redirect(url_for('manageSubject'))
    return redirect(url_for('login'))


@app.route('/renamesubject', methods=['GET', 'POST'])
def renamesubject():
    if 'loggedin' in session and (session['authority'] == 'yearcoordinator' or session['authority'] == 'admin'):
        if request.method == 'POST':
            fsub = open(fs, 'rb')
            subs = pickle.load(fsub)
            all = {}
            year = request.form.get('delyear')
            subtype = request.form.get('delsubtype')
            all['year'] = year
            all['subs'] = subs[subtype][year]
            all['subtype'] = subtype
            session['yeardelete'] = year
            session['subtypedelete'] = subtype
            return render_template('renamesubject.html', all=all)
        return render_template('manageSubject1.html')
    return redirect(url_for('login'))


@app.route('/renamesub', methods=['GET', 'POST'])
def renamesub():
    if 'loggedin' in session and (session['authority'] == 'yearcoordinator' or session['authority'] == 'admin'):
        import addSubject
        delsub = request.form.getlist('rename')
        year = session['yeardelete']
        subtype = session['subtypedelete']
        addSubject.renamesubject(subtype, year, delsub)
        return redirect(url_for('manageSubject'))
    return redirect(url_for('login'))


@app.route('/adminProfile')
def adminProfile():
    if 'loggedin' in session and (session['authority'] == 'yearcoordinator' or session['authority'] == 'admin'):
        logindbs = mysql.connector.connect(
            user='root', password='root@123', host='localhost', database='login')
        lo_cur = logindbs.cursor()
        lo_cur.execute('SELECT * FROM account WHERE id = %s', (session['id'],))
        account = lo_cur.fetchone()
        logindbs.close()
        return render_template('adminprofile.html', account=account)
    return redirect(url_for('login'))


@app.route('/deletetheory')
def deletetheory():
    if 'loggedin' in session and (session['authority'] == 'yearcoordinator' or session['authority'] == 'admin'):
        data = []
        for i in ls:
            if i.name == session['username']:
                data = i.subject
        return render_template('deletetheory.html', data=data)
    return redirect(url_for('login'))


@app.route('/deletetheoryAttendance', methods=['GET', 'POST'])
def deletetheoryAttendance():
    if 'loggedin' in session and (session['authority'] == 'yearcoordinator' or session['authority'] == 'admin'):
        import deleteattendance
        year = request.form.get('year')
        division = request.form.get('division')
        date = request.form.get('date')
        subject = request.form.get('subject')
        batch = request.form.getlist('batch')
        deleteattendance.deleteAttendanceTheory(
            year, division, date, subject, batch, "Theory")
        return redirect(url_for('deletetheory'))
    return redirect(url_for('login'))


@app.route('/deletepractical')
def deletepractical():
    if 'loggedin' in session and (session['authority'] == 'yearcoordinator' or session['authority'] == 'admin'):
        data = []
        for i in ls:
            if i.name == session['username']:
                data = i.subject
        return render_template('deletepractical.html', data=data)
    return redirect(url_for('login'))


@app.route('/deletepracticalAttendance', methods=['GET', 'POST'])
def deletepracticalAttendance():
    if 'loggedin' in session and (session['authority'] == 'yearcoordinator' or session['authority'] == 'admin'):
        import deleteattendance
        year = request.form.get('year')
        division = request.form.get('division')
        date = request.form.get('date')
        subject = request.form.get('subject')
        timeslot = request.form.get('timeslot')
        batch = request.form.getlist('batch')
        deleteattendance.deleteAttendancePractical(
            year, division, date, subject, timeslot, batch, "Practical")
        return redirect(url_for('deletepractical'))
    return redirect(url_for('login'))


# adding class to dataset -----------------------------------------------------------------------------
@app.route('/addclass')
def addClass():
    if 'loggedin' in session and (session['authority'] == 'yearcoordinator' or session['authority'] == 'admin'):
        return render_template('addClass.html')
    return redirect(url_for('login'))


@app.route('/addclass', methods=['GET', 'POST'])
def addDataset():
    if 'loggedin' in session and (session['authority'] == 'yearcoordinator' or session['authority'] == 'admin'):
        if request.method == 'POST':
            uploaded_file = request.files['file']
            year = request.form.get('year')
            div = request.form.get('division')
            if uploaded_file.filename != '':
                file_path = os.path.join(
                    app.config['UPLOAD_FOLDER'], uploaded_file.filename)
                uploaded_file.save(file_path)
                parseCSV(file_path, str(year), str(div))
        return redirect(url_for('addClass'))
    return redirect(url_for('login'))


# -----------------------------------------------------------------------------------------------------

# adding student to database --------------------------------------------------------------------------
@app.route('/addstudent')
def addStudent():
    if 'loggedin' in session and (session['authority'] == 'yearcoordinator' or session['authority'] == 'admin'):
        return render_template('addStudent.html')
    return redirect(url_for('login'))


@app.route('/addstudent', methods=['GET', 'POST'])
def addStud():
    if 'loggedin' in session and (session['authority'] == 'yearcoordinator' or session['authority'] == 'admin'):
        import addStudentDBS
        if request.method == 'POST':
            roll = request.form.get('roll')
            name = request.form.get('name')
            prn = request.form.get('prn')
            year = request.form.get('year')
            division = request.form.get('division')
            batch = request.form.get('batch')
            addStudentDBS.addstud(roll, name, prn, year, division)
        return redirect(url_for('addStudent'))
    return redirect(url_for('login'))


# -----------------------------------------------------------------------------------------------------

# other attendance ---------------------------------------------------------------------------
@app.route('/other')
def other():
    if 'loggedin' in session and session['authority'] == 'Faculty':
        logindbs = mysql.connector.connect(
            user='root', password='root@123', host='localhost', database='login')
        lo_cur = logindbs.cursor()
        sql = "SELECT * FROM `account` WHERE `authorities` = 'Faculty'"
        lo_cur.execute(sql)
        dt = lo_cur.fetchall()
        for i in dt:
            if i[2] == session['username']:
                subs = json.loads(i[-1])
        newdic = {}
        for i in subs:
            for j in subs[i]:
                if subs[i][j]['THEORY']:
                    if i not in newdic:
                        newdic[i] = {}
                        if j not in newdic[i]:
                            newdic[i][j] = {}
                    newdic[i][j] = subs[i][j]['THEORY']
        logindbs.close()
        return render_template('other.html', data=newdic)
    return redirect(url_for('login'))


@app.route('/searchstudentother', methods=['GET', 'POST'])
def searchStudentOther():
    if 'loggedin' in session and session['authority'] == 'Faculty':
        import classRecordDBS
        import attendanceDBS
        if request.method == 'POST':
            year = request.form.get('year')
            division = request.form.get('division')
            sdate = request.form.get('sdate')
            edate = request.form.get('edate')
            subject = request.form.get('subject')
            batch = request.form.getlist('batch')
            bt = ', '.join(batch)
            session['searchother'] = (year, division, sdate, subject, batch)
            data = classRecordDBS.getData_batchvise(year, division, batch)
            data.sort()
            # attendanceDBS.defaulterData(year,division)
            total_data = (session['searchother'], data, bt)
            roll = []
            for i in data:
                roll.append(i[0])
            session['othroll'] = roll
        return render_template('addAttendanceOther.html', data=total_data)
    return redirect(url_for('login'))


@app.route('/addOtherAttendance', methods=['GET', 'POST'])
def addOtherAttendance():
    if 'loggedin' in session and session['authority'] == 'Faculty':
        import addAttendance
        count = request.form.getlist('count')
        addAttendance.addOtherAttendance(
            session['searchother'], count, session['othroll'])
        return redirect(url_for('other'))
    return redirect(url_for('login'))


# Theory--------------------
@app.route('/subjectAttendance_theory')
def subjectAttendance_theory():
    if 'loggedin' in session and session['authority'] == 'Faculty':
        logindbs = mysql.connector.connect(
            user='root', password='root@123', host='localhost', database='login')
        lo_cur = logindbs.cursor()
        sql = "SELECT * FROM `account` WHERE `authorities` = 'Faculty'"
        lo_cur.execute(sql)
        dt = lo_cur.fetchall()
        for i in dt:
            if i[2] == session['username']:
                subs = json.loads(i[-1])
        newdic = {}
        for i in subs:
            for j in subs[i]:
                if subs[i][j]['THEORY']:
                    if i not in newdic:
                        newdic[i] = {}
                        if j not in newdic[i]:
                            newdic[i][j] = {}
                    newdic[i][j] = subs[i][j]['THEORY']
        logindbs.close()
        return render_template('subjectAttendance_theory.html', data=newdic)
    return redirect(url_for('login'))


@app.route('/subjectTable_theory', methods=['GET', 'POST'])
def subjectTable_theory():
    if 'loggedin' in session and session['authority'] == 'Faculty':
        import attendanceDBS
        if request.method == 'POST':
            year = request.form.get('year')
            division = request.form.get('division')
            subject = request.form.get('subject')
            sdate = request.form.get('sdate')
            edate = request.form.get('edate')
            data = attendanceDBS.subjectAttendance_theory(
                year, division, subject, sdate, edate)
        return render_template('subjectTable_theory.html', data=data)
    return redirect(url_for('login'))


# Practical---------------------------------------------------------------------------
@app.route('/subjectAttendance_practical')
def subjectAttendance_practical():
    if 'loggedin' in session and session['authority'] == 'Faculty':
        logindbs = mysql.connector.connect(
            user='root', password='root@123', host='localhost', database='login')
        lo_cur = logindbs.cursor()
        sql = "SELECT * FROM `account` WHERE `authorities` = 'Faculty'"
        lo_cur.execute(sql)
        dt = lo_cur.fetchall()
        for i in dt:
            if i[2] == session['username']:
                subs = json.loads(i[-1])
        newdic = {}
        for i in subs:
            print(subs[i])
            for j in subs[i]:
                if subs[i][j]['PRACTICAL']:
                    if i not in newdic:
                        newdic[i] = {}
                        if j not in newdic[i]:
                            newdic[i][j] = {}
                    newdic[i][j] = subs[i][j]['PRACTICAL']
        logindbs.close()
        return render_template('subjectAttendance_practical.html', data=newdic)
    return redirect(url_for('login'))


@app.route('/subjectTable_practical', methods=['GET', 'POST'])
def subjectTable_practical():
    if 'loggedin' in session and session['authority'] == 'Faculty':
        import attendanceDBS
        if request.method == 'POST':
            year = request.form.get('year')
            division = request.form.get('division')
            subject = request.form.get('subject')
            batch = request.form.get('batch')
            sdate = request.form.get('sdate')
            edate = request.form.get('edate')
            data = attendanceDBS.subjectAttendance_practical(
                year, division, subject, batch, sdate, edate)
        return render_template('subjectTable_practical.html', data=data)
    return redirect(url_for('login'))


# ---------------------------------------------------------------------------
@app.route('/classAttendance')
def classAttendance():
    if 'loggedin' in session and session['authority'] == 'Faculty':
        return render_template('classAttendance.html')
    return redirect(url_for('login'))


@app.route('/classTable', methods=['GET', 'POST'])
def classTable():
    if 'loggedin' in session and session['authority'] == 'Faculty':
        import attendanceDBS
        if request.method == 'POST':
            year = request.form.get('year')
            division = request.form.get('division')
            sdate = request.form.get('sdate')
            edate = request.form.get('edate')
            data = attendanceDBS.classAttendance(year, division, sdate, edate)
            # print(data)
        return render_template('classTable.html', data=data)
    return redirect(url_for('login'))


# ---------------------------------------------------------------------
@app.route('/defaulter')
def defaulter():
    if 'loggedin' in session and session['authority'] == 'Faculty':
        return render_template('defaulter.html')
    return redirect(url_for('login'))


@app.route('/defaultertable', methods=['GET', 'POST'])
def defaulterTable():
    if 'loggedin' in session and session['authority'] == 'Faculty':
        import attendanceDBS
        if request.method == 'POST':
            year = request.form.get('year')
            division = request.form.get('division')
            sdate = request.form.get('sdate')
            edate = request.form.get('edate')
            defaulter = request.form.get('defaulter')
            # print(defaulter)
            data = attendanceDBS.defaulterData(
                year, division, sdate, edate, defaulter)
            # print(data)
        return render_template('defaulterTable.html', data=data)
    return redirect(url_for('login'))


# -----------------------------------------------------------------------------------------------------


# Display class record ------------------------------------------------------------------------------

@app.route('/classrecord')
def classRecord():
    if 'loggedin' in session and (session['authority'] == 'yearcoordinator' or session['authority'] == 'admin'):
        return render_template('classRecord.html')
    return redirect(url_for('login'))


@app.route('/showrecord', methods=['GET', 'POST'])
def showRecord():
    if 'loggedin' in session and (session['authority'] == 'yearcoordinator' or session['authority'] == 'admin'):
        import classRecordDBS
        if request.method == 'POST':
            year = request.form.get('year')
            division = request.form.get('division')
            # print(year,division)
            data = classRecordDBS.getData(year, division)
            return render_template('classRecord.html', data=data)
    return redirect(url_for('login'))


# -----------------------------------------------------------------------------------------------------

# Take attendance theory -------------------------------------------------------------------------------------
@app.route('/theoryAttendance')
def theoryAttendance():
    if 'loggedin' in session and session['authority'] == 'Faculty':
        # new
        logindbs = mysql.connector.connect(
            user='root', password='root@123', host='localhost', database='login')
        lo_cur = logindbs.cursor()
        sql = "SELECT * FROM `account` WHERE `authorities` = 'Faculty'"
        lo_cur.execute(sql)
        dt = lo_cur.fetchall()
        for i in dt:
            if i[2] == session['username']:
                subs = json.loads(i[-1])
        newdic = {}
        for i in subs:
            for j in subs[i]:
                if subs[i][j]['THEORY']:
                    if i not in newdic:
                        newdic[i] = {}
                        if j not in newdic[i]:
                            newdic[i][j] = {}
                    newdic[i][j] = subs[i][j]['THEORY']
        logindbs.close()
        return render_template('theoryAttendance.html', data=newdic)
    return redirect(url_for('login'))


@app.route('/searchstudents_theory', methods=['GET', 'POST'])
def searchStud_theory():
    if 'loggedin' in session and session['authority'] == 'Faculty':
        import classRecordDBS
        import dailyreport
        if request.method == 'POST':
            year = request.form.get('year')
            division = request.form.get('division')
            date = request.form.get('date')
            subject = request.form.get('subject')
            timeslot = request.form.get('timeslot')
            batch = request.form.getlist('batch')
            attype = request.form.get('attype')
            session['attype'] = attype
            bt = ', '.join(batch)
            session['searchtheory'] = (
                year, division, date, subject, timeslot, batch, attype)
            data = classRecordDBS.getData_batchvise(year, division, batch)
            msg = dailyreport.check_session(year, division, date, timeslot)
            data.sort()
            # print(data)
            total_data = (session['searchtheory'], data, bt, msg)
            roll = []
            for i in data:
                roll.append(i[0])
            session['throll'] = roll
        return render_template('addAttendance.html', data=total_data)
    return redirect(url_for('login'))


@app.route('/addattendance', methods=['GET', 'POST'])
def addAttendance():
    if 'loggedin' in session and session['authority'] == 'Faculty':
        import addAttendance
        if request.method == 'POST':
            present = request.form.getlist('present')
            # print(session['searchtheory'])
            if session['attype'] == 'Regular':
                addAttendance.addAttendance_theory(
                    session['searchtheory'], present, session['throll'])
            elif session['attype'] == 'Addition':
                addAttendance.addDoubleAttendance_theory(
                    session['searchtheory'], present, session['throll'])
            addAttendance.addattendance_daily(
                session['searchtheory'], present, session['throll'], "Theory")
        return redirect(url_for('theoryAttendance'))
    return redirect(url_for('login'))


@app.route('/editTheoryAttendance')
def editTheoryAttendance():
    if 'loggedin' in session and session['authority'] == 'Faculty':
        logindbs = mysql.connector.connect(
            user='root', password='root@123', host='localhost', database='login')
        lo_cur = logindbs.cursor()
        sql = "SELECT * FROM `account` WHERE `authorities` = 'Faculty'"
        lo_cur.execute(sql)
        dt = lo_cur.fetchall()
        for i in dt:
            if i[2] == session['username']:
                subs = json.loads(i[-1])
        newdic = {}
        for i in subs:
            for j in subs[i]:
                if subs[i][j]['THEORY']:
                    if i not in newdic:
                        newdic[i] = {}
                        if j not in newdic[i]:
                            newdic[i][j] = {}
                    newdic[i][j] = subs[i][j]['THEORY']
        logindbs.close()
        return render_template('editTheoryAttendance.html', data=newdic)
    return redirect(url_for('login'))


@app.route('/edit_searchstudents_theory', methods=['GET', 'POST'])
def edit_searchstudents_theory():
    if 'loggedin' in session and session['authority'] == 'Faculty':
        import editAttendance
        import classRecordDBS
        if request.method == 'POST':
            year = request.form.get('year')
            division = request.form.get('division')
            date = request.form.get('date')
            subject = request.form.get('subject')
            batch = request.form.getlist('batch')
            bt = ', '.join(batch)
            data = classRecordDBS.getData_batchvise(year, division, batch)
            data.sort()
            roll = []
            for i in data:
                roll.append(i[0])
            session['edit_searchtheory'] = (
                year, division, date, subject, batch, roll)
            attendance = editAttendance.get_attendance(
                year, data, subject, date)
            total_data = (session['edit_searchtheory'], data, attendance, bt)
        return render_template('editattendance.html', data=total_data)
    return redirect(url_for('login'))


@app.route('/edit_addattendance', methods=['GET', 'POST'])
def edit_addattendance():
    if 'loggedin' in session and session['authority'] == 'Faculty':
        import editAttendance
        if request.method == 'POST':
            present = request.form.getlist('present')
            editAttendance.editattendance(
                present, session['edit_searchtheory'])
        return redirect(url_for('editTheoryAttendance'))
    return redirect(url_for('login'))


# Take attendance practical -------------------------------------------------------------------------------------
@app.route('/practicalAttendance')
def practicalAttendance():
    if 'loggedin' in session and session['authority'] == 'Faculty':
        logindbs = mysql.connector.connect(
            user='root', password='root@123', host='localhost', database='login')
        lo_cur = logindbs.cursor()
        sql = "SELECT * FROM `account` WHERE `authorities` = 'Faculty'"
        lo_cur.execute(sql)
        dt = lo_cur.fetchall()
        for i in dt:
            if i[2] == session['username']:
                subs = json.loads(i[-1])
        newdic = {}
        for i in subs:
            print(subs[i])
            for j in subs[i]:
                if subs[i][j]['PRACTICAL']:
                    if i not in newdic:
                        newdic[i] = {}
                        if j not in newdic[i]:
                            newdic[i][j] = {}
                    newdic[i][j] = subs[i][j]['PRACTICAL']
        logindbs.close()
        return render_template('practicalAttendance.html', data=newdic)
    return redirect(url_for('login'))


@app.route('/searchstudents_practical', methods=['GET', 'POST'])
def searchstudents_practical():
    if 'loggedin' in session and session['authority'] == 'Faculty':
        import classRecordDBS
        import dailyreport
        if request.method == 'POST':
            year = request.form.get('year')
            division = request.form.get('division')
            date = request.form.get('date')
            subject = request.form.get('subject')
            timeslot = request.form.get('timeslot')
            batch = request.form.getlist('batch')
            attype = request.form.get('attype')
            session['prattype'] = attype
            msg = dailyreport.check_session_practical(
                year, division, date, batch, timeslot)
            print(msg)
            # print(batch)
            session['searchpractical'] = (
                year, division, date, subject, timeslot, batch, attype)
            data = classRecordDBS.getData_batchvise(year, division, batch)
            data.sort()
            total_data = (session['searchpractical'], data, msg)
            roll = []
            for i in data:
                roll.append(i[0])
            session['prroll'] = roll
        return render_template('addAttendancePractical.html', data=total_data)
    return redirect(url_for('login'))


@app.route('/addAttendance__practical', methods=['GET', 'POST'])
def addAttendance__practical():
    if 'loggedin' in session and session['authority'] == 'Faculty':
        import addAttendance
        if request.method == 'POST':
            present = request.form.getlist('present')
            # print(session['searchpractical'])
            if session['prattype'] == 'Regular':
                addAttendance.addAttendance_practical(
                    session['searchpractical'], present, session['prroll'])
            elif session['prattype'] == 'Addition':
                addAttendance.addDoubleAttendance_practical(
                    session['searchpractical'], present, session['prroll'])
            addAttendance.addattendance_daily(
                session['searchpractical'], present, session['prroll'], "Practical")

        return redirect(url_for('practicalAttendance'))
    return redirect(url_for('login'))


@app.route('/editPracticalAttendance')
def editPracticalAttendance():
    if 'loggedin' in session and session['authority'] == 'Faculty':
        logindbs = mysql.connector.connect(
            user='root', password='root@123', host='localhost', database='login')
        lo_cur = logindbs.cursor()
        sql = "SELECT * FROM `account` WHERE `authorities` = 'Faculty'"
        lo_cur.execute(sql)
        dt = lo_cur.fetchall()
        for i in dt:
            if i[2] == session['username']:
                subs = json.loads(i[-1])
        newdic = {}
        for i in subs:
            for j in subs[i]:
                if subs[i][j]['PRACTICAL']:
                    if i not in newdic:
                        newdic[i] = {}
                        if j not in newdic[i]:
                            newdic[i][j] = {}
                    newdic[i][j] = subs[i][j]['PRACTICAL']
        logindbs.close()
        return render_template('editPracticalAttendance.html', data=newdic)
    return redirect(url_for('login'))


@app.route('/edit_searchstudents_practical', methods=['GET', 'POST'])
def edit_searchstudents_practical():
    if 'loggedin' in session and session['authority'] == 'Faculty':
        import classRecordDBS
        import editAttendance
        if request.method == 'POST':
            year = request.form.get('year')
            division = request.form.get('division')
            date = request.form.get('date')
            subject = request.form.get('subject')
            batch = request.form.getlist('batch')
            data = classRecordDBS.getData_batchvise(year, division, batch)
            data.sort()
            attendance = editAttendance.get_practicalAttendance(
                year, data, subject, date)
            roll = []
            for i in data:
                roll.append(i[0])
            session['edit_searchpractical'] = (
                year, division, date, subject, batch, roll)
            total_data = (session['edit_searchpractical'], data, attendance)
        return render_template('editaddAttendancePractical.html', data=total_data)
    return redirect(url_for('login'))


@app.route('/edit_addAttendance__practical', methods=['GET', 'POST'])
def edit_addAttendance__practical():
    if 'loggedin' in session and session['authority'] == 'Faculty':
        import editAttendance
        if request.method == 'POST':
            present = request.form.getlist('present')
            editAttendance.editattendancePractical(
                present, session['edit_searchpractical'])
        return redirect(url_for('editPracticalAttendance'))
    return redirect(url_for('login'))


# daily report
@app.route('/dailyreport')
def dailyreport():
    if 'loggedin' in session and session['authority'] == 'Faculty':
        return render_template('dailyreport.html')
    return redirect(url_for('login'))


@app.route('/dailyreporttable', methods=['GET', 'POST'])
def dailyreporttable():
    if 'loggedin' in session and session['authority'] == 'Faculty':
        import dailyreport
        year = request.form.get('year')
        div = request.form.get('division')
        date = request.form.get('date')
        data = dailyreport.dailyreport(year, div, date)
        session['dailyreport'] = (year, div, date)
        return render_template('dailyreporttable.html', data=data)
    return redirect(url_for('login'))


@app.route('/updatedailyreport', methods=['GET', 'POST'])
def updatedailyreport():
    if 'loggedin' in session and session['authority'] == 'Faculty':
        import dailyreport
        session['reamrks'] = request.form.getlist('remark')
        session['sphone'] = request.form.getlist('sphone')
        session['pphone'] = request.form.getlist('pphone')
        dailyreport.updatedailyreport(
            session['dailyreport'], session['reamrks'], session['sphone'], session['pphone'])
        return redirect(url_for('dailyreport'))
    return redirect(url_for('login'))


@app.route('/facultygrievance')
def facultygrievance():
    if 'loggedin' in session and session['authority'] == 'Faculty':
        logindbs = mysql.connector.connect(
            user='root', password='root@123', host='localhost', database='login')
        lo_cur = logindbs.cursor()
        marks = mysql.connector.connect(
            user='root', password='root@123', host='localhost', database='marks')
        markCur = marks.cursor()
        sql = "SELECT * FROM `account` WHERE `authorities` = 'Faculty'"
        lo_cur.execute(sql)
        dt = lo_cur.fetchall()
        for i in dt:
            if i[2] == session['username']:
                subs = json.loads(i[-1])
        newsub = []
        newsubwithdiv = {}
        for i in subs:
            for j in subs[i]:
                for k in subs[i][j]['THEORY']:
                    if k not in newsub:
                        newsub.append(k)
                    if k not in newsubwithdiv:
                        newsubwithdiv[k] = []
                        newsubwithdiv[k].append(j)
                    else:
                        newsubwithdiv[k].append(j)
        griapplications = []
        for i in newsub:
            for k in newsubwithdiv[i]:
                sql = "SELECT * FROM `grievance` WHERE `Subject`='{}' AND `Division`='{}'".format(
                    i, k)
                markCur.execute(sql)
                data = markCur.fetchall()
                for k in data:
                    griapplications.append(k)

        sql = "SHOW COLUMNS FROM `grievance`"
        markCur.execute(sql)
        cols = markCur.fetchall()
        column = []
        for i in cols:
            column.append(i[0])

        applications = {'applications': griapplications, 'col': column}
        logindbs.close()
        marks.close()
        return render_template('facultygrievance.html', data=applications)
    return redirect(url_for('login'))


@app.route('/facultygriavancestatus', methods=['GET', 'POST'])
def facultygriavancestatus():
    if 'loggedin' in session and session['authority'] == 'Faculty':
        import studentmarks
        if request.form['action'] == 'ACCEPT':
            status = request.form.getlist('status')
            for m in status:
                k = m.split('/')
                print(k)
                studentmarks.allowgrievances(
                    k[0], k[1], k[2], k[3], k[4], k[5])

        if request.form['action'] == 'REJECT':
            status = request.form.getlist('status')
            for m in status:
                k = m.split('/')
                print(k)
                studentmarks.rejectgrievances(
                    k[0], k[1], k[2], k[3], k[4], k[5])

        return redirect(url_for('facultygrievance'))
    return redirect(url_for('login'))


# for marks coordinator login
@app.route('/examhome')
def examhome():
    if 'loggedin' in session and session['authority'] == 'examcoordinator':
        return render_template('examhome.html', username=session['username'])
    return redirect(url_for('login'))


@app.route('/exammarks')
def exammarks():
    if 'loggedin' in session and session['authority'] == 'examcoordinator':
        return render_template('exammarks.html', subs=subs)
    return redirect(url_for('login'))


@app.route('/addmarks', methods=['GET', 'POST'])
def addmarks():
    if 'loggedin' in session and session['authority'] == 'examcoordinator':
        import addmarks
        if request.method == 'POST':
            uploaded_file = request.files['file']
            exam = request.form.get('exam')
            year = request.form.get('year')
            div = request.form.get('division')
            if uploaded_file.filename != '':
                file_path = os.path.join(
                    app.config['UPLOAD_FOLDER'], uploaded_file.filename)
                uploaded_file.save(file_path)
            addmarks.addmarks(file_path, exam, year, div)
        return redirect(url_for('exammarks'))
    return redirect(url_for('login'))


@app.route('/examdisplay', methods=['GET', 'POST'])
def examdisplay():
    if 'loggedin' in session and session['authority'] == 'examcoordinator':
        if request.method == 'POST':
            marks = mysql.connector.connect(
                user='root', password='root@123', host='localhost', database='marks')
            markCur = marks.cursor()

            all = {}
            all['msg'] = ''
            exam = request.form.get('exam')
            year = request.form.get('year')
            div = request.form.get('division')
            all['pre'] = [exam, year, div]
            tablename = exam+'-'+year+'-'+div
            all['tname'] = tablename
            try:
                sql = "SHOW COLUMNS FROM `{}`".format(tablename)
                markCur.execute(sql)
                cols = markCur.fetchall()
                column = []
                for i in cols:
                    column.append(i[0])
                all['cols'] = column
                sql = 'SELECT * FROM `{}`'.format(tablename)
                markCur.execute(sql)
                data = markCur.fetchall()
                all['data'] = data
                roll = []
                for k in data:
                    roll.append(k[0])
                all['roll'] = roll
                session['examupdate'] = all
            except Exception as e:
                all['msg'] = "Data not found"
                print(e)
            marks.close()
            return render_template('examdisplayTable.html', data=all)
        return render_template('examdisplay.html')
    return redirect(url_for('login'))


@app.route('/updateexam', methods=['GET', 'POST'])
def updateexam():
    if 'loggedin' in session and session['authority'] == 'examcoordinator':
        import addmarks
        cols = session['examupdate']['cols'][3:]
        newmarks = {}
        for i in cols:
            temp = request.form.getlist(i)
            newmarks[i] = temp

        tablename = session['examupdate']['tname']
        roll = session['examupdate']['roll']
        addmarks.update_mark(tablename, newmarks, roll)
        return redirect(url_for('examdisplay'))
    return redirect(url_for('login'))


@app.route('/examdelete', methods=['GET', 'POST'])
def examdelete():
    if 'loggedin' in session and session['authority'] == 'examcoordinator':
        if request.method == 'POST':
            marks = mysql.connector.connect(
                user='root', password='root@123', host='localhost', database='marks')
            markCur = marks.cursor()
            all = {}
            year = request.form.get('year')
            div = request.form.get('division')
            all['pre'] = [year, div]
            sql = 'SHOW TABLES'
            markCur.execute(sql)
            tbs = markCur.fetchall()
            table = []
            for i in range(len(tbs)):
                temp = tbs[i][0].split('-')
                if temp[1] == year.lower() and temp[2] == div.lower():
                    table.append(tbs[i][0])
            all['tables'] = table
            marks.close()
            return render_template('examdelete1.html', data=all)
        return render_template('examdelete.html')
    return redirect(url_for('login'))


@app.route('/examdelete1', methods=['GET', 'POST'])
def examdelete1():
    if 'loggedin' in session and session['authority'] == 'examcoordinator':
        marks = mysql.connector.connect(
            user='root', password='root@123', host='localhost', database='marks')
        markCur = marks.cursor()
        delist = request.form.getlist('delete')
        for i in delist:
            sql = 'DROP TABLE `{}`'.format(i)
            markCur.execute(sql)
            marks.commit()
        marks.close()
        return redirect(url_for('examdelete'))
    return redirect(url_for('login'))


@app.route('/examprofile')
def examprofile():
    if 'loggedin' in session and session['authority'] == 'examcoordinator':
        logindbs = mysql.connector.connect(
            user='root', password='root@123', host='localhost', database='login')
        lo_cur = logindbs.cursor()
        lo_cur.execute('SELECT * FROM account WHERE username = %s',
                       (session['username'],))
        account = lo_cur.fetchone()
        logindbs.close()
        return render_template('examprofile.html', account=account)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, port=4000)
