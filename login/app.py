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
		
		print(account)
		if account:
			session['loggedin'] = True
			session['id'] = account[0]
			session['username'] = account[1]
			if account[1][0] == 'a':
				msg = 'Logged in successfully as admin!'
				session['person']='admin'
				return redirect(url_for('admin'))
			else:
				msg = 'Logged in successfully as hostelite!'
				session['person'] = 'hostelite'
				cur.execute('SELECT name from hostelite where Hostel_ID = \'{}\''.format(account[1][1:]))
				session['name'] = cur.fetchone()[0]
				cur.close()
				conn.close()
				return render_template('student.html',msg=msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/admin')
def admin():
	notifications=dict()
	conn = mysql.connector.connect(host="localhost",user="root",database="hostel_db",password="mysql")
	cur = conn.cursor()
	cur.execute('SELECT * FROM notification WHERE users_concerned=\"a\";')
	notifications = cur.fetchall()
	return render_template('admin.html',notifications=notifications)

@app.route('/delete_notification/<id>')
def delete_notification(id):
	conn = mysql.connector.connect(host="localhost",user="root",database="hostel_db",password="mysql")
	cur = conn.cursor()
	st = 'DELETE FROM notification where id={};'.format(id)
	cur.execute(st)
	conn.commit()
	cur.close()
	return redirect(url_for('admin'))

@app.route('/student')
def student():
	return render_template('student.html')

@app.route('/leaveApplication')
def leave_application():
    return render_template('leave_application.html')

@app.route('/submit_leave', methods=['POST'])
def submit_leave():
	if request.method == 'POST':
		conn = mysql.connector.connect(host="localhost",user="root",database="hostel_db",password="mysql")
		reason = request.form['reason']
		place = request.form['place']
		arrival_datetime = request.form['arrival_datetime']
		leaving_datetime = request.form['leaving_datetime']
        
		hostel_ID = session.get('username')[1:]
        
		cursor = conn.cursor()
		insert_query = "INSERT INTO leave_request (Verification_Status, Reason, Place, Arrival_Datetime, Leaving_Datetime, Hostel_ID) VALUES (%s, %s, %s, %s, %s, %s)"
		data = (0, reason, place, arrival_datetime, leaving_datetime, hostel_ID)
		cursor.execute(insert_query, data)
		conn.commit()
        
        # Redirect to a success page or anywhere you want after submission
		return render_template('student.html',msg="Submitted Successfully")

    # Handle GET requests or errors
	return "Something went wrong."

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

		
		st = 'INSERT INTO HasParent_Guardian VALUES(\'{}\',\'{}\',\'{}\');'.format (HostelID,Legal_ID,relation) 
		cur.execute(st)
		st = 'INSERT INTO Parent VALUES(\'{}\',\'{}\',\'{}\',\'{}\',{},\'{}\');'.format (name,relation,dob,job,Phone_No,Legal_ID) 
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
		
		
		st = 'INSERT INTO Has_LG VALUES(\'{}\',\'{}\',\'{}\');'.format(HostelID,Legal_ID,relation)
		cur.execute(st)
		st = 'INSERT INTO Local_Guardian VALUES(\'{}\',\'{}\',\'{}\',\'{}\',{},\'{}\');'.format (name,Legal_ID,dob,job,Phone_No,gender) 
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
		st = 'INSERT INTO HasParent_Guardian VALUES(\'{}\',\'{}\',\'{}\');'.format (session['username'][1:],Legal_ID,relation) 
		cur.execute(st)
		st = 'INSERT INTO Parent VALUES(\'{}\',\'{}\',\'{}\',\'{}\',{},\'{}\');'.format (name,relation,dob,job,Phone_No,Legal_ID) 
		cur.execute(st)
		conn.commit()
		cur.close()
		conn.close()
		return render_template('student.html')

	return render_template('addParent.html')

@app.route('/viewLeaveRequests', methods = ['GET','POST'])
def viewLeaveRequests():
	db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql",
    database="hostel_db"
	)
	cursor = db.cursor()
	cursor.execute('SELECT Hostel_ID FROM leave_request where Verification_Status=0')
	data = cursor.fetchall()
	if len(data) != 0:
		cursor.execute('SELECT Name from hostelite where Hostel_ID=%s',data[0])
		data = cursor.fetchall()
	return render_template('viewLeaveRequests.html',data=data)

@app.route('/get_leave_details',methods=['POST'])
def get_leave_details():
	db = mysql.connector.connect(
	host="localhost",
    user="root",
    password="mysql",
    database="hostel_db"
	)
	name = request.form.get('name')
	cursor = db.cursor(buffered=True)
	cursor.execute('SELECT * from hostelite WHERE Name=%s',(name,))
	Hostel_ID = cursor.fetchone()
	cursor.execute('SELECT * from leave_request WHERE Hostel_ID=%s',(Hostel_ID[0],))
	details = cursor.fetchone()
	reason = details[1]
	place = details[2]
	arrival_datetime = details[3]
	leaving_datetime = details[4]
	cursor.close()
	details_html = """
    <div class="details">
        <h2>Details for {}</h2>
        <div class="details-columns">
            <div class="details-column">
                <p>Hostelite Name: {}</p>
				<p>Reason: {}</p>
                <p>Place: {}</p>
                <p>Arrival Datetime: {}</p>
				<p>Leaving Datetime: {}</p>
            </div>
        </div>
    </div>
    """.format(
        name,name,reason,place,arrival_datetime,leaving_datetime
    )
	return details_html

@app.route('/accept_leave_request', methods=['POST'])
def accept_leave_request():
	db = mysql.connector.connect(
		host="localhost",
		user="root",
		password="mysql",
		database="hostel_db"
	)
	name = request.form.get('name')
	cursor = db.cursor(buffered=True)
	cursor.execute('SELECT * from hostelite WHERE Name=%s',(name,))
	Hostel_ID = cursor.fetchone()
	cursor.execute('UPDATE leave_request SET Verification_Status = 1 WHERE Hostel_ID = %s', (Hostel_ID[0],))
	db.commit()
	cursor.close()
	return "Request accepted successfully" 


@app.route('/reject_leave_request', methods=['POST'])
def reject_leave_request():
	db = mysql.connector.connect(
		host="localhost",
		user="root",
		password="mysql",
		database="hostel_db"
	)
	name = request.form.get('name')
    
	cursor = db.cursor(buffered=True)
	cursor.execute('DELETE FROM leave_request WHERE Hostel_ID = %s', (name,))

	db.commit()
	cursor.close()
	return "Request rejected and entry deleted"
@app.route('/viewRequests', methods = ['GET','POST'])
def viewRequests():
	db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql",
    database="hostel_db"
	)
	cursor = db.cursor()
	cursor.execute('SELECT Name FROM hostelite where Hostel_Request_Status=\'0\'')
	data = cursor.fetchall()

	return render_template('viewRequests.html',data=data)



@app.route('/get_details', methods=['POST'])
def get_details():
	db = mysql.connector.connect(
	host="localhost",
    user="root",
    password="mysql",
    database="hostel_db"
	)
	name = request.form.get('name')
	
    # Fetch data from the hostelite table
	cursor = db.cursor(buffered=True)
	cursor.execute('SELECT * FROM hostelite WHERE Name = %s', (name,))
	hostelite_data = cursor.fetchone()

    # Fetch data from the hostelite_addr table
	cursor.execute('SELECT * FROM hostelite_addr WHERE Hostelite_ID = %s', (hostelite_data[0],))
	hostelite_addr_data = cursor.fetchone()

    # Fetch data from the HasParent_Guardian table
	cursor.execute('SELECT * FROM HasParent_Guardian WHERE Hostelite_ID = %s', (hostelite_data[0],))
	has_parent_guardian_data = cursor.fetchone()

    # Fetch data from the Parent table
	cursor.execute('SELECT * FROM Parent WHERE Identification_No = %s', (has_parent_guardian_data[1],))
	parent_data = cursor.fetchone()

    # Fetch data from the Has_LG table
	cursor.execute('SELECT * FROM Has_LG WHERE Hostel_ID = %s', (hostelite_data[0],))
	has_lg_data = cursor.fetchone()

    # Fetch data from the Local_Guardian table
	cursor.execute('SELECT * FROM Local_Guardian WHERE Identification_No = %s', (has_lg_data[1],))
	local_guardian_data = cursor.fetchone()

    # Fetch data from the Local_Guardian_Addr table
	cursor.execute('SELECT * FROM Local_Guardian_Addr WHERE LG_ID = %s', (has_lg_data[1],))
	local_guardian_addr_data = cursor.fetchone()

	cursor.close()

    # Format the details as HTML with CSS classes
	details_html = """
    <div class="details">
        <h2>Details for {}</h2>
        <div class="details-columns">
            <div class="details-column">
                <p>Hostelite Name: {}</p>
                <p>Hostelite Phone: {}</p>
                <p>SRN: {}</p>
                <!-- Add more hostelite details here -->
            </div>
            <div class="details-column">
                <h3>Address Details</h3>
                <p>House Details: {}</p>
                <p>City: {}</p>
                <p>State: {}</p>
                <p>Pincode: {}</p>
                <!-- Add more address details here -->
            </div>
        </div>
        <div class="details-columns">
            <div class="details-column">
                <p>Parent Name: {}</p>
				<p>Relation: {}</p>
				<p>Job: {}</p>
				<p>Phone number: {}</p>
                <!-- Add more parent details here -->
            </div>
            <div class="details-column">
                <p>Local Guardian Name: {}</p>
				<p>Relation:{}</p>
                <p>House Details: {}</p>
                <p>City: {}</p>
                <p>State: {}</p>
                <p>Pincode: {}</p>
                <!-- Add more local guardian details here -->
            </div>
        </div>
    </div>
    """.format(
        name,
        hostelite_data[1], hostelite_data[2], hostelite_data[3], hostelite_addr_data[1], hostelite_addr_data[3], hostelite_addr_data[2], hostelite_addr_data[4],
        parent_data[0],parent_data[1],parent_data[3],parent_data[4],
        local_guardian_data[0], has_lg_data[2],local_guardian_addr_data[1], local_guardian_addr_data[3], local_guardian_addr_data[2], local_guardian_addr_data[4]
    )
	return details_html

@app.route('/accept_request', methods=['POST'])
def accept_request():
	db = mysql.connector.connect(
		host="localhost",
		user="root",
		password="mysql",
		database="hostel_db"
	)
	name = request.form.get('name')
	print(name)
    # Fetch data from the hostelite table
	cursor = db.cursor(buffered=True)
	cursor.execute('UPDATE hostelite SET Hostel_Request_Status = \'1\' WHERE Name = %s', (name,))
	cursor.execute('SELECT Hostel_ID,SRN from Hostelite WHERE Name=%s and Hostel_Request_Status = \'1\'',(name,))
	id = cursor.fetchone()
	cursor.execute('INSERT INTO accounts VALUES(NULL,\'{}\',\'{}\',\'{}\')'.format('h'+str(id[0]),'h'+str(id[0]),str(id[1])+'@pesu.pes.edu'))
	db.commit()
	cursor.close()

	return "Request accepted successfully"  # You can customize this response message

@app.route('/search_details',methods=["GET","POST"])
def search_details():
	name = request.form.get('name')
	db = mysql.connector.connect(
		host="localhost",
		user="root",
		password="mysql",
		database="hostel_db"
	)
	cur = db.cursor(buffered=True)
	print(name)
	cur.execute("SELECT Name FROM HOSTELITE WHERE NAME LIKE %s", ('%' + name + '%',))
	data = cur.fetchall()
	print(data)
	return render_template('searchdetails.html',data= data)


@app.route('/reject_request', methods=['POST'])
def reject_request():
	db = mysql.connector.connect(
		host="localhost",
		user="root",
		password="mysql",
		database="hostel_db"
	)
	name = request.form.get('name')
	print(name)
    # Fetch data from the hostelite table
	cursor = db.cursor(buffered=True)
	cursor.execute('DELETE FROM hostelite WHERE Name = %s', (name,))

	db.commit()
	cursor.close()
	return "Request rejected and entry deleted"

if __name__ == "__main__":
	app.run(debug=True)
