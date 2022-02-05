# Overview

This program acts as a simple data storage and retrieval program. Users store information related to their friends, including their birthday months and days, as well as their interests.
Users can enter information by either importing it from a csv file or through manual entry. They can also edit fields or delete information.

My purpose for writing this software was to help me improve my understanding of relational databases such as SQL and SQLite. In particular, I sought to become more comfortable with
incorporating relational databases and relational database functionality into programs that I wrote.

Please use this link to watch a demonstration of this program: [Software Demo Video](http://youtube.link.goes.here)

# Relational Database

This program utilizes SQLite, via the sqlite3 Python module, to store data that has been entered by users. SQLite is a C library that provides a disk-based database, meaning users 
don't need a separate server process. Users are able to access SQLite-created databases using a variation of the SQL query language. 

This program allows users to create and update a single SQLite database. This database consists of a single table with four columns: 'Name', 'Day', 'Month', and 'Interests'. All of the columns except for 'Day'
are varchar character fields, while 'Day' is an integer character field. Each entry is created on a separate row, allowing individual entries to be mupdated or maniupulated separately from all the others.

# Development Environment

Programs and Applications Used:
* Visual Studio Code 1.64.0
* Git / GitHub
* Python 3.10.1 64-bit

The following modules were used:
* csv
* sqlite3

# Useful Websites

* [SQLite Tutorial](https://www.sqlitetutorial.net)
* [SQL - W3Schools](https://www.w3schools.com/sql/)
* [Python.org - sqlite3](https://docs.python.org/3.8/library/sqlite3.html)

# Future Work

* Separate code into individual classes and files
* Allow users to query entries that are within 30 days of current date
* Provide a GUI to the program