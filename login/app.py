# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your secret key'
conn = mysql.connector.connect(
      host="localhost",
      user="root",
      database="dbms_project",
      password="mysql"
      )


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cur = conn.cursor()
		st = 'SELECT * FROM accounts WHERE username = \'{}\' AND password = \'{}\';'.format (username,password) 
		cur.execute(st)
		account = cur.fetchone()
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
	return render_template('register.html')

if __name__ == "__main__":
	app.run()
