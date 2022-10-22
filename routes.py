from flask import Flask, render_template, request,redirect, url_for, session
from addClass import *
from flask_mysqldb import MySQL
from wtforms import SelectField
import os

app = Flask(__name__)

# for the database
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "students"
mysql_stud = MySQL(app)


UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

@app.route('/')
def home():
   return render_template('home.html')

# adding class to dataset -----------------------------------------------------------------------------
@app.route('/addclass')
def addClass():
   return render_template('addClass.html')

@app.route('/addclass', methods = ['GET', 'POST'])
def addDataset():
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

   return redirect(url_for('addClass'))\

# -----------------------------------------------------------------------------------------------------

# adding student to database --------------------------------------------------------------------------
@app.route('/addstudent')
def addStudent():
   return render_template('addStudent.html')

@app.route('/addstudent', methods = ['GET', 'POST'])
def addStud():
   import addStudentDBS
   if request.method == 'POST':
      roll = request.form.get('roll')
      name = request.form.get('name')
      prn = request.form.get('prn')
      year = request.form.get('year')
      division = request.form.get('division')
      addStudentDBS.addstud(roll,name,prn,year,division)
   return redirect(url_for('addStudent'))

# -----------------------------------------------------------------------------------------------------

# Display Attendacne record ---------------------------------------------------------------------------
@app.route('/attendancerecord')
def attendanceRecord():
   return render_template('attendanceRecord.html')



# -----------------------------------------------------------------------------------------------------


# Display class record ------------------------------------------------------------------------------

@app.route('/classrecord')
def classRecord():
   return render_template('classRecord.html')

@app.route('/showrecord', methods = ['GET', 'POST'])
def showRecord():
   import classRecordDBS
   if request.method == 'POST':
      year = request.form.get('year')
      division = request.form.get('division')
      # print(year,division)
      data = classRecordDBS.getData(year,division)
      # print(data)

   return render_template('classRecord.html',data=data)

# -----------------------------------------------------------------------------------------------------

# Take attendance -------------------------------------------------------------------------------------
@app.route('/takeattendance')
def takeAttendance():
   return render_template('takeAttendance.html')

@app.route('/searchstudents', methods = ['GET', 'POST'])
def searchStud():
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

@app.route('/addattendance', methods = ['GET', 'POST'])
def addAttendance():
   import addAttendance
   if request.method == 'POST':
      present = request.form.getlist('present')
      # print(present)
      addAttendance.addAttendance(searchStud.atinfo,present)
      
   return redirect(url_for('takeAttendance'))
# -----------------------------------------------------------------------------------------------------


if __name__ == '__main__':
      app.run(debug = True)
