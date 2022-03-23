import flask
from flask import Flask, render_template, request, redirect, session, flash
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
from flask_ckeditor import CKEditor
import yaml

app = Flask(__name__)
Bootstrap(app)
ckeditor = CKEditor(app)

db = yaml.load(open('db.yaml'), yaml.Loader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

app.config['SECRET_KEY'] = 'secret'

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/register_admin/', methods=['GET', 'POST'])
def register_admin():
    if request.method == 'POST':
        userDetails = request.form
        if userDetails['password'] != userDetails['confirm_password']:
            flash('Passwords do not match! Try again.', 'danger')
            return render_template('register_admin.html')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO admin(name,password) "\
        "VALUES(%s,%s)",(userDetails['name'], userDetails['password']))
        mysql.connection.commit()
        cur.close()
        flash('Registration successful! Please login.', 'success')
        return redirect('/login_admin')
    return render_template('register_admin.html')

@app.route('/login_admin/', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        userDetails = request.form
        username = userDetails['name']
        cur = mysql.connection.cursor()
        resultValue = cur.execute("SELECT * FROM admin WHERE name = %s", ([username]))
        if resultValue > 0:
            user = cur.fetchone()
            if userDetails['password'] == user['password']:
                session['login'] = True
                session['Name'] = user['name']
                flash('Welcome ' + session['Name'] +'! You have been successfully logged in', 'success')
            else:
                cur.close()
                flash('Password does not match', 'danger')
                return render_template('login_admin.html')
        else:
            cur.close()
            flash('User not found', 'danger')
            return render_template('login_admin.html')
        cur.close()
        return redirect('/')
    return render_template('login_admin.html')

@app.route('/register_user/', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        userDetails = request.form
        if userDetails['password'] != userDetails['confirm_password']:
            flash('Passwords do not match! Try again.', 'danger')
            return render_template('register_user.html')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user(name,password) "\
        "VALUES(%s,%s)",(userDetails['name'], userDetails['password']))
        mysql.connection.commit()
        cur.close()
        flash('Registration successful! Please login.', 'success')
        return redirect('/login_user')
    return render_template('register_user.html')

@app.route('/login_user/', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        userDetails = request.form
        username = userDetails['name']
        cur = mysql.connection.cursor()
        resultValue = cur.execute("SELECT * FROM user WHERE name = %s", ([username]))
        if resultValue > 0:
            user = cur.fetchone()
            if userDetails['password'] == user['password']:
                session['login'] = True
                session['Name'] = user['name']
                flash('Welcome ' + session['Name'] +'! You have been successfully logged in', 'success')
            else:
                cur.close()
                flash('Password does not match', 'danger')
                return render_template('login_user.html')
        else:
            cur.close()
            flash('User not found', 'danger')
            return render_template('login_user.html')
        cur.close()
        return redirect('/')
    return render_template('login_user.html')


@app.route('/register_hospital/', methods=['GET', 'POST'])
def register_hospital():
    if request.method == 'POST':
        userDetails = request.form
        if userDetails['password'] != userDetails['confirm_password']:
            flash('Passwords do not match! Try again.', 'danger')
            return render_template('register_hospital.html')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO hospital(name,password,licence_no) "\
        "VALUES(%s,%s,%s)",(userDetails['name'], userDetails['password'],userDetails['licence_no']))
        mysql.connection.commit()
        cur.close()
        flash('Registration successful! Please login.', 'success')
        return redirect('/login_hospital')
    return render_template('register_hospital.html')

@app.route('/login_hospital/', methods=['GET', 'POST'])
def login_hospital():
    if request.method == 'POST':
        userDetails = request.form
        username = userDetails['name']
        cur = mysql.connection.cursor()
        resultValue = cur.execute("SELECT * FROM hospital WHERE name = %s", ([username]))
        if resultValue > 0:
            user = cur.fetchone()
            if userDetails['password'] == user['password']:
                session['login'] = True
                session['Name'] = user['name']
                flash('Welcome ' + session['Name'] +'! You have been successfully logged in', 'success')
            else:
                cur.close()
                flash('Password does not match', 'danger')
                return render_template('login_hospital.html')
        else:
            cur.close()
            flash('User not found', 'danger')
            return render_template('login_hospital.html')
        cur.close()
        return redirect('/')
    return render_template('login_hospital.html')



if __name__ == '__main__':
    app.run(debug=True, port=5001)