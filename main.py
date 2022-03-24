from sre_constants import SUCCESS
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

def is_logged_in(**kwargs):
    try: 
        #check if defined
        session['login']
    except Exception:
        session['login'] = False
    try: 
        #check if defined
        session['type']
    except Exception:
        session['type'] = 'xyz'

        
    if session['login']  :
        for type in kwargs['type']:
            if session['type'] == type:
                if 'if_logged_in_link' in kwargs :
                    return redirect(kwargs['if_logged_in_link'])
                    
                else :
                    
                    return True
            
        flash("You dont have permissions" , 'danger') 
        print(kwargs['type'] , "this type sent",session['type']) 
              
        return redirect('/')         
    elif 'if_not_logged_in_link' in kwargs:
        
        return redirect(kwargs['if_not_logged_in_link'])
        
    else:
        
        return True


# home page 
@app.route('/')
def index():
    # session['login'] = False
    return render_template('index.html')

@app.route('/logout')
def logout():
    session['login'] = False
    flash('Logged Out Successfully', 'success')
    return redirect('/')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')



#user as per primary/ unique key- a part of route
##take input as pincode
#check 100 ki range mein +-10
@app.route('/user/',  methods=['GET', 'POST'])
def explore_hospitals_nearby():
    redirect_to = is_logged_in(type = ['user'], if_not_logged_in_link = '/login_user/')
    if  redirect_to != True:
        return redirect_to
    return render_template('user.html')
    pass
#     if request.method == 'POST':
#             pincode = request.form
            
#             if hospitalDetails == None:
#                   flash('Please Enter valid hospital details.')
#                   return redirect('back')
#             cur = mysql.connection.cursor()
#             cur.execute("SELECT * FROM hospital WHERE pincode=' '") # check if this needs to have %s
#             cur.close()

# admin page 

@app.route('/admin/', methods=['GET', 'POST'])
def admin():
    redirect_to = is_logged_in(type = ['admin'] ,if_not_logged_in_link = '/login_admin/')
    if  redirect_to != True:
        return redirect_to
    return render_template('admin.html')


@app.route('/hospital/', methods=['GET','POST'])
def hospital_main_page():
    redirect_to = is_logged_in(type = ['hospital'], if_not_logged_in_link = '/login_hospital/')
    if  redirect_to != True:
        return redirect_to
    return render_template('hospital.html')
    pass

    
# login and register pages for admin , user , hospital
@app.route('/register_admin/', methods=['GET', 'POST'])
def register_admin():
    redirect_to = is_logged_in(type = ['user' , 'admin' , 'hospital'] ,if_logged_in_link = '/admin/')
    if  redirect_to != True:
        return redirect_to
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
    redirect_to = is_logged_in(type = ['user' , 'admin' , 'hospital'] ,if_logged_in_link = '/admin/')
    if  redirect_to != True:
        return redirect_to
    if request.method == 'POST':
        userDetails = request.form
        username = userDetails['name']
        cur = mysql.connection.cursor()
        resultValue = cur.execute("SELECT * FROM admin WHERE name = %s", ([username]))
        if resultValue > 0:
            user = cur.fetchone()
            if userDetails['password'] == user['password']:
                session['login'] = True
                session['type'] = 'admin'
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
        return redirect('/admin')
    
    return render_template('login_admin.html')

@app.route('/register_user/', methods=['GET', 'POST'])
def register_user():
    redirect_to = is_logged_in(type = ['user' , 'admin' , 'hospital'],if_logged_in_link = '/user/')
    if  redirect_to != True:
        return redirect_to
    if request.method == 'POST':
        userDetails = request.form
        if userDetails['password'] != userDetails['confirm_password']:
            flash('Passwords do not match! Try again.', 'danger')
            return render_template('register_user.html')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user(name,password,adhar_number) "\
        #aaded primary key- aadhar number
        "VALUES(%s,%s,%s)",(userDetails['name'], userDetails['password'], userDetails['adhar_number']))
        mysql.connection.commit()
        cur.close()
        flash('Registration successful! Please login.', 'success')
        return redirect('/login_user')
    return render_template('register_user.html')

@app.route('/login_user/', methods=['GET', 'POST'])
def login_user():
    redirect_to = is_logged_in(type = ['user' , 'admin' , 'hospital'],if_logged_in_link = '/user/')
    if  redirect_to != True:
        return redirect_to
    if request.method == 'POST':
        userDetails = request.form
        username = userDetails['name']
        cur = mysql.connection.cursor()
        resultValue = cur.execute("SELECT * FROM user WHERE name = %s", ([username]))
        if resultValue > 0:
            user = cur.fetchone()
            if userDetails['password'] == user['password']:
                session['login'] = True
                session['type'] = 'user'
                session['Name']= user['name']
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
        return redirect('/user')
    return render_template('login_user.html')


@app.route('/register_hospital/', methods=['GET', 'POST'])
def register_hospital():
    redirect_to = is_logged_in(type = ['user' , 'admin' , 'hospital'],if_logged_in_link = '/hospital/')
    if  redirect_to != True:
        return redirect_to
    if request.method == 'POST':
        userDetails = request.form
        if userDetails['password'] != userDetails['confirm_password']:
            flash('Passwords do not match! Try again.', 'danger')
            return render_template('register_hospital.html')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO hospital(name,password,licence_no) "\
        "VALUES(%s,%s,%s)",(userDetails['name'], userDetails['password'],userDetails['licence_no']))
        
        
        # creating the particular hospital's database when hospital registers itself.

        cur.execute("CREATE TABLE {0} (equipment_name Varchar(50), price INT, count INT);".format(userDetails['name']))
        mysql.connection.commit()
        cur.close()

        flash('Registration successful! Please login.', 'success')
        return redirect('/login_hospital')
    return render_template('register_hospital.html')

@app.route('/login_hospital/', methods=['GET', 'POST'])
def login_hospital():
    redirect_to = is_logged_in( type = ['user' , 'admin' , 'hospital'],if_logged_in_link = '/hospital/')
    if  redirect_to != True:
        return redirect_to
    if request.method == 'POST':
        userDetails = request.form
        username = userDetails['name']
        cur = mysql.connection.cursor()
        resultValue = cur.execute("SELECT * FROM hospital WHERE name = %s", ([username]))
        if resultValue > 0:
            user = cur.fetchone()
            if userDetails['password'] == user['password']:
                session['login'] = True
                session['type'] = 'hospital'
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



# pages for admin_addprice disease , equipmennts , medicine
@app.route('/admin_addprice_disease/', methods=['GET', 'POST'])
def admin_addprice_disease():
    is_logged_in(type = ['admin'],if_not_logged_in_link = '/login_admin/')
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
    redirect_to = is_logged_in(type = ['admin'] , if_not_logged_in_link = '/login_admin/')
    if  redirect_to != True:
        return redirect_to
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
    redirect_to = is_logged_in(type = ['admin'],if_not_logged_in_link = '/login_admin/')
    if  redirect_to != True:
        return redirect_to
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

######### check if i entered correct database
@app.route('/hospital_addprice_disease/', methods=['GET', 'POST'])
def hospital_addprice_disease():
    is_logged_in(type = ['hospital'],if_not_logged_in_link = '/login_hospital/')
    if request.method == 'POST':
        userDetails = request.form
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO disease_gov(name,min_price,max_price,days_recover) "\
        "VALUES(%s,%s,%s,%s)",(userDetails['name'], userDetails['min_price'], userDetails['max_price'], userDetails['days_recover']))
        mysql.connection.commit()
        cur.close()
        flash('Data added to the database', 'success')
        return redirect('/hospital')
    return render_template('hospital_addprice_disease.html')


@app.route('/hospital_addprice_medicine/', methods=['GET', 'POST'])
def hospital_addprice_medicine():
    redirect_to = is_logged_in(type = ['hospital'],if_not_logged_in_link = '/login_hospital/')
    if  redirect_to != True:
        return redirect_to
    if request.method == 'POST':
        userDetails = request.form
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO medicine_gov(name,min_price,max_price) "\
        "VALUES(%s,%s,%s)",(userDetails['name'], userDetails['min_price'], userDetails['max_price']))
        mysql.connection.commit()
        cur.close()
        flash('Data added to the database', 'success')
        return redirect('/hospital')
    return render_template('hospital_addprice_medicine.html')


# user add report and admin view report

@app.route('/user_addreport/', methods=['GET', 'POST'])
def user_addreport():
    redirect_to = is_logged_in(type = ['user'],if_not_logged_in_link = '/login_user/')
    if  redirect_to != True:
        return redirect_to
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
    redirect_to = is_logged_in(type = ['user','admin','hospital'] ,if_not_logged_in_link = '/login_admin/')
    if  redirect_to != True:
        return redirect_to
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM complain")
    if resultValue > 0:
        complains = cur.fetchall()
        cur.close()
        return render_template('admin_viewreport.html', complains=complains , session = session)
    cur.close()
    return render_template('admin_viewreport.html',compalins=None , session = session)
    

# add and view experience    

@app.route('/add_experience/', methods=['GET', 'POST'])
def add_experience():
    redirect_to = is_logged_in(type = ['user'],if_not_logged_in_link = '/login_user/')
    if  redirect_to != True:
        return redirect_to
    if request.method == 'POST':
        userDetails = request.form
        print(userDetails['date'])
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO experience(experience, name, date) "\
        "VALUES(%s,%s,%s)",(userDetails['experience'], userDetails['name'], userDetails['date']))
        mysql.connection.commit()
        cur.close()
        flash('Your Experience Registered', 'success')
        return redirect('/view_experience')   #user's personal landing page
    return render_template('add_experience.html')


@app.route('/view_experience/', methods=['GET', 'POST'])
def view_experience():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM experience")
    if resultValue > 0:
        experience = cur.fetchall()
        cur.close()
        return render_template('view_experience.html', experience=experience)
    cur.close()
    return render_template('view_experience.html', experience=None)

@app.route('/user_find_hospital/', methods=['GET', 'POST'])
def user_find_hospital():
    return render_template('maps.html')

# to search price for disease , equipments , medicine

@app.route('/search_disease/', methods=['GET', 'POST'])
def search_disease():
    redirect_to = is_logged_in(type = ['user'],if_not_logged_in_link = '/login/')
    if  redirect_to != True:
        return redirect_to
    if request.method == 'POST':
        userDetails = request.form
        disease=userDetails['disease']
        cur = mysql.connection.cursor()
        resultValue = cur.execute("SELECT * FROM disease_gov where name=%s",([disease]))
        if resultValue > 0:
            data = cur.fetchall()
            cur.close()
            return render_template('search_disease.html', data=data)
        cur.close()
    return render_template('search_disease.html',data=None)

@app.route('/search_equipment/', methods=['GET', 'POST'])
def search_equipment():
    redirect_to = is_logged_in(type = ['user'],if_not_logged_in_link = '/login/')
    if  redirect_to != True:
        return redirect_to
    if request.method == 'POST':
        userDetails = request.form
        equipment=userDetails['equipment']
        cur = mysql.connection.cursor()
        resultValue = cur.execute("SELECT * FROM equipment_gov where name=%s",([equipment]))
        if resultValue > 0:
            data = cur.fetchall()
            cur.close()
            return render_template('search_equipment.html', data=data)
        cur.close()
    return render_template('search_equipment.html',data=None)

@app.route('/hospital_addprice_equipment/', methods=['GET', 'POST'])
def hospital_addprice_equipment():
    redirect_to = is_logged_in(type = ['hospital'] , if_not_logged_in_link = '/login_hospital/')
    if  redirect_to != True:
        return redirect_to
    if request.method == 'POST':
        userDetails = request.form
        cur = mysql.connection.cursor()
        hospital_name = session['Name']
        cur.execute(f"INSERT INTO {hospital_name} (price,equipment_name,count) "\
        "VALUES(%s,%s,%s)",(userDetails['price'], userDetails['name'] ,userDetails['count']))
        mysql.connection.commit()
        cur.close()
        flash('Data added to the database', 'success')
        return redirect('/hospital')
    return render_template('hospital_addprice_equipment.html')

@app.route('/hospital_update_count_equipments/', methods=['GET', 'POST'])
def hospital_update_count():
    redirect_to = is_logged_in(type = ['hospital'] , if_not_logged_in_link = '/login_hospital/')
    if  redirect_to != True:
        return redirect_to
    if request.method == 'POST':
        userDetails = request.form
        hospital_name = session['Name']
        cur = mysql.connection.cursor()
        cur.execute(f"UPDATE {hospital_name} SET count = '{userDetails['count']}' WHERE equipment_name = '{userDetails['name']}' ")
        cur.execute(f"UPDATE {hospital_name} SET price = '{userDetails['price']}' WHERE equipment_name = '{userDetails['name']}' ")
        mysql.connection.commit()
        cur.close()
        flash('Data updated to the database', 'success')
        return redirect('/hospital')
    return render_template('hospital_update_count_equipment.html')

@app.route('/search_medicine/', methods=['GET', 'POST'])
def search_medicine():
    redirect_to = is_logged_in(type = ['user'],if_not_logged_in_link = '/login/')
    if  redirect_to != True:
        return redirect_to
    if request.method == 'POST':
        userDetails = request.form
        medicine=userDetails['medicine']
        cur = mysql.connection.cursor()
        resultValue = cur.execute("SELECT * FROM medicine_gov where name=%s",([medicine]))
        if resultValue > 0:
            data = cur.fetchall()
            cur.close()
            return render_template('search_medicine.html', data=data)
        cur.close()
    flash('No such medicine','danger')     
    return render_template('search_medicine.html',data=None)


if __name__ == '__main__':
    app.run(debug=True, port=5001)