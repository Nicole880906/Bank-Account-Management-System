# Bank-Account-Management-System

## Preview

![image](https://github.com/Nicole880906/Bank-Account-Management-System/blob/development/demo/login.png)
![image](https://github.com/Nicole880906/Bank-Account-Management-System/blob/development/demo/home.png)
![image](https://github.com/Nicole880906/Bank-Account-Management-System/blob/development/demo/accountInfo.png)
![image](https://github.com/Nicole880906/Bank-Account-Management-System/blob/development/demo/transactionDetails.png)

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

3. Import database  
   login the mysql command_  
    `mysql -u root –p`  
   create database_  
    `mysql> CREATE DATABASE accountmanagement;`  
    `mysql> USE accountmanagement;`  
   import from sql file_  
    `mysql> source tables.sql`

4. Login Interface  
   `python login.py`

## Demo

For more information, please check out the demo: https://drive.google.com/file/d/1BBrE1fsoePYOvf5u_vC1J4eTVHuETDYb/view?usp=drive_link
