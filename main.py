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

# home page 
@app.route('/')
def index():
    return render_template('index.html')


# login and register pages for admin , user , hospital
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
    if session['login'] :
        return redirect('/admin')
    if request.method == 'POST':
        userDetails = request.form
        username = userDetails['name']
        cur = mysql.connection.cursor()
        resultValue = cur.execute("SELECT * FROM admin WHERE name = %s", ([username]))
        if resultValue > 0:
            user = cur.fetchone()
            if userDetails['password'] == user['password']:
                session['login'] = True
                session['admin_Name'] = user['name']
                flash('Welcome ' + session['admin_Name'] +'! You have been successfully logged in', 'success')
            else:
                cur.close()
                flash('Password does not match', 'danger')
                return render_template('login_admin.html')
        else:
            cur.close()
            flash('User not found', 'danger')
            return render_template('login_admin.html')
        cur.close()
        return redirect('/admin')
    
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
                session['user_Name'] = user['name']
                flash('Welcome ' + session['user_Name'] +'! You have been successfully logged in', 'success')
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
                session['hospital_Name'] = user['name']
                flash('Welcome ' + session['hospital_Name'] +'! You have been successfully logged in', 'success')
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

# admin page 

@app.route('/admin/', methods=['GET', 'POST'])
def admin():
    
    return render_template('admin.html')

# pages for admin_addprice disease , equipmennts , medicine
@app.route('/admin_addprice_disease/', methods=['GET', 'POST'])
def admin_addprice_disease():
    if request.method == 'POST':
        userDetails = request.form
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO disease_gov(name,min_price,max_price,days_recover) "\
        "VALUES(%s,%s,%s,%s)",(userDetails['name'], userDetails['min_price'], userDetails['max_price'], userDetails['days_recover']))
        mysql.connection.commit()
        cur.close()
        flash('Data added to the database', 'success')
        return redirect('/admin')
    return render_template('admin_addprice_disease.html')

@app.route('/admin_addprice_equipment/', methods=['GET', 'POST'])
def admin_addprice_equipment():
    if request.method == 'POST':
        userDetails = request.form
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO equipment_gov(min_price,max_price,name) "\
        "VALUES(%s,%s,%s)",( userDetails['min_price'], userDetails['max_price'], userDetails['name']))
        mysql.connection.commit()
        cur.close()
        flash('Data added to the database', 'success')
        return redirect('/admin')
    return render_template('admin_addprice_equipment.html')

@app.route('/admin_addprice_medicine/', methods=['GET', 'POST'])
def admin_addprice_medicine():
    if request.method == 'POST':
        userDetails = request.form
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO medicine_gov(name,min_price,max_price) "\
        "VALUES(%s,%s,%s)",(userDetails['name'], userDetails['min_price'], userDetails['max_price']))
        mysql.connection.commit()
        cur.close()
        flash('Data added to the database', 'success')
        return redirect('/admin')
    return render_template('admin_addprice_medicine.html')


@app.route('/user_addreport/', methods=['GET', 'POST'])
def user_addreport():
    if request.method == 'POST':
        userDetails = request.form
        print(userDetails['date'])
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO complain(complain, name, date) "\
        "VALUES(%s,%s,%s)",(userDetails['complain'], userDetails['name'], userDetails['date']))
        mysql.connection.commit()
        cur.close()
        flash('Your Complaint Registered', 'success')
        return redirect('/admin_viewreport')
    return render_template('user_addreport.html')

@app.route('/admin_viewreport/', methods=['GET', 'POST'])
def admin_viewreport():
    
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM complain")
    if resultValue > 0:
        complains = cur.fetchall()
        cur.close()
        return render_template('admin_viewreport.html', complains=complains)
    cur.close()
    return render_template('admin_viewreport.html',compalins=None)
    

if __name__ == '__main__':
    app.run(debug=True, port=5001)