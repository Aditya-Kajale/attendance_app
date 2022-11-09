from flask import Flask, render_template, request,redirect, url_for, session
from addClass import *
from flask_mysqldb import MySQL
from wtforms import SelectField
import mysql.connector
import os
import re

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
    import faculty
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
            # sql = 'INSERT INTO account VALUES (N, {}, {}, {})'
            lo_cur.execute('INSERT INTO account VALUES (%s, %s, %s, %s)', (id,username, password, email,))
            logindbs.commit()
            faculty.obj.accept(id,username,[])
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
      import faculty
      ls = faculty.ls
      name = []
      subs = []
      for i in ls:
         name.append(i.name)
         subs.append(i.subject)
      all = [name,subs]
      return render_template('adminhome.html',ls = all)
   return redirect(url_for('home'))

@app.route('/manageFaculty')
def manageFaculty():
   if 'loggedin' in session and session['username'] == 'admin':
      return render_template('managefaculty.html')
   return redirect(url_for('home'))

@app.route('/adminSubject')
def manageSubject():
   if 'loggedin' in session and session['username'] == 'admin':
      return render_template('managesubject.html')
   return redirect(url_for('home'))

@app.route('/adminProfile')
def adminProfile():
   if 'loggedin' in session and session['username'] == 'admin':
      lo_cur.execute('SELECT * FROM account WHERE id = %s', (session['id'],))
      account = lo_cur.fetchone()
      return render_template('adminprofile.html',account=account)
   return redirect(url_for('home'))



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
         if uploaded_file.filename != '':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            # set the file path
            uploaded_file.save(file_path)
            # print(file_path)
            print(year,div)
            parseCSV(file_path,str(year),str(div))

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
         # print(year,division)
         data = classRecordDBS.getData(year,division)
         # print(data)

      return render_template('classRecord.html',data=data)
   return redirect(url_for('login'))

# -----------------------------------------------------------------------------------------------------

# Take attendance -------------------------------------------------------------------------------------
@app.route('/takeattendance')
def takeAttendance():
   if 'loggedin' in session and session['username'] != 'admin': 
      return render_template('takeAttendance.html')
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
         faculty = request.form.get('faculty')
         timeslot = request.form.get('timeslot')
         searchStud.atinfo = (year,division,date,lectype,subject,faculty,timeslot)
         data = classRecordDBS.getData(year,division)
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
