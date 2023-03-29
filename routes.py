from flask import Flask, render_template, request,redirect, url_for, session
from addClass import *
from flask_mysqldb import MySQL
import mysql.connector
import os
import re
import pickle
f = 'fcinfo.pkl'
fs = 'subinfo.pkl'

class Faculty:
  # Constructor
   def __init__(self, id, name, subject, authority):
      self.id = id
      self.name = name
      self.subject  = subject
      self.authority =  authority

   # Function to create and append new student
   def accept(self, id, Name, Subject, authority):
      ob = Faculty(id, Name, Subject, authority)
      ls.append(ob)
      fwobj = open(f,'wb')
      pickle.dump(ls,fwobj)

   # Function to display student details
   def display(self):
      frobj = open(f,'rb')
      ff = pickle.load(frobj)
      print(ff)

   # Search Function
   def search(self, rn):
      for i in range(len(ls)):
         if(ls[i].name == rn):
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

# print(1,ls[0].name)
obj = Faculty(0,'', {},'')

logindbs = mysql.connector.connect(user='root', password ='', host='localhost', database='login')
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
   logindbs = mysql.connector.connect(user='root', password='', host='localhost', database='login')
   lo_cur = logindbs.cursor()

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
         session['authority'] = account[0][1]
         session['username'] = account[0][2]
         
         # Redirect to home page    
         if session['authority'] == 'admin' or session['authority'] == 'yearcoordinator':
            return redirect(url_for('adminHome'))
         elif session['authority'] == 'master':
            return redirect(url_for('masterHome'))
         elif session['authority'] == 'student':
            year = account[0][4].split('@')[0]
            session['year'] = year
            return redirect(url_for('studentHome'))
         else:
            return redirect(url_for('home'))
      else:
         # Account doesnt exist or username/password incorrect
         msg = 'Incorrect username/password!'
   logindbs.close()
   return render_template('login.html', msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
   logindbs = mysql.connector.connect(user='root', password='', host='localhost', database='login')
   lo_cur = logindbs.cursor()
    # Output message if something goes wrong...
   msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
   if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
      # Create variables for easy access
      id = request.form['id']
      authoritiy = request.form['authoritiy']
      username = request.form['username']
      password = request.form['password']
      email = request.form['email']
      # print(username,password,email,authorities)

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
         obj.accept(id,username,{"Theory":[],"Practical":[]},authoritiy)
         lo_cur.execute('INSERT INTO account VALUES (%s, %s, %s, %s, %s)', (id, authoritiy, username, password, email,))
         logindbs.commit()
         msg = 'You have successfully registered!'
   
   elif request.method == 'POST':
      # Form is empty... (no POST data)
      msg = 'Please fill out the form!'
   # Show registration form with message (if any)
   logindbs.close()
   return render_template('register.html', msg=msg)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('usrename', None)
   session.pop('authority', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session and session['authority'] == 'Faculty' :
         account = {}
         # We need all the account info for the user so we can display it on the profile page
         lo_cur.execute('SELECT * FROM account WHERE id = %s', (session['id'],))
         account['data'] = lo_cur.fetchone()
         for i in ls:
            # print(i.name,session['username'])
            if i.name == session['username']: 
               account['subject'] = i.subject
         
         # Show the profile page with account info
         return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/home')
def home():
   # Check if user is loggedin
   if 'loggedin' in session and session['authority'] == 'Faculty':
      # User is loggedin show them the home page
      return render_template('home.html', username=session['username'])
   # User is not loggedin redirect to login page
   return redirect(url_for('login'))

# Master Pages ----------------------------------------------------------------
@app.route('/masterHome')
def masterHome():
   if 'loggedin' in session and session['authority'] == 'master' :
      return render_template('masterhome.html',username=session['username'])
   return redirect(url_for('login')) 

@app.route('/masterprofile')
def masterprofile():
   if 'loggedin' in session and session['authority'] == 'master' :
      lo_cur.execute('SELECT * FROM account WHERE id = %s', (session['id'],))
      account = lo_cur.fetchone()
      return render_template('masterprofile.html',account=account)
   return redirect(url_for('login')) 

@app.route('/masterclean')
def masterclean():
   if 'loggedin' in session and session['authority'] == 'master' :
      return render_template('masterclean.html')
   return redirect(url_for('login')) 

@app.route('/cleandata',methods = ['GET', 'POST'])
def cleandata():
   import cleandata
   year = request.form.get('year')
   cleandata.cleandata(year)
   return redirect(url_for('masterclean'))
    

# student Pages ------------------------------------------------------------
@app.route('/studenthome')
def studentHome():
   if 'loggedin' in session and session['authority'] == 'student' :
      return render_template('studenthome.html',username=session['username'])
   return redirect(url_for('login')) 

@app.route('/studentprofile')
def studentprofile():
   if 'loggedin' in session and session['authority'] == 'student' :
      lo_cur.execute('SELECT * FROM account WHERE id = %s', (session['id'],))
      account = lo_cur.fetchone()
      return render_template('studentprofile.html',account=account)
   return redirect(url_for('login')) 

@app.route('/studenttheory')
def studenttheory():
   if 'loggedin' in session and session['authority'] == 'student' :
      total = {}
      year = session['year']
      print(session['year'],subs)
      total['subs'] = subs['Theory'][year]
      return render_template('studenttheory.html',total=total)
   return redirect(url_for('login')) 

@app.route('/studenttheoryshow',methods = ['GET', 'POST'])
def studenttheoryshow():
   if 'loggedin' in session and session['authority'] == 'student' :
      import studentattendance 
      total = {}
      year = session['year']  
      roll = session['id']
      total['name'] = session['username']
      subject = request.form.get('subject')
      total['subject'] = subject
      total['data'] = studentattendance.studenttAttendance_theory(roll,year,subject)
      return render_template('studenttheoryshow.html',total=total)
   return redirect(url_for('login')) 

@app.route('/studentpractical')
def studentpractical():
   if 'loggedin' in session and session['authority'] == 'student' :
      total = {}
      year = session['year']
      # print(session['year'],subs)
      total['subs'] = subs['Practical'][year]
      return render_template('studentpractical.html',total=total)
   return redirect(url_for('login')) 

@app.route('/studentpracticalshow',methods = ['GET', 'POST'])
def studentpracticalshow():
   if 'loggedin' in session and session['authority'] == 'student' :
      import studentattendance 
      total = {}
      year = session['year']  
      roll = session['id']
      total['name'] = session['username']
      subject = request.form.get('subject')
      total['subject'] = subject
      total['data'] =studentattendance.studenttAttendance_practical(roll, year,subject)
      return render_template('studentpracticalshow.html',total=total)
   return redirect(url_for('login')) 


@app.route('/studentdefaulter')
def studentdefaulter():
   if 'loggedin' in session and session['authority'] == 'student' :
      import studentattendance 
      total = {}
      year = session['year']  
      roll = session['id']
      total['name'] = session['username']
      total['data'] = studentattendance.studenttAttendance_defaulter(roll,year)
      return render_template('studentdefaulter.html',total=total)
   return redirect(url_for('login')) 



# Admin Pages -----------------------------------------------------------------
@app.route('/adminHome')
def adminHome():
   if 'loggedin' in session and session['authority'] == 'yearcoordinator' or session['authority'] == 'admin':
      name = []
      subs = []
      for i in ls:
         name.append(i.name)
         subs.append(i.subject)
         print(name,subs)
      # print(faculty.obj.getName(1))
      all = [name,subs]
      return render_template('adminhome.html',ls = all)
   return redirect(url_for('login'))

@app.route('/manageFaculty')
def manageFaculty():
   if 'loggedin' in session and session['authority'] == 'yearcoordinator' or session['authority'] == 'admin':
      faculty = []
      for i in ls:
         faculty.append(i.name) 
      return render_template('managefaculty.html',faculty = faculty)
   return redirect(url_for('login'))

@app.route('/selectSubject',methods = ['GET', 'POST'])
def selectSubject():
   if 'loggedin' in session and session['authority'] == 'yearcoordinator' or session['authority'] == 'admin':
      fsub = open(fs,'rb')
      subs = pickle.load(fsub)
      all = {}
      all['rem_subs_th'] = []
      all['rem_subs_pr'] = []
      faculty = request.form.get('faculty')
      session ['fc'] = faculty
      for i in ls:
         if i.name == faculty:
            fsubs = i.subject
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
      return render_template('selectSubject.html',all = all)
   return redirect(url_for('login'))

@app.route('/assignSubject',methods = ['GET', 'POST'])
def assignSubject():
   subs_th = request.form.getlist('subs_th')
   subs_pr = request.form.getlist('subs_pr')
   fc = session['fc']
   print(subs_th,subs_pr)

   for i in ls:
      if i.name == fc:
         i.subject['Theory'] =  subs_th
         i.subject['Practical'] = subs_pr
   
   fwobj = open(f,'wb')
   pickle.dump(ls,fwobj)
   return redirect(url_for('manageFaculty'))


@app.route('/registerFaculty', methods=['GET', 'POST'])
def registerFaculty():
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
         obj.accept(id,username,{"Theory":[],"Practical":[]})
         lo_cur.execute('INSERT INTO account VALUES (%s, %s, %s, %s)', (id,username, password, email,))
         logindbs.commit()

   elif request.method == 'POST':
      # Form is empty... (no POST data)
      msg = 'Please fill out the form!'

   return redirect(url_for('manageFaculty'))


@app.route('/removeFaculty',methods = ['GET', 'POST'])
def removeFaculty():
   import removeFaculty
   faculty = request.form.get('faculty')
   id = None
   for i in ls:
      if i.name == faculty:
         id = i.id
   removeFaculty.removeFaculty(faculty,id)
   obj.delete(faculty)
   return redirect(url_for('manageFaculty'))

@app.route('/manageSubject',methods = ['GET', 'POST'])
def manageSubject():
   if 'loggedin' in session and session['authority'] == 'yearcoordinator' or session['authority'] == 'admin':
      if request.method == 'POST':
         fsub = open(fs,'rb')
         subs = pickle.load(fsub)
         all={}
         year = request.form.get('year')
         subtype = request.form.get('subtype')
         all['year'] = year
         all['subs'] = subs[subtype][year]
         session ['year_for_subject'] = year
         session ['subtype'] = subtype
         return render_template('manageSubject2.html',all=all)
      return render_template('manageSubject1.html')
   return redirect(url_for('login'))

@app.route('/addsubject',methods = ['GET', 'POST'])
def addSubject():
   if 'loggedin' in session and session['authority'] == 'yearcoordinator' or session['authority'] == 'admin':
      import addSubject
      subject = request.form.get('subject')
      year = session['year_for_subject']
      subtype = session ['subtype']
      addSubject.addsubject(subtype,year,subject)
      return redirect(url_for('manageSubject'))
   return redirect(url_for('login'))
   
@app.route('/adminProfile')
def adminProfile():
   if 'loggedin' in session and session['authority'] == 'yearcoordinator' or session['authority'] == 'admin':
      lo_cur.execute('SELECT * FROM account WHERE id = %s', (session['id'],))
      account = lo_cur.fetchone()
      return render_template('adminprofile.html',account=account)
   return redirect(url_for('login'))

@app.route('/deletetheory')
def deletetheory():
   if 'loggedin' in session and session['authority'] == 'yearcoordinator' or session['authority'] == 'admin':
      data = []
      for i in ls:
         if i.name == session['username']:
            data = i.subject
      return render_template('deletetheory.html',data=data)
   return redirect(url_for('login'))

@app.route('/deletetheoryAttendance',methods = ['GET', 'POST'])
def deletetheoryAttendance():
   if 'loggedin' in session and session['authority'] == 'yearcoordinator' or session['authority'] == 'admin':
      import deleteattendance
      year = request.form.get('year')
      division = request.form.get('division')
      date = request.form.get('date')
      subject = request.form.get('subject')
      batch = request.form.getlist('batch')
      deleteattendance.deleteAttendanceTheory(year,division,date,subject,batch,"Theory")
      return redirect(url_for('deletetheory'))
   return redirect(url_for('login'))


@app.route('/deletepractical')
def deletepractical():
   if 'loggedin' in session and session['authority'] == 'yearcoordinator' or session['authority'] == 'admin':
      data = []
      for i in ls:
         if i.name == session['username']:
            data = i.subject
      return render_template('deletepractical.html',data=data)
   return redirect(url_for('login'))

@app.route('/deletepracticalAttendance',methods = ['GET', 'POST'])
def deletepracticalAttendance():
   if 'loggedin' in session and session['authority'] == 'yearcoordinator' or session['authority'] == 'admin':
      import deleteattendance
      year = request.form.get('year')
      division = request.form.get('division')
      date = request.form.get('date')
      subject = request.form.get('subject')
      timeslot = request.form.get('timeslot')
      batch = request.form.getlist('batch')
      deleteattendance.deleteAttendancePractical(year,division,date,subject,timeslot,batch,"Practical")
      return redirect(url_for('deletepractical'))
   return redirect(url_for('login'))


# adding class to dataset -----------------------------------------------------------------------------
@app.route('/addclass')
def addClass():
   if 'loggedin' in session and session['authority'] == 'yearcoordinator' or session['authority'] == 'admin':
      return render_template('addClass.html')
   return redirect(url_for('login'))

@app.route('/addclass', methods = ['GET', 'POST'])
def addDataset():
   if 'loggedin' in session and session['authority'] == 'yearcoordinator' or session['authority'] == 'admin':
      if request.method == 'POST':
         uploaded_file = request.files['file']
         year = request.form.get('year')
         div = request.form.get('division')
         if uploaded_file.filename != '':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(file_path)
            parseCSV(file_path,str(year),str(div))
      return redirect(url_for('addClass'))
   return redirect(url_for('login'))

# -----------------------------------------------------------------------------------------------------

# adding student to database --------------------------------------------------------------------------
@app.route('/addstudent')
def addStudent():
   if 'loggedin' in session and session['authority'] == 'yearcoordinator' or session['authority'] == 'admin':
      return render_template('addStudent.html')
   return redirect(url_for('login'))

@app.route('/addstudent', methods = ['GET', 'POST'])
def addStud():
   if 'loggedin' in session and session['authority'] == 'yearcoordinator' or session['authority'] == 'admin':
      import addStudentDBS
      if request.method == 'POST':
         roll = request.form.get('roll')
         name = request.form.get('name')
         prn = request.form.get('prn')
         year = request.form.get('year')
         division = request.form.get('division')
         batch = request.form.get('batch')
         addStudentDBS.addstud(roll,name,prn,year,division,batch)
      return redirect(url_for('addStudent'))

   return redirect(url_for('login'))

# -----------------------------------------------------------------------------------------------------

# other attendance ---------------------------------------------------------------------------
@app.route('/other')
def other():
   if 'loggedin' in session and session['authority'] == 'Faculty': 
      data = []
      for i in ls:
         if i.name == session['username']:
            data = i.subject
      return render_template('other.html',data=data)
   redirect(url_for('login'))

@app.route('/searchstudentother', methods=['GET', 'POST'])
def searchStudentOther():
   if 'loggedin' in session and session['authority'] == 'Faculty': 
      import classRecordDBS
      import dailyreport
      if request.method == 'POST':
         year = request.form.get('year')
         division = request.form.get('division')
         date = request.form.get('date')
         subject = request.form.get('subject')
         batch = request.form.getlist('batch')
         bt = ', '.join(batch)
         searchStudentOther.atinfo = (year,division,date,subject,batch)
         data = classRecordDBS.getData_batchvise(year,division,batch)
         data.sort()
         # print(data)
         total_data = (searchStudentOther.atinfo, data,bt)
         roll = []
         for i in data:
            roll.append(i[0])
         session['roll'] = roll
      return render_template('addAttendanceOther.html',data = total_data)
   return redirect(url_for('login'))

@app.route('/addOtherAttendance', methods = ['GET','POST'])
def addOtherAttendance():
   if 'loggedin' in session and session['authority'] == 'Faculty': 
      import addAttendance
      count = request.form.getlist('count')
      addAttendance.addOtherAttendance(searchStudentOther.atinfo,count,session['roll'])
      return redirect(url_for('theoryAttendance'))
   return redirect(url_for('login'))

# Theory--------------------
@app.route('/subjectAttendance_theory')
def subjectAttendance_theory():
   if 'loggedin' in session and session['authority'] == 'Faculty': 
      data = []
      for i in ls:
         if i.name == session['username']:
            data = i.subject
      return render_template('subjectAttendance_theory.html',data = data)
   return redirect(url_for('login'))

@app.route('/subjectTable_theory', methods = ['GET', 'POST'])
def subjectTable_theory():
   if 'loggedin' in session and session['authority'] == 'Faculty': 
      import attendanceDBS
      if request.method == 'POST':
         year = request.form.get('year')
         division = request.form.get('division')
         subject = request.form.get('subject')
         sdate = request.form.get('sdate')
         edate = request.form.get('edate')
         data = attendanceDBS.subjectAttendance_theory(year,division,subject,sdate,edate)
      return render_template('subjectTable_theory.html',data=data)
   return redirect(url_for('login'))

# Practical---------------------------------------------------------------------------
@app.route('/subjectAttendance_practical')
def subjectAttendance_practical():
   if 'loggedin' in session and session['authority'] == 'Faculty': 
      data = []
      for i in ls:
         if i.name == session['username']:
            data = i.subject
      return render_template('subjectAttendance_practical.html',data = data)
   return redirect(url_for('login'))

@app.route('/subjectTable_practical', methods = ['GET', 'POST'])
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
         data = attendanceDBS.subjectAttendance_practical(year,division,subject,batch,sdate,edate)
      return render_template('subjectTable_practical.html',data=data)
   return redirect(url_for('login'))

# ---------------------------------------------------------------------------
@app.route('/classAttendance')
def classAttendance():
   if 'loggedin' in session and session['authority'] == 'Faculty': 
      return render_template('classAttendance.html')
   return redirect(url_for('login'))


@app.route('/classTable', methods = ['GET', 'POST'])
def classTable():
   if 'loggedin' in session and session['authority'] == 'Faculty': 
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

# ---------------------------------------------------------------------
@app.route('/defaulter')
def defaulter():
   if 'loggedin' in session and session['authority'] == 'Faculty': 
      return render_template('defaulter.html')
   return redirect(url_for('login'))

@app.route('/defaultertable', methods = ['GET', 'POST'])
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
         data = attendanceDBS.defaulterData(year,division,sdate,edate,defaulter)
         # print(data)
      return render_template('defaulterTable.html',data=data)
   return redirect(url_for('login'))

# -----------------------------------------------------------------------------------------------------


# Display class record ------------------------------------------------------------------------------

@app.route('/classrecord')
def classRecord():
   if 'loggedin' in session and session['authority'] == 'yearcoordinator' or session['authority'] == 'admin': 
      return render_template('classRecord.html')
   return redirect(url_for('login'))

@app.route('/showrecord', methods = ['GET', 'POST'])
def showRecord():
   if 'loggedin' in session and session['authority'] == 'yearcoordinator' or session['authority'] == 'admin': 
      import classRecordDBS
      if request.method == 'POST':
         year = request.form.get('year')
         division = request.form.get('division')
         # print(year,division)
         data = classRecordDBS.getData(year,division)
         return render_template('classRecord.html',data=data)
         
   return redirect(url_for('login'))

# -----------------------------------------------------------------------------------------------------

# Take attendance theory -------------------------------------------------------------------------------------
@app.route('/theoryAttendance')
def theoryAttendance():
   if 'loggedin' in session and session['authority'] == 'Faculty': 
      data = []
      for i in ls:
         if i.name == session['username']:
            data = i.subject
      return render_template('theoryAttendance.html',data = data)
   return redirect(url_for('login'))


@app.route('/searchstudents_theory', methods = ['GET', 'POST'])
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
         bt = ', '.join(batch)
         searchStud_theory.atinfo = (year,division,date,subject,timeslot,batch)
         data = classRecordDBS.getData_batchvise(year,division,batch)
         msg = dailyreport.check_session(year,division,date,timeslot)
         print(msg)
         data.sort()
         # print(data)
         total_data = (searchStud_theory.atinfo, data,bt,msg)
         roll = []
         for i in data:
            roll.append(i[0])
         session['roll'] = roll
      return render_template('addAttendance.html',data = total_data)
   return redirect(url_for('login'))

@app.route('/addattendance', methods = ['GET', 'POST'])
def addAttendance():
   if 'loggedin' in session and session['authority'] == 'Faculty': 
      import addAttendance
      if request.method == 'POST':
         present = request.form.getlist('present')
         # print(session['roll'])
         # print(searchStud_theory.atinfo)
         addAttendance.addAttendance_theory(searchStud_theory.atinfo,present,session['roll'])
         addAttendance.addattendance_daily(searchStud_theory.atinfo,present,session['roll'],"Theory")
      return redirect(url_for('theoryAttendance'))
   return redirect(url_for('login'))

# Take attendance practical -------------------------------------------------------------------------------------
@app.route('/practicalAttendance')
def practicalAttendance():
   if 'loggedin' in session and session['authority'] == 'Faculty': 
      data = []
      for i in ls:
         if i.name == session['username']:
            data = i.subject
      return render_template('practicalAttendance.html',data = data)
   return redirect(url_for('login'))

@app.route('/searchstudents_practical', methods = ['GET', 'POST'])
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
         msg = dailyreport.check_session_practical(year,division,date,batch,timeslot)
         print(msg)
         # print(batch)
         searchstudents_practical.atinfo = (year,division,date,subject,timeslot,batch)
         data = classRecordDBS.getData_batchvise(year,division,batch)
         data.sort()
         total_data = (searchstudents_practical.atinfo, data,msg)
         roll = []
         for i in data:
            roll.append(i[0])
         session['roll'] = roll
      return render_template('addAttendancePractical.html',data = total_data)
   return redirect(url_for('login'))

@app.route('/addAttendance__practical', methods = ['GET', 'POST'])
def addAttendance__practical():
   if 'loggedin' in session and session['authority'] == 'Faculty': 
      import addAttendance
      if request.method == 'POST':
         present = request.form.getlist('present')
         # print(session['roll'])
         # print(searchstudents_practical.atinfo)
         addAttendance.addAttendance_practical(searchstudents_practical.atinfo,present,session['roll'])
         addAttendance.addattendance_daily(searchstudents_practical.atinfo,present,session['roll'],"Practical")

      return redirect(url_for('practicalAttendance'))
   return redirect(url_for('login'))

@app.route('/dailyreport')
def dailyreport():
   if 'loggedin' in session and session['authority'] == 'Faculty': 
      return render_template('dailyreport.html')
   return redirect(url_for('login'))

@app.route('/dailyreporttable',methods=['GET', 'POST'])
def dailyreporttable():
   if 'loggedin' in session and session['authority'] == 'Faculty': 
      import dailyreport
      year = request.form.get('year')
      div = request.form.get('division')
      date = request.form.get('date')
      data = dailyreport.dailyreport(year,div,date)
      dailyreporttable.atinfo = (year,div,date)
      return render_template('dailyreporttable.html',data=data)
   return redirect(url_for('login'))

@app.route('/updatedailyreport',methods=['GET', 'POST'])
def updatedailyreport():
   if 'loggedin' in session and session['authority'] == 'Faculty': 
      import dailyreport
      reamrks = request.form.getlist('remark')
      dailyreport.updatedailyreport(dailyreporttable.atinfo,reamrks)
      return redirect(url_for('dailyreport'))
   return redirect(url_for('login'))

if __name__ == '__main__':
      app.run(debug = True)
