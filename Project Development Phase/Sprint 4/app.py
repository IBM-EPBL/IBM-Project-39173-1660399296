from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail 
import re
from twilio.rest import Client

app = Flask(__name__)

hostname = '98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud'
uid = 'jqj93360'
pwd = 'FljjHGlh2Y8TAce9'
driver = "{IBM DB2 ODBC DRIVER}"
db_name = 'bludb'
port = '30875'
protocol = 'TCPIP'
cert = "DigiCertGlobalRootCA.crt"
dsn = (
    "DATABASE ={0};"
    "HOSTNAME ={1};"
    "PORT ={2};"
    "UID ={3};"
    "SECURITY=SSL;"
    "PROTOCOL={4};"
    "PWD ={6};"
).format(db_name, hostname, port, uid, protocol, cert, pwd)
connection = ibm_db.connect(dsn, "", "")
print()
# query = "SELECT username FROM USER1 WHERE username=?"
# stmt = ibm_db.prepare(connection, query)
# ibm_db.bind_param(stmt, 1, username)
# ibm_db.execute(stmt)
# username = ibm_db.fetch_assoc(stmt)
# print(username)
app.secret_key = 'a'



@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = " "
    if request.method == 'POST':
        username = request.form['username']
        email_id = request.form['email_id']
        phone_no = request.form['phone_no']
       
        blood_grp = request.form['blood_grp']
        gender= request.form['gender']
        address= request.form['address']
        dob = request.form['dob']
        weight= request.form['weight']
        password = request.form['password']
        query = "SELECT * FROM USER1 WHERE username=?;"
        stmt = ibm_db.prepare(connection, query)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        if (account):

            msg = "Account already exists!"
            return render_template('register.html', msg=msg)
        #elif not re.match(r'[^@]+@[^@]+\.[^@]+', email_id):
            # msg = "Invalid email addres"
        #elif not re.match(r'[A-Za-z0-9+', username):
           # msg = "Name must contain only characters and numbers"
        else:
            query = "INSERT INTO USER1 values(?,?,?,?,?,?,?,?,?)"
            stmt = ibm_db.prepare(connection, query)
            ibm_db.bind_param(stmt, 1, username)
            ibm_db.bind_param(stmt, 2, email_id)
            ibm_db.bind_param(stmt, 3, phone_no)
            ibm_db.bind_param(stmt, 4, password)
            ibm_db.bind_param(stmt, 5, blood_grp)
            ibm_db.bind_param(stmt, 6, gender)
            ibm_db.bind_param(stmt, 7, address)
            ibm_db.bind_param(stmt, 8, dob)
            ibm_db.bind_param(stmt, 9, weight)
            ibm_db.execute(stmt)
            msg = 'You have successfully Logged In!!'
            return render_template('login.html', msg=msg)
    else:
        msg = 'PLEASE FILL OUT OF THE FORM'
        return render_template('register.html', msg=msg)

@app.route('/register2', methods=['GET', 'POST'])
def register2():
    msg = " "
    if request.method == 'POST':
        username = request.form['username']
        email_id = request.form['email_id']
        phone_no = request.form['phone_no']
       
        blood_grp = request.form['blood_grp']
        gender= request.form['gender']
        address= request.form['address']
        dob = request.form['dob']
        weight= request.form['weight']
        password = request.form['password']
        query = "SELECT * FROM USER2 WHERE username=?;"
        stmt = ibm_db.prepare(connection, query)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        if (account):

            msg = "Account already exists!"
            return render_template('register2.html', msg=msg)
        #elif not re.match(r'[^@]+@[^@]+\.[^@]+', email_id):
            # msg = "Invalid email addres"
        #elif not re.match(r'[A-Za-z0-9+', username):
           # msg = "Name must contain only characters and numbers"
        else:
            query = "INSERT INTO USER2 values(?,?,?,?,?,?,?,?,?)"
            stmt = ibm_db.prepare(connection, query)
            ibm_db.bind_param(stmt, 1, username)
            ibm_db.bind_param(stmt, 2, email_id)
            ibm_db.bind_param(stmt, 3, phone_no)
            ibm_db.bind_param(stmt, 4, password)
            ibm_db.bind_param(stmt, 5, blood_grp)
            ibm_db.bind_param(stmt, 6, gender)
            ibm_db.bind_param(stmt, 7, address)
            ibm_db.bind_param(stmt, 8, dob)
            ibm_db.bind_param(stmt, 9, weight)
            ibm_db.execute(stmt)
            msg = 'You have successfully Logged In!!'
            return render_template('login2.html', msg=msg)
    else:
        msg = 'PLEASE FILL OUT OF THE FORM'
        return render_template('register2.html', msg=msg)


@app.route("/login",methods=['GET','POST'])
def login():
	if request.method=="POST":
		username=request.form['username1']
		password=request.form['password1']
		query="select * from USER1 where username=? and password=?;"
		stmt=ibm_db.prepare(connection, query)
		ibm_db.bind_param(stmt, 1, username)
		ibm_db.bind_param(stmt, 2, password)
		ibm_db.execute(stmt)
		data=ibm_db.fetch_assoc(stmt)
		if data:
			session['loggedin']=True
			msg='Login Successfully'
			return redirect(url_for('view2'))
		
		else:
			msg='Incorrect Username or Password'
	return render_template("login.html")

@app.route('/loginadmin', methods=['GET', 'POST'])
def loginadmin():
    global userid
    msg = ' '
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        query = "select * from admin where username=? and password=?"
        stmt = ibm_db.prepare(connection, query)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['Loggedin'] = True
            session['id'] = account['USERNAME']
            session['username'] = account['USERNAME']
            msg = 'Logged in Successfully'
            return render_template('admin.html', msg=msg, username=str.upper(username))
        else:
            msg = 'Incorrect Username or Password'
            return render_template('loginadmin.html')
    else:
        msg = 'PLEASE FILL OUT OF THE FORM'
        return render_template('loginadmin.html', msg=msg)

@app.route('/login2', methods=['GET', 'POST'])
def login2():
    global userid
    msg = ' '
    if request.method == "POST":
        username = request.form['username2']
        password = request.form['password2']
        query = "select * from user2 where username=? and password=?"
        stmt = ibm_db.prepare(connection, query)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['Loggedin'] = True
            session['id'] = account['USERNAME']
            session['username'] = account['USERNAME']
            msg = 'Logged in Successfully'
            return redirect(url_for('view'))
        else:
            msg = 'Incorrect Username or Password'
            return render_template('view.html', msg=msg)
    else:
        msg = 'PLEASE FILL OUT OF THE FORM'
        return render_template('login2.html', msg=msg)



@app.route('/view', methods=['GET', 'POST'])
def view():
   
  query = "SELECT * FROM USER1"
  stmt = ibm_db.prepare(connection, query)
  ibm_db.execute(stmt)
  data=[]
  tuple = ibm_db.fetch_tuple(stmt)
  while tuple!=False:
        data.append(tuple)
        tuple=ibm_db.fetch_tuple(stmt)
  return render_template("view.html",data=data) 
  

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template("admin.html")


@app.route('/view2', methods=['GET', 'POST'])
def view2():
   
  query = "SELECT * FROM USER2"
  stmt = ibm_db.prepare(connection, query)
  ibm_db.execute(stmt)
  data=[]
  tuple = ibm_db.fetch_tuple(stmt)
  while tuple!=False:
        data.append(tuple)
        tuple=ibm_db.fetch_tuple(stmt)
  return render_template("view2.html",data=data) 
  



@app.route("/send",methods=['GET','POST'])
def send():
	if request.method=="POST":
		id=request.form['send']

		query="select email_id from user1"
		
		stmt = ibm_db.prepare(connection, query)
		
		ibm_db.execute(stmt)
		data = ibm_db.fetch_assoc(stmt)
		print(data) 
		message = Mail(from_email='sabrishdeepak2512@gmail.com',to_emails=data['EMAIL_ID'],subject='Sending with Twilio SendGrid is Fun',html_content='<strong>and easy to do anywhere, even with Python</strong>')
		try:
			sg = SendGridAPIClient('xx')
			response = sg.send(message)
			print(response.status_code)
			print(response.body)
			print(response.headers)
		except Exception as e:
			print(e)
	return redirect('/view')
		
@app.route("/")                                       
@app.route('/', methods=['GET', 'POST'])
def welcome():
    return render_template('welcome.html')

if __name__ == "__main__":
    app.run(debug=True)
    app.run(host='0.0.0.0')