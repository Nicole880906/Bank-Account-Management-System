# Bank-Account-Management-System

## Preview



## Introduction
This is an Intelligent Bank Account Management System based on Python Tkinter and MySQL.  
It provides functions including face recognition login, money transfer, and transaction history search.  

You can follow the steps below to implement the system.  

## Working
1. Install MySQL on local machine: https://dev.mysql.com/downloads/installer/  
2. Create a virtual environment using Anaconda  
    `conda create -n bams python=3.7`  
    `conda activate bams`  
    `pip install -r requirements.txt`
   > [!NOTE]
> If you are using MacOS, please also implement `pip3 install pyobjc==9.0.1`
4. Import database  
   _// login the mysql command_  
    `mysql -u root –p`  
   _// create database_  
    `mysql> CREATE DATABASE accountmanagement;`  
    `mysql> USE accountmanagement;`  
   _// import from sql file_  
    `mysql> source tables.sql`  
5. Login Interface  
    `python login.py`

## Demo
For more information, please check out the demo.
