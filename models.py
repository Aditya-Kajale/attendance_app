from routes import mysql_stud
import mysql.connector


# create students database
# 'students' database needs to created manually
cur = mysql_stud.connection.cursor()
sql = "CREATE TABLE `students`.`btech` (`ROLL_NO` INT(11) NOT NULL , `NAME` TEXT NOT NULL , `YEAR` TEXT NOT NULL , `DIVISION` TEXT NOT NULL , `BATCH` TEXT NOT NULL , `SPHONE` TEXT NOT NULL , `PPHONE` TEXT NOT NULL ) ;"
cur.execute(sql)
mysql_stud.connection.commit()
cur = mysql_stud.connection.cursor()
sql = "CREATE TABLE `students`.`ty` (`ROLL_NO` INT(11) NOT NULL , `NAME` TEXT NOT NULL , `YEAR` TEXT NOT NULL , `DIVISION` TEXT NOT NULL , `BATCH` TEXT NOT NULL , `SPHONE` TEXT NOT NULL , `PPHONE` TEXT NOT NULL ) ;"
cur.execute(sql)
mysql_stud.connection.commit()
sql = "CREATE TABLE `students`.`sy` (`ROLL_NO` INT(11) NOT NULL , `NAME` TEXT NOT NULL , `YEAR` TEXT NOT NULL , `DIVISION` TEXT NOT NULL , `BATCH` TEXT NOT NULL , `SPHONE` TEXT NOT NULL , `PPHONE` TEXT NOT NULL ) ;"
cur.execute(sql)
mysql_stud.connection.commit()


# for theory dataabase
sql = "CREATE DATABASE theory_btech"
cur.execute(sql)
sql = "CREATE DATABASE theory_ty"
cur.execute(sql)
sql = "CREATE DATABASE theory_sy"
cur.execute(sql)


# for practical dataabase
sql = "CREATE DATABASE practical_btech"
cur.execute(sql)
sql = "CREATE DATABASE practical_ty"
cur.execute(sql)
sql = "CREATE DATABASE practical_sy"
cur.execute(sql)


# for marks
sql = "CREATE DATABASE marks"
cur.execute(sql)
sql = "CREATE TABLE `grievancee` (`Roll` INT(11) NOT NULL , `Examtype` TEXT NOT NULL , `Year` TEXT NOT NULL , `Division` TEXT NOT NULL , `Subject` TEXT NOT NULL , `Marks` TEXT NOT NULL , `Status` TEXT NOT NULL DEFAULT 'Remaining')"
cur.execute(sql)


# for login
sql = "CREATE DATABASE login"
cur.execute(sql)
sql = "CREATE TABLE `account` (`id` INT(11) NOT NULL , `authorities` TEXT NOT NULL , `username` TEXT NOT NULL , `password` TEXT NOT NULL , `email` TEXT NOT NULL , `SUB` TEXT NOT NULL )"
cur.execute(sql)
sql = "INSERT INTO `account` (`id`, `authorities`, `username`, `password`, `email`, `SUB`) VALUES ('1', 'admin', 'admin', 'admin', 'admin@gmail.com', {})"
cur.execute(sql)

# for daily
sql = "CREATE DATABASE daily_cse"
cur.execute(sql)
