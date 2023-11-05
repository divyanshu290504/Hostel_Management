# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from datetime import date

app = Flask(__name__)
app.secret_key = 'your secret key'
import re
def change_date_format(dt):
	return re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\3-\\2-\\1', dt)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		conn = mysql.connector.connect(
      host="localhost",
      user="root",
      database="hostel_db",
      password="mysql"
      )
		username = request.form['username']
		password = request.form['password']
		cur = conn.cursor()
		st = 'SELECT * FROM accounts WHERE username = \'{}\' AND password = \'{}\';'.format (username,password) 
		cur.execute(st)
		account = cur.fetchone()
		conn.commit()
		cur.close()
		conn.close()
		print(account)
		if account:
			session['loggedin'] = True
			session['id'] = account[0]
			session['username'] = account[1]
			if account[1][0] == 'a':
				msg = 'Logged in successfully as admin!'
				session['person']='admin'
				return render_template('admin.html',msg=msg)
			else:
				msg = 'Logged in successfully as hostelite!'
				session['person'] = 'hostelite'
				return render_template('student.html',msg=msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	
	print(request.form)
	if request.method == 'POST' and len(request.form) != 0:
		conn = mysql.connector.connect(
      host="localhost",
      user="root",
      database="hostel_db",
      password="mysql"
      )
		name = request.form['Name']
		Legal_ID = request.form['Legal_ID']
		Phone_No = request.form['Phone_No']
		SRN = request.form['SRN']
		DOB = change_date_format(request.form['DOB'])
		DOB = date(int(DOB[6:]),int(DOB[3:5]),int(DOB[0:2]))
		Hostel_Request_Status = '0'
		cur = conn.cursor()
		st = 'INSERT INTO hostelite(Name,Phone_No,SRN,DOB,Legal_ID,Hostel_Request_Status) VALUES(\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\');'.format (name,Phone_No,SRN,DOB,Legal_ID,Hostel_Request_Status) 
		cur.execute(st)
		House_Details = request.form['House_Details']
		City = request.form['City']
		State = request.form['State']
		Pincode = request.form['Pincode']
		st = 'SELECT Hostel_ID from hostelite where Legal_ID=\'{}\';'.format(Legal_ID)
		cur.execute(st)
		HostelID = cur.fetchone()[0]

		st = 'INSERT INTO hostelite_addr VALUES(\'{}\',\'{}\',\'{}\',\'{}\',{});'.format (HostelID,House_Details,State,City,Pincode) 
		cur.execute(st)
		name = request.form['PName']
		relation = request.form['PRelation']
		dob = change_date_format(request.form['PDOB'])
		dob = date(int(dob[6:]),int(dob[3:5]),int(dob[0:2]))
		job = request.form['PJob']
		Phone_No = request.form['PPhone_No']
		Legal_ID = request.form['PIdentification_No']

		st = 'INSERT INTO Parent VALUES(\'{}\',\'{}\',\'{}\',\'{}\',{},\'{}\');'.format (name,relation,dob,job,Phone_No,Legal_ID) 
		cur.execute(st)
		st = 'INSERT INTO HasParent_Guardian VALUES(\'{}\',\'{}\',\'{}\');'.format (HostelID,Legal_ID,relation) 
		cur.execute(st)
		name = request.form['LName']
		House_Details = request.form['LHouse_Details']
		City = request.form['LCity']
		State = request.form['LState']
		Pincode = request.form['LPincode']
		dob = change_date_format(request.form['LDOB'])
		dob = date(int(dob[6:]),int(dob[3:5]),int(dob[0:2]))
		job = request.form['LJob']
		gender = request.form['LGender']
		Phone_No = request.form['LPhone_No']
		Legal_ID = request.form['LIdentification_No']
		relation = request.form['LRelation']
		
		st = 'INSERT INTO Local_Guardian VALUES(\'{}\',\'{}\',\'{}\',\'{}\',{},\'{}\');'.format (name,Legal_ID,dob,job,Phone_No,gender) 
		cur.execute(st)
		st = 'INSERT INTO Has_LG VALUES(\'{}\',\'{}\',\'{}\');'.format(HostelID,Legal_ID,relation)
		cur.execute(st)
		st = 'INSERT INTO Local_Guardian_Addr VALUES(\'{}\',\'{}\',\'{}\',\'{}\',{});'.format (Legal_ID,House_Details,State,City,Pincode) 
		cur.execute(st)
		conn.commit()
		cur.close()
		conn.close()
		return render_template('home.html',msg = "Request Accepted Successfully")
	return render_template('register.html')

@app.route('/addParent', methods = ['GET','POST'])
def addParent():
	if request.method == 'POST' and len(request.form) != 0:
		conn = mysql.connector.connect(
      host="localhost",
      user="root",
      database="hostel_db",
      password="mysql"
      )
		name = request.form['PName']
		relation = request.form['PRelation']
		dob = change_date_format(request.form['PDOB'])
		dob = date(int(dob[6:]),int(dob[3:5]),int(dob[0:2]))
		job = request.form['PJob']
		Phone_No = request.form['PPhone_No']
		Legal_ID = request.form['PIdentification_No']
		cur = conn.cursor()
		st = 'INSERT INTO Parent VALUES(\'{}\',\'{}\',\'{}\',\'{}\',{},\'{}\');'.format (name,relation,dob,job,Phone_No,Legal_ID) 
		cur.execute(st)
		st = 'INSERT INTO HasParent_Guardian VALUES(\'{}\',\'{}\',\'{}\');'.format (session['username'][1:],Legal_ID,relation) 
		cur.execute(st)
		conn.commit()
		cur.close()
		conn.close()
		return render_template('student.html')

	return render_template('addParent.html')

@app.route('/viewRequests', methods = ['GET','POST'])
def viewRequests():
	db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql",
    database="hostel_db"
	)
	cursor = db.cursor()
	cursor.execute('SELECT Name FROM hostelite')
	data = cursor.fetchall()

	return render_template('viewRequests.html',data=data)

if __name__ == "__main__":
	app.run()
