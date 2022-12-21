from flask import Flask, render_template, request,redirect, url_for, session
from addClass import *
from flask_mysqldb import MySQL
from wtforms import SelectField
import mysql.connector
import os
import re
import pickle
f = 'fcinfo.pkl'
fs = 'subinfo.pkl'

class Faculty:
  # Constructor
    def __init__(self, id, name, subject):
        self.id = id
        self.name = name
        self.subject  = subject
 
    # Function to create and append new student
    def accept(self, id, Name, Subject):
        ob = Faculty(id, Name, Subject)
        ls.append(ob)
        fwobj = open(f,'wb')
        pickle.dump(ls,fwobj)
 
    # Function to display student details
    def display(self, ob):
        frobj = open(f,'rb')
        ff = pickle.load(frobj)
        print(ff)

    # Search Function
    def search(self, rn):
        for i in range(len(ls)):
            if(ls[i].id == rn):
                return i
 
    # Delete Function
    def delete(self, rn):
        i = obj.search(rn)
        print(i)
        del ls[i]
        fwobj = open(f,'wb')
        pickle.dump(ls,fwobj)

    # Update Function
    def update(self, rn, No):
        i = obj.search(rn)
        roll = No
        ls[i].id = roll

    def getSubject(self,rn):
        i = obj.search(rn)
        return ls[i].subject

    def getName(self,rn):
        i = obj.search(rn)
        print(i)
        return ls[i].name
try : 
   frobj = open(f,'rb')
   ff = pickle.load(frobj)
   fsub = open(fs,'rb')
   subs = pickle.load(fsub)
   ls = ff
except:
   ls = []
   subs = []

obj = Faculty(0,'', [])



logindbs = mysql.connector.connect(user='root', password='', host='localhost', database='login')
lo_cur = logindbs.cursor()

app = Flask(__name__)
app.secret_key = 'your secret key'


# for the student database
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "students"
mysql_stud = MySQL(app)


UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

# log in and logout ----------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # print(type(username),type(password))
        sql = 'SELECT * FROM account WHERE username = "{}" and password= "{}"'.format(username,password)
        lo_cur.execute(sql)
        account = lo_cur.fetchall()
        print(account)
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True 
            session['id'] = account[0][0]
            session['username'] = account[0][1]
            # Redirect to home page    
            if session['username'] == 'admin':
               return redirect(url_for('adminHome'))
            else:
               return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template('login.html', msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        id = request.form['id']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        print(username,password,email)

        sql = 'SELECT * FROM account WHERE username = "{}"'.format(username)
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
            obj.accept(id,username,[])
            lo_cur.execute('INSERT INTO account VALUES (%s, %s, %s, %s)', (id,username, password, email,))
            logindbs.commit()
            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)

    return render_template('register.html', msg=msg)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session :
        # We need all the account info for the user so we can display it on the profile page
        lo_cur.execute('SELECT * FROM account WHERE id = %s', (session['id'],))
        account = lo_cur.fetchone()
        print(account)
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/home')
def home():
   # Check if user is loggedin
   if 'loggedin' in session and session['username'] != 'admin':
      # User is loggedin show them the home page
      return render_template('home.html', username=session['username'])
   # User is not loggedin redirect to login page
   return redirect(url_for('login'))


# Admin Pages -----------------------------------------------------------------
@app.route('/adminHome')
def adminHome():
   if 'loggedin' in session and session['username'] == 'admin':
      name = []
      subs = []
      for i in ls:
         name.append(i.name)
         subs.append(i.subject)
      # print(faculty.obj.getName(1))
      all = [name,subs]
      return render_template('adminhome.html',ls = all)
   return redirect(url_for('login'))

# ----------------------------------------------------------------------------------
@app.route('/manageFaculty')
def manageFaculty():
   if 'loggedin' in session and session['username'] == 'admin':
      faculty = []
      for i in ls:
         faculty.append(i.name) 
      return render_template('managefaculty.html',faculty = faculty)
   return redirect(url_for('login'))

@app.route('/selectSubject',methods = ['GET', 'POST'])
def selectSubject():
   if 'loggedin' in session and session['username'] == 'admin':
      all = {}
      all['rem_subs'] = []
      faculty = request.form.get('faculty')
      session ['fc'] = faculty
      fsubs = []
      for i in ls:
         if i.name == faculty:
            fsubs = i.subject
      all['fc'] = faculty
      all['subs_have'] = fsubs
      all['len_sub'] = len(all['subs_have'])
      for i in subs:
         if i not in all['subs_have']:
            all['rem_subs'].append(i)
      return render_template('selectSubject.html',all = all)
   return redirect(url_for('login'))

@app.route('/assignSubject',methods = ['GET', 'POST'])
def assignSubject():
   all_subs = request.form.getlist('subs')
   fc = session['fc']
   for i in ls:
      if i.name == fc:
         i.subject = all_subs
   
   fwobj = open(f,'wb')
   pickle.dump(ls,fwobj)
   return redirect(url_for('manageFaculty'))

# --------------------------------------------------------------------------------
@app.route('/manageSubject')
def manageSubject():
   if 'loggedin' in session and session['username'] == 'admin':
      all = {}
      all['subs'] = subs
      return render_template('manageSubject.html',all =all)
   return redirect(url_for('login'))

@app.route('/addsubject',methods = ['GET', 'POST'])
def addSubject():
   if 'loggedin' in session and session['username'] == 'admin':
      subject = request.form.get('subject')
      subs.append(subject)
      subw = open(fs,'wb')
      pickle.dump(subs,subw)
      return redirect(url_for('manageSubject'))
   return redirect(url_for('login'))
   
# ------------------------------------------------------------------------------
@app.route('/adminProfile')
def adminProfile():
   if 'loggedin' in session and session['username'] == 'admin':
      lo_cur.execute('SELECT * FROM account WHERE id = %s', (session['id'],))
      account = lo_cur.fetchone()
      return render_template('adminprofile.html',account=account)
   return redirect(url_for('login'))



# adding class to dataset -----------------------------------------------------------------------------
@app.route('/addclass')
def addClass():
   if 'loggedin' in session and session['username'] != 'admin':
      return render_template('addClass.html')
   return redirect(url_for('login'))

@app.route('/addclass', methods = ['GET', 'POST'])
def addDataset():
   if 'loggedin' in session and session['username'] != 'admin':
      if request.method == 'POST':
         uploaded_file = request.files['file']
         year = request.form.get('year')
         div = request.form.get('division')
         batchlength = request.form.get('batchlength')
         if uploaded_file.filename != '':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            # set the file path
            uploaded_file.save(file_path)
            # print(file_path)
            # print(year,div)
            parseCSV(file_path,str(year),str(div),batchlength)

      return redirect(url_for('addClass'))

   return redirect(url_for('login'))


# -----------------------------------------------------------------------------------------------------

# adding student to database --------------------------------------------------------------------------
@app.route('/addstudent')
def addStudent():
   if 'loggedin' in session and session['username'] != 'admin':
      return render_template('addStudent.html')
   return redirect(url_for('login'))


@app.route('/addstudent', methods = ['GET', 'POST'])
def addStud():
   if 'loggedin' in session and session['username'] != 'admin':
      import addStudentDBS
      if request.method == 'POST':
         roll = request.form.get('roll')
         name = request.form.get('name')
         prn = request.form.get('prn')
         year = request.form.get('year')
         division = request.form.get('division')
         addStudentDBS.addstud(roll,name,prn,year,division)
      return redirect(url_for('addStudent'))

   return redirect(url_for('login'))


# -----------------------------------------------------------------------------------------------------

# Display Attendacne record ---------------------------------------------------------------------------
@app.route('/subjectRecord')
def subjectAttendance():
   if 'loggedin' in session and session['username'] != 'admin': 
      return render_template('subjectAttendance.html')
   return redirect(url_for('login'))


@app.route('/subjectTable', methods = ['GET', 'POST'])
def subjectTable():
   if 'loggedin' in session and session['username'] != 'admin': 
      import attendanceDBS
      if request.method == 'POST':
         year = request.form.get('year')
         division = request.form.get('division')
         subject = request.form.get('subject')
         sdate = request.form.get('sdate')
         edate = request.form.get('edate')
         data = attendanceDBS.subjectAttendance(year,division,subject,sdate,edate)
      return render_template('subjectTable.html',data=data)
   return redirect(url_for('login'))


@app.route('/classAttendance')
def classAttendance():
   if 'loggedin' in session and session['username'] != 'admin': 
      return render_template('classAttendance.html')
   return redirect(url_for('login'))


@app.route('/classTable', methods = ['GET', 'POST'])
def classTable():
   if 'loggedin' in session and session['username'] != 'admin': 
      import attendanceDBS
      if request.method == 'POST':
         year = request.form.get('year')
         division = request.form.get('division')
         sdate = request.form.get('sdate')
         edate = request.form.get('edate')
         data = attendanceDBS.classAttendance(year,division,sdate,edate)
         # print(data)
      return render_template('classTable.html',data=data)
   return redirect(url_for('login'))


@app.route('/defaulter')
def defaulter():
   if 'loggedin' in session and session['username'] != 'admin': 
      return render_template('defaulter.html')
   return redirect(url_for('login'))


# -----------------------------------------------------------------------------------------------------


# Display class record ------------------------------------------------------------------------------

@app.route('/classrecord')
def classRecord():
   if 'loggedin' in session and session['username'] != 'admin': 
      return render_template('classRecord.html')
   return redirect(url_for('login'))

@app.route('/showrecord', methods = ['GET', 'POST'])
def showRecord():
   if 'loggedin' in session and session['username'] != 'admin': 
      import classRecordDBS
      if request.method == 'POST':
         year = request.form.get('year')
         division = request.form.get('division')
         delete = request.form.get('delete')
         # print(year,division)
         if delete == 'delete':
            classRecordDBS.delete_data(year,division)
            return redirect(url_for('classRecord'))
         else:
            data = classRecordDBS.getData(year,division)
            return render_template('classRecord.html',data=data)
         
   return redirect(url_for('login'))

# -----------------------------------------------------------------------------------------------------

# Take attendance -------------------------------------------------------------------------------------
@app.route('/takeattendance')
def takeAttendance():
   if 'loggedin' in session and session['username'] != 'admin': 
      data = []
      for i in ls:
         if i.name == session['username']:
            data = i.subject
      return render_template('takeAttendance.html',data = data)
   return redirect(url_for('login'))


@app.route('/searchstudents', methods = ['GET', 'POST'])
def searchStud():
   if 'loggedin' in session and session['username'] != 'admin': 
      import classRecordDBS
      if request.method == 'POST':
         year = request.form.get('year')
         division = request.form.get('division')
         date = request.form.get('date')
         lectype = request.form.get('lectype')
         subject = request.form.get('subject')
         timeslot = request.form.get('timeslot')
         batch = request.form.getlist('batch')
         print(batch)
         searchStud.atinfo = (year,division,date,lectype,subject,timeslot,batch)
         data = classRecordDBS.getData_batchvise(year,division,batch)
         total_data = (searchStud.atinfo, data)
         # print(total_data)
      return render_template('addAttendance.html',data = total_data)
   return redirect(url_for('login'))

@app.route('/addattendance', methods = ['GET', 'POST'])
def addAttendance():
   if 'loggedin' in session and session['username'] != 'admin': 
      import addAttendance
      if request.method == 'POST':
         present = request.form.getlist('present')
         # print(present)
         addAttendance.addAttendance(searchStud.atinfo,present)
         
      return redirect(url_for('takeAttendance'))
   return redirect(url_for('login'))

# -----------------------------------------------------------------------------------------------------


if __name__ == '__main__':
      app.run(debug = True)
