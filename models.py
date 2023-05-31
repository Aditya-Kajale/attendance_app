import mysql.connector

dbs = mysql.connector.connect(
    user='root', password='root@123', host='localhost', database='students')
dbscursor = dbs.cursor()

# create students database
# 'students' database needs to created manually
sql = "CREATE TABLE `students`.`btech` (`ROLL_NO` INT(11) NOT NULL , `NAME` TEXT NOT NULL , `YEAR` TEXT NOT NULL , `DIVISION` TEXT NOT NULL , `BATCH` TEXT NOT NULL , `SPHONE` TEXT NOT NULL , `PPHONE` TEXT NOT NULL ) ;"
dbscursor.execute(sql)
dbs.commit()
sql = "CREATE TABLE `students`.`ty` (`ROLL_NO` INT(11) NOT NULL , `NAME` TEXT NOT NULL , `YEAR` TEXT NOT NULL , `DIVISION` TEXT NOT NULL , `BATCH` TEXT NOT NULL , `SPHONE` TEXT NOT NULL , `PPHONE` TEXT NOT NULL ) ;"
dbscursor.execute(sql)
dbs.commit()
sql = "CREATE TABLE `students`.`sy` (`ROLL_NO` INT(11) NOT NULL , `NAME` TEXT NOT NULL , `YEAR` TEXT NOT NULL , `DIVISION` TEXT NOT NULL , `BATCH` TEXT NOT NULL , `SPHONE` TEXT NOT NULL , `PPHONE` TEXT NOT NULL ) ;"
dbscursor.execute(sql)
dbs.commit()


# for theory dataabase
sql = "CREATE DATABASE theory_btech"
dbscursor.execute(sql)
sql = "CREATE DATABASE theory_ty"
dbscursor.execute(sql)
sql = "CREATE DATABASE theory_sy"
dbscursor.execute(sql)


# for practical dataabase
sql = "CREATE DATABASE practical_btech"
dbscursor.execute(sql)
sql = "CREATE DATABASE practical_ty"
dbscursor.execute(sql)
sql = "CREATE DATABASE practical_sy"
dbscursor.execute(sql)


# for marks
sql = "CREATE DATABASE marks"
dbscursor.execute(sql)
sql = "CREATE TABLE `marks`.`grievancee` (`Roll` INT(11) NOT NULL , `Examtype` TEXT NOT NULL , `Year` TEXT NOT NULL , `Division` TEXT NOT NULL , `Subject` TEXT NOT NULL , `Marks` TEXT NOT NULL , `Status` TEXT NOT NULL DEFAULT 'Remaining')"
dbscursor.execute(sql)


# for login
sql = "CREATE DATABASE login"
dbscursor.execute(sql)
sql = "CREATE TABLE `login`.`account` (`id` INT(11) NOT NULL , `authorities` TEXT NOT NULL , `username` TEXT NOT NULL , `password` TEXT NOT NULL , `email` TEXT NOT NULL , `SUB` TEXT NOT NULL )"
dbscursor.execute(sql)
sql = "INSERT INTO `login`.`account` (`id`, `authorities`, `username`, `password`, `email`, `SUB`) VALUES ('1', 'admin', 'admin', 'admin', 'admin@gmail.com', {})"
dbscursor.execute(sql)
dbs.commit()

# for daily
sql = "CREATE DATABASE daily_cse"
dbscursor.execute(sql)
