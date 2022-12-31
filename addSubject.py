import pandas as pd
import mysql.connector
from datetime import date, timedelta
import pickle

at_btech = mysql.connector.connect(user='root', password='', host='localhost', database='theory_btech')
at_ty = mysql.connector.connect(user='root', password='', host='localhost', database='theory_ty')
at_sy = mysql.connector.connect(user='root', password='', host='localhost', database='theory_sy')
at_fy = mysql.connector.connect(user='root', password='', host='localhost', database='theory_fy')

btech = at_btech.cursor()
ty = at_ty.cursor()
sy = at_sy.cursor()
fy = at_fy.cursor()

fs = 'subinfo.pkl'
fsub = open(fs,'rb')
subs = pickle.load(fsub)

def addsubject(year,subject):
    # print(year,subject)
    subs[year].append(subject)
    # print(subs)
    subw = open(fs,'wb')
    pickle.dump(subs,subw)

    