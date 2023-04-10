from routes import mysql_stud
import json
import mysql.connector


def assignSubjectToFaculty(divs,branch,faculty):
    logindbs = mysql.connector.connect(user='root', password='', host='localhost', database='login')
    lo_cur = logindbs.cursor()
    # print('OLD - ', faculty[-1] )
    subs = json.loads(faculty[-1])
    username = faculty[2]
    id = faculty[0]
    for i in subs:
        for j in subs[i]:
            for k in subs[i][j]:
                for h in subs[i][j][k]:
                    subs[i][j][k][h] = []
    print(divs)
    print(branch)
    for i in divs:
        data = i.split('/')
        subs[data[0]][data[1]][data[2]][data[3]] = []
        # if data[3] not in subs[data[0]][data[1]][data[2]]:

    for i in branch:
        data = i.split('/')
        subs[data[0]][data[1]][data[2]][data[3]].append(data[4])


    delind = []
    for i in subs:
        for j in subs[i]:
            for k in subs[i][j]:
                for h in subs[i][j][k]:
                    if subs[i][j][k][h] == []:
                        # del subs[i][j][k][h]
                        delind.append([i,j,k,h])
    for i in delind:
        del subs[i[0]][i[1]][i[2]][i[3]]
        
    subs = json.dumps(subs)
    print('NEW - ',subs)
    
    sql = "UPDATE `account` SET `SUB`= %s WHERE `username`=%s "
    val = (subs,username,)
    lo_cur.execute(sql,val)
    logindbs.commit()
    logindbs.close()
