# # import pickle
# # # # import pandas as pd
# # # # # import connection as cn
# # # # from datetime import date, timedelta
# # # # import mysql.connector 


# # # # # # at_btech = mysql.connector.connect(user='root', password='', host='localhost', database='theory_btech')

# # # # # # btech = at_btech.cursor()

# # # # # # sdate = date(2022,10,22)   # start date
# # # # # # edate = date(2022,10,31)   # end date
# # # # # # a = [sdate+timedelta(days=x) for x in range((edate-sdate).days)]
# # # # # # print(a)
# # # # # # tt = []
# # # # # # for i in a:
# # # # # #     ss = i.strftime("%Y_%m_%d")
# # # # # #     tt.append(ss)

# # # # # # # dts = '+'.join(tt)
# # # # # # # print(tt)

# # # # # # ll = []
# # # # # # try:
# # # # # #     for i in tt:
# # # # # #         print(i)
# # # # # #         sql = 'SELECT {} AS "total" FROM se WHERE division = "A"'.format(i)
# # # # # #         btech.execute(sql)
# # # # # #         data = btech.fetchall()
# # # # # #         # print(data)
# # # # # #         for k in range(len(data)):
# # # # # #             data[k] = data[k][0]
# # # # # #         ll.append(data)
# # # # # # except:
# # # # # #     print('except')

# # # # # # su = [sum(x) for x in zip(*ll)]
# # # # # # print(su)


# # # # # # # # # sdate = '2019-3-22'
# # # # # # # # # sdate = date(sdate)

# # # # # # print(faculty.obj.getName(2))

    



# # # # # # class Faculty:
# # # # # #   # Constructor
# # # # # #     def __init__(self, id, name, subject):
# # # # # #         self.id = id
# # # # # #         self.name = name
# # # # # #         self.subject  = subject
 
# # # # # #     # Function to create and append new student
# # # # # #     def accept(self, id, Name, Subject):
# # # # # #         ob = Faculty(id, Name, Subject)
# # # # # #         ls.append(ob)
# # # # # #         fwobj = open(f,'wb')
# # # # # #         pickle.dump(ls,fwobj)
 
# # # # # #     # Function to display student details
# # # # # #     def display(self, ob):
# # # # # #         frobj = open(f,'rb')
# # # # # #         ff = pickle.load(frobj)
# # # # # #         print(ff)

# # # # # #     # Search Function
# # # # # #     def search(self, rn):
# # # # # #         for i in range(len(ls)):
# # # # # #             if(ls[i].id == rn):
# # # # # #                 return i
 
# # # # # #     # Delete Function
# # # # # #     def delete(self, rn):
# # # # # #         i = obj.search(rn)
# # # # # #         print(i)
# # # # # #         del ls[i]
# # # # # #         fwobj = open(f,'wb')
# # # # # #         pickle.dump(ls,fwobj)
# # # # # #         print(ls)

# # # # # #     # Update Function
# # # # # #     def update(self, rn, No):
# # # # # #         i = obj.search(rn)
# # # # # #         roll = No
# # # # # #         ls[i].id = roll

# # # # # #     def getSubject(self,rn):
# # # # # #         i = obj.search(rn)
# # # # # #         return ls[i].subject

# # # # # #     def getName(self,rn):
# # # # # #         print('asdasd')
# # # # # #         i = obj.search(rn)
# # # # # #         print(i)
# # # # # #         return ls[i].name
# # # # # # try : 
# # # # # #     frobj = open(f,'rb')
# # # # # #     ff = pickle.load(frobj)
# # # # # #     ls = ff
# # # # # # except:
# # # # # #     ls = []

# # # # # # obj = Faculty(0,'', [])



# # # f = 'fcinfo.pkl'
# # f = 'subinfo.pkl'

subs = {"Theory":{"BTECH":['Software Engineering',
        'Big Data Analytics',
        'Cloud Computing',
        'Blockchain Technology',
        'Full Stack Development',
        'System Administration'],
        "TY":[],
        "SY":[],
        "FY":[]},
        "Practical":{"BTECH":['Big Data Analytics (PR)',
        'Cloud Computing (PR)',
        'Full Stack Development (PR)',
        'System Administration (PR)'],
        "TY":[],
        "SY":[],
        "FY":[]
        }}
# # # fc = []
# # # # # for reading 
# # frobj = open(f,'rb')
# # ff = pickle.load(frobj)
# # # fwobj = open(f,'wb')
# # # pickle.dump(subs,fwobj)
 

# # print(ff)

# gap = 8
# pre = 0
# for i in range (1,6):
#     for k in range(pre):
#         print(' ',end='')
    
#     print(i,end='')
#     for j in range (gap):
#         print(' ',end='')
#     if i!=5:
#         print(i)
#     if i==5:
#         print('')
#     gap-=2
#     pre+=1

# gap=2
# pre = 3
# for i in range(4,0,-1):
#     for k in range(pre):
#         print(' ',end='')
#     print(i,end='')
#     for j in range (gap):
#         print(' ',end='')
#     print(i)
#     gap +=2
#     pre-=1

temp = {"Theory":{"BTECH":['Software Engineering',
        'Big Data Analytics',
        'Cloud Computing',
        'Blockchain Technology',
        'Full Stack Development',
        'System Administration'],
        "TY":[],
        "SY":[],
        "FY":[]},   
        "Practical":{"BTECH":['Big Data Analytics (PR)',
        'Cloud Computing (PR)',
        'Full Stack Development (PR)',
        'System Administration (PR)'],
        "TY":[],
        "SY":[],
        "FY":[]
        }}

import json

sub = {"BTECH":{"A":{"THEORY":{},"PRACTICAL":{}},
                "B":{"THEORY":{},"PRACTICAL":{}}},
        "TY":{"A":{"THEORY":{},"PRACTICAL":{}},
                "B":{"THEORY":{},"PRACTICAL":{}}},
        "SY":{"A":{"THEORY":{},"PRACTICAL":{}},
                "B":{"THEORY":{},"PRACTICAL":{}}}}


res = json.loads(sub)
res['BTECH']['A']['THEORY']['Software Engineering'] = ['A1', 'A2', 'A3']
print(res['BTECH']['A']['THEORY'].keys())







