from flask import Flask, request, session,redirect, url_for, render_template
from flaskext.mysql import MySQL
import pymysql
import re

from werkzeug.security import generate_password_hash,check_password_hash
from email.message import EmailMessage
import smtplib


app = Flask(__name__,template_folder='../templates', static_folder='../static', static_url_path='')


mysql = MySQL()


app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'bliink'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
app.config['SECRET_KEY']='DevRuth'
conn = mysql.connect()
cursor = conn.cursor(pymysql.cursors.DictCursor)
#cursor.execute("CREATE TABLE offline (id INT  AUTO_INCREMENT PRIMARY KEY,department VARCHAR(1000),year VARCHAR(1000),location VARCHAR(1000),shelf VARCHAR (1000))");

@app.route ('/')
def home():
    if 'loggedin' in session:

        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))
@app.route('/register', methods=['GET', 'POST'])
def register():

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:

        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']


        hashed_pw = generate_password_hash(request.form['password'])

        cursor.execute('SELECT * FROM project WHERE username = %s', (username))
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%&])',password):

            msg='Password must contain one uppercase and lowercase a special character and a number!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:

            cursor.execute('INSERT INTO project VALUES (%s,%s, %s, %s, %s)', (None,fullname, username, email, hashed_pw))
            conn.commit()

            msg = 'You have successfully registered!'

            return redirect(url_for('login'))
    elif request.method == 'POST':

        msg = 'Please fill out the form!'

    return render_template('register.html', msg=msg)
@app.route('/offline' ,methods=['GET', 'POST'])
def offline():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST' and 'department' in request.form and 'year' in request.form and 'location' in request.form and 'shelf' in request.form:


        department = request.form['department']
        print(department)
        year = request.form['year']
        print(year)
        location = request.form['location']
        print(location)
        shelf= request.form['shelf']
        print(shelf)
        cursor.execute('INSERT INTO offline VALUES (%s,%s,%s,%s,%s)',(None,department,year,location,shelf))
        conn.commit()
        return redirect(url_for('off'))




    return render_template('off.html')
@app.route('/off')
def off():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM offline')
    employees=cursor.fetchall()
    return render_template('offline.html',employees=employees)



@app.route('/employee', methods=['GET', 'POST'])
def employee():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'department' in request.form and 'role' in request.form and 'salary' in request.form and 'email' in request.form and 'number' in request.form:

        fullname = request.form['name']
        department = request.form['department']
        role= request.form['role']
        salary =request.form['salary']
        number =request.form['number']
        email = request.form['email']


        cursor.execute('SELECT * FROM employee WHERE email = %s', (email))
        account = cursor.fetchone()

        if account:
            msg = 'email already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'

            msg = 'Password must contain one uppercase and lowercase a special character and a number!'
        elif not re.match(r'[A-Za-z0-9]+', fullname):
            msg = 'Username must contain only characters and numbers!'
        elif not fullname or not email:
           msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO employee VALUES (%s,%s, %s, %s, %s,%s,%s)',(None, fullname, department,role,salary, email, number))
            n=conn.commit()
            print(n)


            msg = 'You have successfully registered!'

            return redirect(url_for('all'))
    elif request.method == 'POST':

        msg = 'Please fill out the form!'
    return render_template('employee.html',msg=msg)
@app.route('/all')
def all():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM employee ')
    employees=cursor.fetchall()

    return render_template('all.html',employees=employees)
@app.route('/finance')
def finance():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM employee WHERE department =%s',('Finance'))
    employees=cursor.fetchall()

    return render_template('finance.html',employees=employees)
@app.route('/it')
def it():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM employee WHERE department =%s',('IT'))
    employees=cursor.fetchall()

    return render_template('all.html',employees=employees)
@app.route('/hr')
def hr():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM employee WHERE department =%s',('Human resource'))
    employees=cursor.fetchall()

    return render_template('hr.html',employees=employees)
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():


    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form :
        # Create variables for easy access
        username = request.form['username']
        passwor = request.form['password']

        cursor.execute('SELECT * FROM project WHERE username = %s ', (username))
        account = cursor.fetchone()
        print(account)
        if account:


            h=check_password_hash(account['password'],passwor)
            if h==True:
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                return redirect(url_for('home'))

            else:



             msg = 'Incorrect username/password!'

        else:

            usernam=request.form['username']
            passw=request.form['password']
            if usernam =='Admin' and passw =='1234Aa@':
                session['admin'] = True
                session['username'] = usernam
                session['password'] = passw


                return redirect(url_for('admin'))
            else:
                msg='invalid credentials'

    return render_template('login.html', msg=msg)


@app.route('/profile')
def profile():

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)


    if 'loggedin' in session:

        cursor.execute('SELECT * FROM project WHERE id = %s', [session['id']])
        account = cursor.fetchone()

        return render_template('profile.html', account=account)

    return redirect(url_for('login'))
@app.route('/logout')
def logout():

   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)

   return redirect(url_for('login'))
@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():


    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)


    msg = ''

    def email_alert(subject, body, to):
        msg = EmailMessage()
        msg.set_content(body)
        msg['subject'] = subject
        msg['to'] = to


        user="blinkcustomercare777@gmail.com"
        msg['from'] = user

        password ="sfemzfrnumkzrvap"

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(user, password)
        server.send_message(msg)
        server.quit()
    if request.method == 'POST' and 'email' in request.form:

        email = request.form['email']


        cursor.execute('SELECT * FROM project WHERE email = %s ', (email))
        acc=cursor.fetchone()
        print(acc)
        if acc:
            session ['change'] =True
            session['id'] = acc['id']
            session['email'] =acc ['email']
            session['password']=acc ['password']
            email_alert("Password reset request",f'''To reset your password,visit the link below:{url_for('reset_token',_external=True)} If you did not make this request then please ignore this email and nothing will change"''',"grafana777@gmail.com")






            msg='An email has been sent with instructions to reset your password'
            return render_template('basic.html')

        else:
            msg = 'Please enter a valid email'

    return render_template('forgot.html', msg=msg)


@app.route("/reset_passwords", methods=['GET', 'POST'])
def reset_token():

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    msg = ''




    if request.method == 'POST' and 'password' in request.form :

        password = request.form['password']
        if not re.match(r'(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%&])', password):

          msg = 'Password must contain one uppercase and lowercase a special character and a number!'
        else:

         hashed_pw = generate_password_hash(request.form['password'])


         id= session ['id']

         if 'change' in session:


           cursor.execute('UPDATE project SET password =%s WHERE id =%s',(hashed_pw,id))
           conn.commit()


           msg = 'You have successfully changed your password!'
           return redirect(url_for('login'))
         else:
            msg='try again'


    return render_template('reset.html', msg=msg,title='Reset Password')




if __name__ == '__main__':

    app.run(debug=True)



