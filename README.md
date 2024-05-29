# Face-Recognition-using-KivyMD

# So what to do once you have my.... Our code:)

## First thing is to fix the database which is needed.

Stepp 1:
  Open Terimal or however you manage your MySQL Tables.
  
Step 2:
  write the Sql code:
    $ CREATE DATABASE loginform;
    $ USE loginform;
    $ CREATE TABLE (
    $ email varchar(255) primary key,
    $ password varchar(255));

Step 3:
  Check that the Table is create correctly, with SQL code:
    $ DESC logindata;
    
Step 4:
  Add dummy data so that you can use for testing application
  SQl code:
    $ INSERT INTO logindata VALUES('kevenisboss@gmail.com','keven');

Step 5:
  On line 715 and 755 you will find a mysql connector,
  database = mysql.connector.Connect(host="localhost", user="root", password="12345678;", database="loginform")
  what you need to do is change the password to your database password for when you created it!
  
  <<<<<<<< Don't forget change for both 715 and 755, 715 is for login class and 755 is for signup class >>>>>>>>

## Okay now your done with the database stuff!


  
