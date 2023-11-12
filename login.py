
from tkinter import *
from tkinter import ttk
from tkinter.tix import COLUMN
from tkmacosx import Button
from datetime import datetime
import cv2
import pickle
import pyttsx3
import numpy as np
import tkinter as tk
import mysql.connector
import PySimpleGUI as sg
import tkinter.messagebox as Messagebox


# Login Page
class Login:

	#Login button
	def presslogin(self):
		if(self.email.get() == "" or self.password.get() == ""):
			Messagebox.showerror(title = 'Warning', message = 'Please input both email and passwords!')
		else:
			myconn = mysql.connector.connect(host="localhost", user="root", passwd="YourPassword", database="accountmanagement")
			date = datetime.utcnow()
			now = datetime.now()
			current_time = now.strftime("%H:%M:%S")
			cursor = myconn.cursor()			
			cursor.execute("select * from Customer where email=%s and passwords=%s",(self.email.get(), self.password.get()))
			row = cursor.fetchone()
			if row == None:
				Messagebox.showerror("Error","Invalid email & Passwords")
			else:
				Messagebox.showinfo("Success","Welcome")
				self.login(self.email.get())
			myconn.close()

	#signup button
	def signup(self):
		self.window.destroy()
		import register

	#face recognition button
	def facecapture(self):
		# 1 Create database connection
		myconn = mysql.connector.connect(host="localhost", user="root", passwd="YourPassword", database="accountmanagement")
		date = datetime.utcnow()
		now = datetime.now()
		current_time = now.strftime("%H:%M:%S")
		cursor = myconn.cursor()

		# 2 Load recognize and read label from model
		recognizer = cv2.face.LBPHFaceRecognizer_create()
		recognizer.read("train.yml")

		labels = {"person_name": 1}
		with open("labels.pickle", "rb") as f:
			labels = pickle.load(f)
			labels = {v: k for k, v in labels.items()}

		# create text to speech
		engine = pyttsx3.init()
		rate = engine.getProperty("rate")
		engine.setProperty("rate", 175)

		# Define camera and detect face
		face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
		cap = cv2.VideoCapture(0)

		# 3 Open the camera and start face recognition
		a = True
		while(a):
			ret, frame = cap.read()
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=3)

			for (x, y, w, h) in faces:
				print(x, w, y, h)
				roi_gray = gray[y:y + h, x:x + w]
				roi_color = frame[y:y + h, x:x + w]
				# predict the id and confidence for faces
				id_, conf = recognizer.predict(roi_gray)

				# 3.1 If the face is recognized
				if conf >= 70:
					font = cv2.QT_FONT_NORMAL
					id = 0
					id += 1
					name = labels[id_]
					current_name = name
					color = (255, 0, 0)
					stroke = 2
					cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
					cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))

					# Find the customer's information in the database.
					select = "SELECT email, name, DAY(login_date), MONTH(login_date), YEAR(login_date) FROM Customer WHERE name='%s'" % (name)
					name = cursor.execute(select)
					result = cursor.fetchall()
					data = "error"

					for x in result:
						data = x
					# If the customer's information is not found in the database
					if data == "error":
						print("The customer", current_name, "is NOT FOUND in the database.")
						
						cap.release()
						cv2.destroyAllWindows()
						self.window.destroy()
						import register
					# If the customer's information is found in the database
					else:
						# Update the data in database
						update =  "UPDATE Customer SET login_date=%s WHERE name=%s"
						val = (date, current_name)
						cursor.execute(update, val)
						update = "UPDATE Customer SET login_time=%s WHERE name=%s"
						val = (current_time, current_name)
						cursor.execute(update, val)
						myconn.commit()
               
						hello = ("Hello ", current_name, "Welcom to the iKYC System")
						engine.say(hello)
						# engine.runAndWait()
						a = False

				# 3.2 If the face is unrecognized
				else: 
					color = (255, 0, 0)
					stroke = 2
					font = cv2.QT_FONT_NORMAL
					cv2.putText(frame, "UNKNOWN", (x, y), font, 1, color, stroke, cv2.LINE_AA)
					cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))
					hello = ("Your face is not recognized")
					engine.say(hello)
					a = a + 1
					 # engine.runAndWait()

			cv2.imshow('iKYC System', frame)
			k = cv2.waitKey(20) & 0xff
			if k == ord('q'):
				break
        
		cap.release()
		cv2.destroyAllWindows()
		Messagebox.showinfo("Success","Welcome")
		myconn = mysql.connector.connect(host="localhost", user="root", passwd="YourPassword", database="accountmanagement")
		cursor = myconn.cursor()
		cursor.execute("select email, passwords from Customer where name=%s",(current_name,))
		getinfo = cursor.fetchall()       
		self.login(getinfo[0][0])
		myconn.close()

	def __init__(self):
		self.window = Tk()
		self.window.title("Intelligent Know Your Customer")
		self.window.geometry('800x500')
		self.window["bg"] = "#F3F3FA"
        
		#Set the top
		frametop = Frame(self.window, bg = '#A3D1D1')
		frametop.pack(side = TOP, fill = BOTH)
		welcome = Label(frametop, text = 'WELCOME TO IKYC!', bg = '#A3D1D1', font=('arial',40)).pack()


		#Build a login interface
		loginframe = Frame(self.window, bg = '#D8D8EB')
		loginframe.pack(side = RIGHT, expand = 1)

		emaillbl = Label(loginframe, text = "Email" , bg = '#D8D8EB').grid(row = 1, column = 1, padx = 5, pady = 5)
		passwordlbl = Label(loginframe, text = "Passwords", bg = '#D8D8EB').grid(row = 2, column = 1, padx = 5, pady = 5)
		
		self.email = StringVar()
		self.password = StringVar()
		Entry(loginframe, textvariable = self.email).grid(row = 1, column = 2, columnspan = 3, padx = 5, pady = 5)
		Entry(loginframe, textvariable = self.password).grid(row = 2, column = 2, columnspan = 3, padx = 5, pady = 5)
		
		loginbutton = Button(loginframe, text = "LOG IN", command = self.presslogin).grid(row = 3, column = 1, padx = 5, pady = 5)
		signupbutton = Button(loginframe, text = "SIGN UP", command = self.signup).grid(row = 3, column = 2, padx = 5, pady = 5)
		face = PhotoImage(file = "./images/face.gif")
		facebutton   = Button(loginframe, image = face, command = self.facecapture).grid(row = 3, column = 4, padx = 5, pady = 5)

		self.window.mainloop()
	
	def login(self,user):
		self.window.destroy()
		iKYC(user)


class iKYC:

	def logout(self, user):
		self.root.destroy()

		self.confirm = Tk()
		self.confirm.title("LOG OUT")
		self.confirm.geometry('350x150')
		self.confirm.configure(bg ="#D8D8EB") 
		
		# empty = Label(self.confirm, text = "", height = 3)
		confirmlbl = Label(self.confirm, text = "Sure to Log Out?", font = ('arial',20), height = 3, bg ="#D8D8EB")
		yesBt = Button(self.confirm, text = "Yes", command = self.yes, width = 80, height = 40, bg ="#9191c2", borderwidth=0)
		noBt = Button(self.confirm, text = "No", command = lambda:self.no(user), width = 80, height = 40, bg ="#9191c2", borderwidth=0)
		
		confirmlbl.pack()
		yesBt.pack(anchor=tk.S,side=tk.RIGHT,padx=50,pady=10)
		noBt.pack(anchor=tk.S,side=tk.LEFT,padx=50,pady=10)



	def yes(self):
		self.confirm.destroy()
		Login()
		

	def no(self,user): 
		self.confirm.destroy()
		iKYC(user)


	def account(self,currentLogInUser):
		myconn = mysql.connector.connect(host="localhost", user="root", passwd="YourPassword", database="accountmanagement")
		cursor = myconn.cursor()
		cursor.execute("select distinct(A.account_num) from Customer C, Account A, linkCustomerAccount L where C.email = L.email and L.account_id = A.account_id and C.email=%s",(currentLogInUser,))
		self.useraccountnum = cursor.fetchall()
		if self.useraccountnum == None:
			Messagebox.showerror("Error","Invalid Username & Passwords")
		else:
			f1greet = Label(self.frame1, text = "Hi! Your accounts are shown below:", font = ('arial', 30), bg = '#D1E9E9').pack(padx = 5, pady = 5)
			for i in self.useraccountnum:
				a = np.size(self.useraccountnum)
				showaccountnum = Button(self.frame1, text = i, bg = '#3D7878', fg = 'white', height = 120, width = 600, font = ('arial',40), command = lambda:self.notebook.select(self.frame2)).pack(padx = 5, pady = 5)
		createaccountBt = Button(self.frame1, text = "Create new account", bg = "#005757", fg = "white", height = 50, width = 230, font = ('arial', 20), command = lambda:self.createaccount(currentLogInUser)).pack(padx = 5, pady = 20)
		myconn.close()    
        
	def createaccount(self,currentLogInUser):
		self.root.destroy()
		Createaccount(currentLogInUser)             
        
	def accountinfo(self,currentLogInUser):
		f2greet = Label(self.frame2, text = "Account info", font = ('arial',30), bg = '#D1C8F2').pack(padx = 5, pady = 5) 

		scrollbar = tk.Scrollbar(self.frame2)               # 將 Frame 裡放入 Scrollbar
		scrollbar.pack(side='right', fill='y')        # 設定位置在右側，垂直填滿

		myconn = mysql.connector.connect(host="localhost", user="root", passwd="YourPassword", database="accountmanagement")
		cursor = myconn.cursor()
		for i in range(np.size(self.useraccountnum)):
			cursor.execute("select A.account_type, A.balance from Account A where A.account_num = %s",self.useraccountnum[i])
			info = cursor.fetchall()
			if info == None:
				Messagebox.showerror("Error","Invalid Username & Passwords")
			else:
				shownum = Label(self.frame2, text = self.useraccountnum[i], bg = '#D1C8F2', font = ('arial',20)).pack(padx = 5, pady = 5)
				table2 = ttk.Treeview(self.frame2, height=3)
				table2.pack()

				#define our column 
				table2['columns'] = ('account_type','balance')

				# format our column
				table2.column("#0", width = 0,  stretch = NO)
				table2.column("account_type",anchor = CENTER, width = 300)
				table2.column("balance",anchor = CENTER,width = 300)
        
				#Create Headings 
				table2.heading("#0", text = "", anchor = CENTER)
				table2.heading("account_type", text = "ACCOUNT TYPE", anchor = CENTER)
				table2.heading("balance", text = "BALANCE", anchor = CENTER)                
                           
				for j in range(np.shape(info)[0]):
					table2.insert(parent = '', index = 'end', iid = j, text = '', values = info[j])
				table2.pack()
				frameinf2 = Frame(self.frame2, bg = "#D1C8F2")
				frameinf2.pack()
				dotransact = Button(frameinf2, text = "Transact history", bg = '#6C3365', fg = 'white', height = 50, width = 160, font = ('arial',20), command = lambda i = i:self.transaction(self.useraccountnum[i])).pack(side = LEFT, padx = 5, pady = 5)
				trans = Button(frameinf2, text = "Transfer", bg = '#8F4586', fg = 'white', height = 50, width = 130, font = ('arial',25), command = lambda i = i:self.gototransfer(self.useraccountnum[i],currentLogInUser)).pack(side = LEFT, padx = 5, pady = 10)
		myconn.close()

		scrollbar.config(command=self.frame2.yview)    # 設定 scrollbar 綁定 text 的 yview
		self.frame2.pack()

  
	def gototransfer(self, accountnum,currentLogInUser):        
		self.root.destroy()
		Transferpage(accountnum,currentLogInUser)
        

	def transaction(self, account_num):
		for widget in self.frame3.winfo_children():
			widget.destroy()
		self.notebook.select(self.frame3)
		print(account_num)
		f3greet = Label(self.frame3, text = "Transaction Details:", font = ('arial',30), bg = '#E6E6F2').pack(padx = 5, pady = 5) 
		self.table = ttk.Treeview(self.frame3, height=5)
		self.table.pack()

        
		#define our column 
		self.table['columns'] = ('transaction_id', 'from_account', 'to_account', 'amount', 'trans_time', 'trans_date')

		# format our column
		self.table.column("#0", width=0,  stretch=NO)
		self.table.column("transaction_id",anchor=CENTER, width=100)
		self.table.column("from_account",anchor=CENTER,width=100)
		self.table.column("to_account",anchor=CENTER,width=100)
		self.table.column("amount",anchor=CENTER,width=100)
		self.table.column("trans_time",anchor=CENTER,width=100)
		self.table.column("trans_date",anchor=CENTER,width=100)
        
		#Create Headings 
		self.table.heading("#0",text="",anchor=CENTER)
		self.table.heading("transaction_id",text="Id",anchor=CENTER)
		self.table.heading("from_account",text="FROM",anchor=CENTER)
		self.table.heading("to_account",text="TO",anchor=CENTER)
		self.table.heading("amount",text="AMOUNT",anchor=CENTER)
		self.table.heading("trans_time",text="time",anchor=CENTER)
		self.table.heading("trans_date",text="date",anchor=CENTER)

		#Build the connection
		myconn = mysql.connector.connect(host="localhost", user="root", passwd="YourPassword", database="accountmanagement")
		cursor = myconn.cursor()
		cursor.execute("select T.transaction_id, L.from_account, L.to_account, T.amount, T.trans_time, T.trans_date from Account A, linkAccountTransaction L, Transaction T where account_num = %s and (A.account_id = L.from_account or A.account_id = L.to_account) and L.transaction_id = T.transaction_id ",account_num)
		detail = cursor.fetchall()

		#add data
		for i in range(np.shape(detail)[0]):
			self.table.insert(parent = '', index = 'end', iid = i, text = '', values = detail[i])
		self.table.pack()

		

		# self.tree.pack()


		myconn.close()
        
		frameinf3 = Frame(self.frame3, bg = '#7373B9', height = 300)     
		frameinf3.pack(side = BOTTOM,fill = BOTH, padx = 10, pady = 5)  

		self.getyear = StringVar()        
		self.getmonth = StringVar()        
		self.getday = StringVar()
		searchyearlb = Label(frameinf3, text = "year", bg = '#7373B9', fg = 'white', font = ('arail', 20)).pack(side = LEFT, padx = 5, pady = 5)
		searchyear = Entry(frameinf3, bg = '#E6E6F2', width = 15, textvariable = self.getyear).pack(side = LEFT, pady = 5)
		searchmonthlb = Label(frameinf3, text = "month", bg = '#7373B9', fg = 'white', font = ('arail', 20)).pack(side = LEFT, padx = 5, pady = 5)
		searchmonth = Entry(frameinf3, bg = '#E6E6F2', width = 15, textvariable = self.getmonth).pack(side = LEFT, pady = 5)
		searchdaylb = Label(frameinf3, text = "day", bg = '#7373B9', fg = 'white', font = ('arail', 20)).pack(side = LEFT, padx = 5, pady = 5)
		searchday = Entry(frameinf3, bg = '#E6E6F2', width = 15, textvariable = self.getday).pack(side = LEFT, pady = 5)        
		searchto = Button(frameinf3, bg = '#E6E6F2', text = "Search", command = lambda:self.search(account_num)).pack(side = RIGHT,padx = 5, pady = 5)
        
        
        
	def search(self, account_num):

		year = self.getyear.get()
		month = self.getmonth.get()
		date = self.getday.get()

		if (year == "" and month == "" and date == ""):
			self.transaction(account_num)
		else:
			myconn = mysql.connector.connect(host="localhost", user="root", passwd="YourPassword", database="accountmanagement")
			cursor = myconn.cursor()
			if(month == "" and date == ""):
				cursor.execute("select T.transaction_id, L.from_account, L.to_account, T.amount, T.trans_time, T.trans_date from Account A, linkAccountTransaction L, Transaction T where account_num = %s and (A.account_id = L.from_account or A.account_id = L.to_account) and L.transaction_id = T.transaction_id and YEAR(T.trans_date) = %s",(account_num[0], self.getyear.get()))
				row = cursor.fetchall()
				if row == None:
					Messagebox.showerror("Error","no record")
				else:
					for i in self.table.get_children():
						self.table.delete(i)
					for j in range(np.shape(row)[0]):
						self.table.insert(parent = '', index = 'end', iid = j, text = '', values = row[j])
					self.table.pack()
				myconn.close()
			elif(date == ""):
				cursor.execute("select T.transaction_id, L.from_account, L.to_account, T.amount, T.trans_time, T.trans_date from Account A, linkAccountTransaction L, Transaction T where account_num = %s and (A.account_id = L.from_account or A.account_id = L.to_account) and L.transaction_id = T.transaction_id and YEAR(T.trans_date) = %s and MONTH(T.trans_date) = %s",(account_num[0], self.getyear.get(),self.getmonth.get()))
				row = cursor.fetchall()
				if row == None:
					Messagebox.showerror("Error","no record")
				else:
					for i in self.table.get_children():
						self.table.delete(i)                        
					for j in range(np.shape(row)[0]):
						self.table.insert(parent = '', index = 'end', iid = j, text = '', values = row[j])
					self.table.pack()
				myconn.close()
			else:
				cursor.execute("select T.transaction_id, L.from_account, L.to_account, T.amount, T.trans_time, T.trans_date from Account A, linkAccountTransaction L, Transaction T where account_num = %s and (A.account_id = L.from_account or A.account_id = L.to_account) and L.transaction_id = T.transaction_id and YEAR(T.trans_date) = %s and MONTH(T.trans_date) = %s and DAY(T.trans_date) = %s",(account_num[0], self.getyear.get(),self.getmonth.get(),self.getday.get()))
				row = cursor.fetchall()
				if row == None:
					Messagebox.showerror("Error","no record")
				else:
					for i in self.table.get_children():
						self.table.delete(i)                        
					for j in range(np.shape(row)[0]):
						self.table.insert(parent = '', index = 'end', iid = j, text = '', values = row[j])
					self.table.pack()
				myconn.close()           
             
        
            
	def __init__(self, currentLogInUser):
		#Create the window
		self.root = Tk()
		self.root.title("Intelligent Know Your Customer")
		self.root.geometry('1100x700')

		#Set the area
		frameleft = Frame(self.root ,width = 250, height = 700, bg = '#A3D1D1')
		frameleft.pack(side = LEFT, fill = BOTH, padx = 8, pady = 10)      
		framemain = Frame(self.root ,width = 850, height = 710, bg = '#FFEEDD')
		framemain.pack()

		#Create database connection
		myconn = mysql.connector.connect(host="localhost", user="root", passwd="YourPassword", database="accountmanagement")
		now = datetime.now()
		time = now.strftime("%H:%M:%S")
		date = now.strftime("%Y-%m-%d")
		cursor = myconn.cursor()
		cursor.execute("select * from Customer where email=%s",(currentLogInUser,))
		row = cursor.fetchone()
		if row == None:
			Messagebox.showerror("Error","Invalid Username & Passwords")
		else:
			print("")

		update = "UPDATE Customer SET login_date=%s WHERE email=%s"
		val = (date, currentLogInUser)
		cursor.execute(update, val)
		update = "UPDATE Customer SET login_time=%s WHERE email=%s"
		val = (time, currentLogInUser)
		cursor.execute(update, val)
		myconn.commit()
		myconn.close()

		#Build a profile
		profile = PhotoImage(file = "./images/profile.gif")
		profileBt = Button(frameleft, image = profile).grid(row = 1, column = 1, columnspan = 2, padx = 20, pady = 20)

		username = Label(frameleft, text = row[1], bg = '#A3D1D1', font=('arial',30)).grid(row = 3, column = 1, rowspan = 3, columnspan = 2, pady = 5)
		email = Label(frameleft, text = currentLogInUser, bg = '#A3D1D1', font=('arial',20)).grid(row = 6, column = 1, rowspan = 3, columnspan = 2, pady = 10)

		logindatelbl = Label(frameleft, text = "Login date", bg = '#A3D1D1', font=('arial',20)).grid(row = 10, column = 1, pady = 10)
		logindatenum = Label(frameleft, text = date, bg = '#A3D1D1', font=('arial',20)).grid(row = 10, column = 2, pady = 10)
		logintimelbl = Label(frameleft, text = "Login time", bg = '#A3D1D1', font=('arial',20)).grid(row = 11, column = 1, pady = 10)
		logintimenum = Label(frameleft, text = time, bg = '#A3D1D1', font=('arial',20)).grid(row = 11, column = 2, pady = 10)
		dash = Label(frameleft, text = "---------------------------------", bg = '#A3D1D1', font=('arial',20)).grid(row = 12, column = 1, pady = 10, columnspan = 2)
		historylogin = Label(frameleft, text = "Last login time:", bg = '#A3D1D1', font=('arial',20)).grid(row = 13, column = 1, pady = 10, columnspan = 2)
		historylogindate = Label(frameleft, text = row[4], bg = '#A3D1D1', font=('arial',20)).grid(row = 14, column = 1, pady = 10)
		historylogintime = Label(frameleft, text = row[3], bg = '#A3D1D1', font=('arial',20)).grid(row = 14, column = 2, pady = 10)
		logoutBt = Button(frameleft, text = "LOG OUT", command = lambda:self.logout(currentLogInUser), bg = "#009393", fg = 'white', font = ('arial', 25), width = 150, height = 50).grid(row = 20, column = 1, columnspan = 2, padx = 10, pady = 10)

		#build the notebook
		self.notebook = ttk.Notebook(framemain)     
		self.frame1 = Frame(self.notebook, width = 860, height = 750, bg = '#D1E9E9')
		self.frame2 = Frame(self.notebook, width = 860, height = 750, bg = '#D1C8F2')
		self.frame3 = Frame(self.notebook, width = 860, height = 750, bg = '#E6E6F2')
		self.notebook.add(self.frame1, text = f'{"ACCOUNT": ^50s}')        
		self.notebook.add(self.frame2, text = f'{"ACCOUNT INFO": ^50s}') 
		self.notebook.add(self.frame3, text = f'{"TRANSACTION": ^50s}')
		self.notebook.pack(expand = 1, fill = BOTH)
		self.account(currentLogInUser)
		self.accountinfo(currentLogInUser)

		self.root.mainloop()

        
        
        
class Createaccount:
	def createBt(self, currentUser):
		if (self.accountid.get() == "" or self.accountnum.get() == "" or self.typeo.get() == ""):
			print(self.accountid.get())
			print(self.accountnum.get())
			print(self.typeo.get())
			Messagebox.showerror('Warning','All Fields Are Required.')
		elif((self.typeo.get() != 'Saving') and (self.typeo.get() != 'Current')):
			Messagebox.showerror('Warning','Type should be \'Saving\' or \'Current\'.')
		else:
			myconn = mysql.connector.connect(host="localhost", user="root", passwd="YourPassword", database="accountmanagement")
			cursor = myconn.cursor()
			cursor.execute("select * from Account where account_id = %s",(self.accountid.get(),))
			row = cursor.fetchone()
			if row != None:
				Messagebox.showerror("Warning","AccountID Already Exist, Please try with another ID")
			else:
				cursor.execute("insert into Account(account_id, account_num, account_type, balance) values (%s,%s,%s,%s)",(self.accountid.get(), self.accountnum.get(), self.typeo.get(),1000))
				cursor.execute("commit")
				cursor.execute("insert into linkCustomerAccount(account_id, email) values (%s,%s)",(self.accountid.get(), currentUser))
				cursor.execute("commit")
				Messagebox.showinfo("Success","Successfully create the account.")
				self.window.destroy()
				iKYC(currentUser)

	def goback(self, currentUser):
		self.window.destroy()
		iKYC(currentUser)                
                              
                
	def __init__(self, currentUser):
		print(currentUser)
		self.window = Tk()
		self.window.title("Create New Account")
		self.window.geometry('600x400')

		#Set the top
		frametop = Frame(self.window, bg = '#A3D1D1')
		frametop.pack(side = TOP, fill = BOTH)
		Label(frametop, text = 'Create a New Account', bg = '#A3D1D1', font=('arial',40)).pack()


		#Build a register interface
		createframe = Frame(self.window, bg = '#D8D8EB')
		createframe.pack(side = RIGHT, expand = 1)

		Label(createframe, text = "accountID" , bg = '#D8D8EB', font = ('arial', 20)).grid(row = 1, column = 1, padx = 5, pady = 5)
		Label(createframe, text = "(ex: 1,2,3,4,5)" , bg = '#D8D8EB', font = ('arial', 15)).grid(row = 2, column = 1)
		Label(createframe, text = "account number" , bg = '#D8D8EB', font = ('arial', 20)).grid(row = 3, column = 1, padx = 5, pady = 5)
		Label(createframe, text = "(xxx-xxxxxx-xxx)" , bg = '#D8D8EB', font = ('arial', 15)).grid(row = 4, column = 1)
		Label(createframe, text = "type", bg = '#D8D8EB', font = ('arial', 20)).grid(row = 5, column = 1, padx = 5, pady = 5)
		Label(createframe, text = "(Saving or Current)", bg = '#D8D8EB', font = ('arial', 15)).grid(row = 6, column = 1)

		self.accountid = StringVar()
		self.accountnum = StringVar()
		self.typeo = StringVar()
		accountid = Entry(createframe, textvariable = self.accountid).grid(row = 1, column = 2, padx = 5, pady = 5)
		accountnum = Entry(createframe, textvariable = self.accountnum).grid(row = 3, column = 2, padx = 5, pady = 5)
		typeo = Entry(createframe, textvariable = self.typeo).grid(row = 5, column = 2, padx = 5, pady = 5)

		createbutton = Button(createframe, text = "Create" , command = lambda:self.createBt(currentUser), bg = "#CCA3CC").grid(row = 7, column = 1, padx = 5, pady = 5)
		exitbutton = Button(createframe, text = "Goback" , command = lambda:self.goback(currentUser), bg = "#CCA3CC").grid(row = 7, column = 2, padx = 5, pady = 5)

		self.window.mainloop()  

        
        
        
class Transferpage:                          
	def __init__(self, accountnum, currentUser):        
		self.new = Tk()
		self.new.title("Transfer")
		self.new.geometry('360x230')
		self.new["bg"] = "#FF9224"
        
        
		transframe = Frame(self.new, bg = "#FFDCB9")
		transframe.pack(padx = 10, pady = 10)
        
		self.toaccount = StringVar()
		self.ammounto = StringVar()
		self.verify = StringVar()

		fromaccountlb = Label(transframe, text = "From", font = ('arial', 20), bg = "#FFDCB9").grid(row = 0, column = 0, padx = 5, pady = 5)       
		fromaccount = Label(transframe, text = accountnum, font = ('arial', 20), bg = "#FFDCB9").grid(row = 0, column = 1, padx = 5, pady = 5)         
		toaccountlb = Label(transframe, text = "To", font = ('arial', 20), bg = "#FFDCB9").grid(row = 1, column = 0, padx = 5, pady = 5)        
		toaccountet = Entry(transframe, textvariable = self.toaccount).grid(row = 1, column = 1, padx = 5, pady = 5)    
        
		ammountlb = Label(transframe, text = "Ammount", font = ('arial', 20), bg = "#FFDCB9").grid(row = 2, column = 0, padx = 5, pady = 5)       
		ammountet = Entry(transframe, textvariable = self.ammounto).grid(row = 2, column = 1, padx = 5, pady = 5)
        
		verifylb = Label(transframe, text = "passwords", font = ('arial', 20), bg = "#FFDCB9").grid(row = 3, column = 0, padx = 5, pady = 5)       
		verifyet = Entry(transframe, textvariable = self.verify).grid(row = 3, column = 1, padx = 5, pady = 5)
     
		transferbt = Button(transframe, text = "Confirm", font = ('arial', 20), command = lambda : self.confirmtransfer(accountnum, currentUser)).grid(row = 4, column = 0, padx = 5, pady = 5)
		gobackbt = Button(transframe, text = "Go Back", font = ('arial', 20), command = lambda : self.gobackto(currentUser)).grid(row = 4, column = 1, padx = 5, pady = 5)

        
	def gobackto(self, currentUser):
		self.new.destroy()                                
		iKYC(currentUser)        
         
        
	def confirmtransfer(self, accountnum, currentUser):
		if(self.toaccount.get() == "" or self.ammounto.get() == "" or self.verify.get() == ""):
			Messagebox.showerror("Warning","All Field Are Required.")
		else:        
			myconn = mysql.connector.connect(host="localhost", user="root", passwd="YourPassword", database="accountmanagement")
			now = datetime.now()
			time = now.strftime("%H:%M:%S")
			date = now.strftime("%Y-%m-%d")
			cursor = myconn.cursor()
			cursor.execute("select * from Account A, linkCustomerAccount L, Customer C where account_num = %s and C.passwords = %s and (A.account_id = L.account_id) and L.email = C.email",(accountnum[0], self.verify.get(),))
			pwd = cursor.fetchall()
			if pwd == []:
				Messagebox.showerror("Error","Wrong Password.")
			else:            
				cursor.execute("select * from Account where account_num = %s",(self.toaccount.get(),))
				row = cursor.fetchall()
				if row == []:
					Messagebox.showerror("Error","The receiptor doesn't Exist.")
				else:
					cursor.execute("select balance from Account where account_type = 'Current' and account_num = %s",(accountnum[0],))
					money = cursor.fetchall()
					if money[0][0] < int(self.ammounto.get()):
						Messagebox.showerror("Warning","Don't have enough money in Current account.")
					else:
						cursor.execute("select * from Transaction")
						ID = cursor.fetchall()                  
						cursor.execute("insert into Transaction(transaction_id, amount, trans_time, trans_date) values (%s,%s,%s,%s)",(len(ID)+1, self.ammounto.get(), time, date))
						cursor.execute("commit")

						cursor.execute("select account_id from Account where account_num = %s and account_type = 'Current'",(accountnum[0],))
						fromID = cursor.fetchall()                          
						cursor.execute("select account_id from Account where account_num = %s and account_type = 'Current'",(self.toaccount.get(),))
						toID = cursor.fetchall()                      
						cursor.execute("insert into linkAccountTransaction(transaction_id, from_account, to_account) values (%s,%s,%s)",(len(ID)+1, fromID[0][0], toID[0][0]))
						cursor.execute("commit")

						cursor.execute("UPDATE Account SET balance = %s WHERE account_num = %s and account_type = 'Current'",(str(money[0][0]-int(self.ammounto.get())), accountnum[0],))
						myconn.commit()
                                               
						cursor.execute("select balance from Account where account_type = 'Current' and account_num = %s",(self.toaccount.get(),))                        
						getmoney = cursor.fetchall() 
						print(getmoney)
						print(self.toaccount.get())
						print((self.toaccount.get(),))                                              
						cursor.execute("UPDATE Account SET balance = %s WHERE account_num = %s and account_type = 'Current'",(str(getmoney[0][0]+int(self.ammounto.get())), self.toaccount.get(),))
						myconn.commit()                                              
						myconn.close()
						self.new.destroy()                                
						iKYC(currentUser)
                        
                        
                        
                        
                        
Login()