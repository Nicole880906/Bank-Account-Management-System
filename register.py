import urllib
import numpy as np
import mysql.connector
import cv2
import os
import pyttsx3
import pickle
from datetime import datetime
import sys
import PySimpleGUI as sg
from tkinter import *
import tkinter.messagebox as Messagebox
from tkmacosx import Button

class Register:
	def login(self):
		self.root.destroy()
		import login

	def signup(self):
		if (self.userid.get() == "" or self.username.get() == "" or self.password.get() == "" or self.cpassword.get() == ""):
			Messagebox.showerror('Warning','All Fields Are Required.')
		elif(self.password.get() != self.cpassword.get()):
			Messagebox.showerror('Warning','Passwords and ConfirmPasswords are different.')	
		else:
			print("Connect")
			myconn = mysql.connector.connect(host="localhost", user="root", passwd="YourPassword", database="accountmanagement")
			now = datetime.now()
			time = now.strftime("%H:%M:%S")
			date = now.strftime("%Y-%m-%d")
			cursor = myconn.cursor()		
			cursor.execute("select * from Customer where email=%s",(self.userid.get(),))
			row = cursor.fetchone()
			if row != None:
				Messagebox.showerror("Warning","Userid Already Exist, Please try with another Userid")
			else:
				cursor.execute("insert into Customer(email, name, passwords, login_time, login_date) values (%s,%s,%s,%s,%s)",(self.userid.get(), self.username.get(), self.password.get(),time, date))
				cursor.execute("commit")

				Messagebox.showinfo("Success","Your account has been successfully registered. Please complete the face-capture procedure")
				self.facecapture()
						
	def facecapture(self):
		faceCascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
		video_capture = cv2.VideoCapture(0)

		# Specify the `user_name` and `NUM_IMGS`.
		user_name = self.username.get()
		NUM_IMGS = 300
		if not os.path.exists('data/{}'.format(user_name)):
    			os.mkdir('data/{}'.format(user_name))

		cnt = 1
		font = cv2.FONT_HERSHEY_SIMPLEX
		bottomLeftCornerOfText = (80, 50)
		fontScale = 1
		fontColor = (102, 102, 225)
		lineType = 2

		# Open camera
		while cnt <= NUM_IMGS:
			# Capture frame-by-frame
    			ret, frame = video_capture.read()

    			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    			"""
    			faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,
        				minSize=(30, 30),flags=cv2.CASCADE_SCALE_IMAGE,)

    			# Draw a rectangle around the faces
    			for (x, y, w, h) in faces:
        				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    			msg = "Saving {}'s Face Data [{}/{}]".format(user_name, cnt, NUM_IMGS)
    			cv2.putText(frame, msg,bottomLeftCornerOfText,font,fontScale,fontColor,lineType)

    			"""

    			# Display the resulting frame
    			cv2.imshow('Video', frame)
    			# Store the captured images in `data/Jack`
    			cv2.imwrite("data/{}/{}{:03d}.jpg".format(user_name, user_name, cnt), frame)
    			cnt += 1

    			key = cv2.waitKey(100)

		# When everything is done, release the capture
		video_capture.release()
		cv2.destroyAllWindows()

		Messagebox.showinfo("Success","Your account has been successfully registered")
		import train
		self.root.destroy()
		import login


	def __init__(self):
		self.root = Tk()
		self.root.title("Register a New Account")
		self.root.geometry('800x500')
		self.root["bg"] = "#F3F3FA"
        
		#Set the top
		frametop = Frame(self.root, bg = '#A3D1D1')
		frametop.pack(side = TOP, fill = BOTH)
		Label(frametop, text = 'Register', bg = '#A3D1D1', font=('arial',40)).pack()


		#Build a register interface
		registerframe = Frame(self.root, bg = '#D8D8EB')
		registerframe.pack(side = RIGHT, expand = 1)

		Label(registerframe, text = "userid" , bg = '#D8D8EB').grid(row = 1, column = 1, padx = 5, pady = 5)
		Label(registerframe, text = "username" , bg = '#D8D8EB').grid(row = 2, column = 1, padx = 5, pady = 5)
		Label(registerframe, text = "passwords", bg = '#D8D8EB').grid(row = 3, column = 1, padx = 5, pady = 5)
		Label(registerframe, text = "comfirm passwords", bg = '#D8D8EB').grid(row = 4, column = 1, padx = 5, pady = 5)
		
		
		self.userid = StringVar()
		self.username = StringVar()
		self.password = StringVar()
		self.cpassword = StringVar()
		userid = Entry(registerframe, textvariable = self.userid).grid(row = 1, column = 2, padx = 5, pady = 5)
		username = Entry(registerframe, textvariable = self.username).grid(row = 2, column = 2, padx = 5, pady = 5)
		password = Entry(registerframe, textvariable = self.password).grid(row = 3, column = 2, padx = 5, pady = 5)
		comfirmpassword = Entry(registerframe, textvariable = self.cpassword).grid(row = 4, column = 2, padx = 5, pady = 5)
		
		registerbutton  = Button(registerframe, text = "Register" , command = self.signup).grid(row = 5, column = 1, padx = 5, pady = 5)
		loginbutton = Button(registerframe, text = "Already have an account.", command = self.login).grid(row = 5, column = 2, padx = 5, pady = 5)

		self.root.mainloop()
	

Register()
