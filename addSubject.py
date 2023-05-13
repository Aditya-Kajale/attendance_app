import pandas as pd
import mysql.connector
from datetime import date, timedelta
import pickle

fs = 'subinfo.pkl'
fsub = open(fs, 'rb')
subs = pickle.load(fsub)


def addsubject(subtype, year, subject):
    at_btech = mysql.connector.connect(
        user='root', password='root@123', host='localhost', database='theory_btech')
    at_ty = mysql.connector.connect(
        user='root', password='root@123', host='localhost', database='theory_ty')
    at_sy = mysql.connector.connect(
        user='root', password='root@123', host='localhost', database='theory_sy')

    ap_btech = mysql.connector.connect(
        user='root', password='root@123', host='localhost', database='practical_btech')
    ap_ty = mysql.connector.connect(
        user='root', password='root@123', host='localhost', database='practical_ty')
    ap_sy = mysql.connector.connect(
        user='root', password='root@123', host='localhost', database='practical_sy')

    btech = at_btech.cursor()
    ty = at_ty.cursor()
    sy = at_sy.cursor()

    btechP = ap_btech.cursor()
    tyP = ap_ty.cursor()
    syP = ap_sy.cursor()

    if subtype == "Theory":
        if year == "BTECH":
            sql = "CREATE TABLE `theory_btech`.`{}` (`roll` INT NOT NULL , `name` VARCHAR(50) NOT NULL ,  `division` TEXT NOT NULL ) ENGINE = InnoDB;".format(
                subject)
            btech.execute(sql)
            at_btech.commit()

        elif year == "TY":
            sql = "CREATE TABLE `theory_ty`.`{}` (`roll` INT NOT NULL , `name` VARCHAR(50) NOT NULL ,  `division` TEXT NOT NULL ) ENGINE = InnoDB;".format(
                subject)
            ty.execute(sql)
            at_ty.commit()

        elif year == "SY":
            sql = "CREATE TABLE `theory_sy`.`{}` (`roll` INT NOT NULL , `name` VARCHAR(50) NOT NULL , `division` TEXT NOT NULL ) ENGINE = InnoDB;".format(
                subject)
            sy.execute(sql)
            at_sy.commit()

    elif subtype == "Practical":
        if year == "BTECH":
            sql = "CREATE TABLE `practical_btech`.`{}` (`roll` INT NOT NULL , `name` VARCHAR(50) NOT NULL ,  `division` TEXT NOT NULL , `batch` VARCHAR(5) NOT NULL ) ENGINE = InnoDB;".format(
                subject)
            btechP.execute(sql)
            ap_btech.commit()

        elif year == "TY":
            sql = "CREATE TABLE `practical_ty`.`{}` (`roll` INT NOT NULL , `name` VARCHAR(50) NOT NULL ,  `division` TEXT NOT NULL , `batch` VARCHAR(5) NOT NULL ) ENGINE = InnoDB;".format(
                subject)
            tyP.execute(sql)
            ap_ty.commit()

        elif year == "SY":
            sql = "CREATE TABLE `practical_sy`.`{}` (`roll` INT NOT NULL , `name` VARCHAR(50) NOT NULL , `division` TEXT NOT NULL , `batch` VARCHAR(5) NOT NULL ) ENGINE = InnoDB;".format(
                subject)
            syP.execute(sql)
            ap_sy.commit()

    at_btech.close()
    at_sy.close()
    at_ty.close()

    ap_btech.close()
    ap_sy.close()
    ap_ty.close()

    subs[subtype][year].append(subject)
    subw = open(fs, 'wb')
    pickle.dump(subs, subw)


def renamesubject(subtype, year, subjects):
    at_btech = mysql.connector.connect(
        user='root', password='root@123', host='localhost', database='theory_btech')
    at_ty = mysql.connector.connect(
        user='root', password='root@123', host='localhost', database='theory_ty')
    at_sy = mysql.connector.connect(
        user='root', password='root@123', host='localhost', database='theory_sy')

    ap_btech = mysql.connector.connect(
        user='root', password='root@123', host='localhost', database='practical_btech')
    ap_ty = mysql.connector.connect(
        user='root', password='root@123', host='localhost', database='practical_ty')
    ap_sy = mysql.connector.connect(
        user='root', password='root@123', host='localhost', database='practical_sy')

    btech = at_btech.cursor()
    ty = at_ty.cursor()
    sy = at_sy.cursor()

    btechP = ap_btech.cursor()
    tyP = ap_ty.cursor()
    syP = ap_sy.cursor()

    if subtype == "Theory":
        if year == "BTECH":
            for i in range(len(subjects)):
                subjects[i] = subjects[i].strip()
                if subjects[i] != '':
                    sql = 'ALTER TABLE `{}` RENAME TO `{}`'.format(
                        subs[subtype][year][i], subjects[i])
                    btech.execute(sql)
                    at_btech.commit()
                    subs[subtype][year][i] = subjects[i]
        elif year == "TY":
            for i in range(len(subjects)):
                subjects[i] = subjects[i].strip()
                if subjects[i] != '':
                    sql = 'ALTER TABLE `{}` RENAME TO `{}`'.format(
                        subs[subtype][year][i], subjects[i])
                    ty.execute(sql)
                    at_ty.commit()
                    subs[subtype][year][i] = subjects[i]
        elif year == "SY":
            for i in range(len(subjects)):
                subjects[i] = subjects[i].strip()
                if subjects[i] != '':
                    sql = 'ALTER TABLE `{}` RENAME TO `{}`'.format(
                        subs[subtype][year][i], subjects[i])
                    sy.execute(sql)
                    at_sy.commit()
                    subs[subtype][year][i] = subjects[i]

    elif subtype == "Practical":
        if year == "BTECH":
            for i in range(len(subjects)):
                subjects[i] = subjects[i].strip()
                if subjects[i] != '':
                    sql = 'ALTER TABLE `{}` RENAME TO `{}`'.format(
                        subs[subtype][year][i], subjects[i])
                    btechP.execute(sql)
                    ap_btech.commit()
                    subs[subtype][year][i] = subjects[i]
        elif year == "TY":
            for i in range(len(subjects)):
                subjects[i] = subjects[i].strip()
                if subjects[i] != '':
                    sql = 'ALTER TABLE `{}` RENAME TO `{}`'.format(
                        subs[subtype][year][i], subjects[i])
                    tyP.execute(sql)
                    ap_ty.commit()
                    subs[subtype][year][i] = subjects[i]
        elif year == "SY":
            for i in range(len(subjects)):
                subjects[i] = subjects[i].strip()
                if subjects[i] != '':
                    sql = 'ALTER TABLE `{}` RENAME TO `{}`'.format(
                        subs[subtype][year][i], subjects[i])
                    syP.execute(sql)
                    ap_sy.commit()
                    subs[subtype][year][i] = subjects[i]

    subw = open(fs, 'wb')
    pickle.dump(subs, subw)
