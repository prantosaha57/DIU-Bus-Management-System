from sslcommerz_lib import SSLCOMMERZ
from flask_mail import Mail, Message
from flask import Flask, render_template, redirect, request, session, flash
import mysql.connector
import hashlib
import random
import os
from datetime import datetime

SSLCZ_SESSION_API = 'https://sandbox.sslcommerz.com/gwprocess/v4/api.php'

mydb = mysql.connector.connect(host='localhost', 
                               user='root', 
                               password='', 
                               database='users')

app = Flask(__name__, static_folder='static')

app.secret_key = "123@123"

UPLOAD_FOLDER = os.path.join('static', 'images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['STATIC_FOLDER'] = 'static'
app.config['STATIC_URL_PATH'] = '/static'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'diubus59@gmail.com'
app.config['MAIL_PASSWORD'] = 'pand drdl gidk kopz'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

c = mydb.cursor(buffered=True)

otp = random.randint(00000, 99999)
mail = Mail(app)
count = 0


@app.route('/')
@app.route('/index.html')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/home2')
def home2():
    return render_template('home2.html')


@app.route('/TryDifferentRoute.html')
def SearchForAvailableBus():
    if 'id' in session:
        return render_template('TryDifferentRoute.html')
    else:
        msg = flash("You need to login first")
        return render_template('index.html', msg=msg)
        


@app.route('/AfterLogin')
def afterlogin():
    return render_template('home1.html.html')


@app.route('/DeleteTicket.html')
def DeleteTicket():
    return render_template("DeleteTicket.html")


@app.route('/Dashboard.html')
def dashboard():
    # img_file_path = session.get('uploaded_img_file_path', None)
    id = session.get('id')
    use = c.execute("Select Name From student_signup Where ID Like '{}'".format(id))
    use = c.fetchone()
    if use is not None and len(use) > 0:
        name = str(use[0])
        return render_template('Dashboard.html', name=name, id=id)


@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('id', None)
    return render_template('index.html')


@app.route('/payment.html')
def paymets():
    c.execute("SELECT SUM(price) FROM payment_details")
    price = c.fetchone()[0]

    return render_template('payment.html', price=price)


@app.route('/BeforePay.html')
def BeforePay():
    return render_template('BeforePay.html')


@app.route('/forgotpassword.html')
def forgotpassword():
    return render_template('forgotpassword.html')


@app.route('/UpdateTicket.html')
def UpdateTicket():
    return render_template('UpdateTicket.html')


@app.route('/ChangeName.html')
def changename():
    return render_template('/ChangeName.html')


@app.route('/ChangePassword.html')
def changepass():
    return render_template('/ChangePassword.html')


@app.route('/ScheduleManagerView.html')
def ScheduleManager():
    return render_template('ScheduleManagerView.html')


@app.route('/ScheduleStudentView.html')
def ScheduleStudent():
    return render_template('ScheduleStudentView.html')


@app.route('/Tickets.html')
def Ticket():
    return render_template('Tickets.html')


@app.route('/Status.html')
def stat():
    return render_template('Status.html')


@app.route('/home1.html')
def home1():
    if 'id' in session:
        id = session['id']
        c.execute("SELECT * FROM student_signup WHERE ID =%s", (id,))
        user = c.fetchone()

        c.execute("Select * From student_signup Where ID LIKE '{}'".format(id))
        f = c.fetchone()
        if f is not None and len(f) > 0:
            f1 = f[7]
            t = f[8]

        # select_query = "SELECT * FROM payment_details WHERE user_id LIKE %s"
        select_query = 'SELECT * FROM payment_details WHERE user_id LIKE %s ORDER BY id DESC LIMIT 1'
        values = (id,)
        c.execute(select_query, values)
        last_ticket = c.fetchone()
        
        name = str(user[0])

        return render_template('home1.html', Froms=f1, Tos=t, name=name, id=id, last_ticket=last_ticket)


@app.route('/Passenger.html')
def passenger():
    return render_template('Passenger.html')


@app.route('/AddTicket.html')
def AddTicket():
    return render_template('AddTicket.html')


@app.route('/home2.html')
def homes2():
    return render_template('home2.html')


@app.route('/login', methods=["GET", "POST"])
def logins():
    if request.method == 'POST':
        id = request.form["id"]
        pass_word = request.form["password"]

        hash_object = hashlib.sha256(pass_word.encode())
        pass_word = hash_object.hexdigest()

        c.execute(
            "SELECT * FROM student_signup WHERE ID =%s AND Password=%s", (id, pass_word))
        user = c.fetchone()

        c.execute(
            "SELECT * FROM manager_signup WHERE ID =%s AND Password=%s", (id, pass_word))
        users = c.fetchone()

        c.execute(
            "SELECT * FROM driver_signup WHERE ID =%s AND Password=%s", (id, pass_word))
        uses = c.fetchone()

        # img_file_path = session.get('uploaded_img_file_path', None)

        session['id'] = id

        id = session.get('id')
        f1 = []
        t = []
        c.execute("Select * From payment_details Where user_id LIKE '{}' ORDER BY id DESC LIMIT 1".format(id))
        f = c.fetchone()
        if f is not None and len(f) > 0:
            f1 = f[1]
            t = f[2]
        select_query = "SELECT * FROM payment_details WHERE user_id LIKE %s ORDER BY id DESC LIMIT 1"
        values = (id,)
        c.execute(select_query, values)
        last_ticket = c.fetchone()
        
        if user is not None and len(user) > 0:
            name = str(user[0])
            session['last_ticket'] = last_ticket 

            last_ticket = session.get('last_ticket')
            # session['name'] = name
            # session['Froms'] = f1
            # session['Tos'] = t
            # name = session.get('name')
            # f1 = session.get('Froms')
            # t = session.get('Tos')
            return render_template('home1.html', Froms=f1, Tos=t, name=name, id=id, last_ticket=last_ticket)
        elif users is not None and len(users) > 0:

            return render_template('home2.html')

        elif uses is not None and len(uses) > 0:
            return render_template('home3.html')

        else:
            flash("Invalid Password or Email")
            msg = "Wrong ID or Password. Please Re-check your ID, Password and try again."
            return render_template("index.html", msg=msg)
    return render_template('index.html')


@app.route('/SeeLocationStdnt.html')
def Location():
    return render_template('SeeLocationStdnt.html')


@app.route('/opt1.html')
def opt1():
    return render_template('otp1.html')


@app.route('/singup.html', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        id = request.form["id"]
        email = request.form["email"]

        c.execute(
            "SELECT * FROM student_signup WHERE Email = %s or ID = %s", (email, id))
        user = c.fetchone()

        

        if user is not None and len(user) > 0:
            flash("Email  Already exsist")
            msg = "Email Already exsist"
            return render_template('singup.html', msg=msg)

        else:
            if '@diu.edu.bd' in email:
                c.execute("INSERT INTO student_signup (Name, ID, Email) VALUES (%s, %s, %s)",
                          (name, id, email))
                mydb.commit()
                c.execute(
                    "UPDATE student_signup SET OTP =%s WHERE Email =%s", (otp, email))
                mydb.commit()
                message = Message(
                    'OTP', sender='diubus59@gmail.com', recipients=[email])
                message.body = (
                    f"Dear {name},\n\n"
                    f"Your OTP for DIU Bus Management system is {otp}. Please use this code to complete your verification. "
                    "This code is valid for the next 10 minutes. Do not share it with anyone.\n\n"
                    "If you did not request this code, please contact us immediately at diubus59@gmail.com.\n\n"
                    "Thank you.\n"
                    "DIU Bus Management Team")
                mail.send(message)
                flash("OTP send you email")
                msg = "An OTP has been send to your email. Please check your email."
                return render_template('otp1.html', msg=msg)

            else:
                flash('Wrong Email')
                msg = 'Email does not exsist for diu email'
                return render_template('singup.html', msg=msg)
    return render_template('singup.html')


@app.route('/forgotpass', methods=["GET", "POST"])
def forgotpass():
    if request.method == 'POST':
        id = request.form["id"]
        email = request.form["email"]
        c.execute(
            "SELECT * FROM student_signup WHERE ID LIKE '{}' AND Email LIKE '{}'".format(id, email))

        user = c.fetchall()
        if user is not None and len(user) > 0:
            c.execute(
                "UPDATE student_signup SET OTP =%s WHERE Email =%s", (otp, email))
            mess = Message(
                'OTP', sender='diubus59@gmail.com', recipients=[email])
            mess.body = (
                f"We received a request to reset your password for the DIU Bus Management system. Your OTP for password reset is {otp}. "
                "This code is valid for the next 10 minutes. Please use this code to complete your password reset process.\n\n"
                "Important: Do not share this OTP with anyone to ensure the security of your account.\n\n"
                "If you did not request a password reset, please contact us immediately at diubus59@gmail.com.\n\n"
                "Thank you for using DIU Bus Management system.\n\n"
                "Best regards,\n"
                "DIU Bus Management Team")
            mail.send(mess)
            flash("OTP send you email")
            msg = "An OTP has been send to your email. Please check your email."
            return render_template('otp.html', msg=msg)
        else:
            flash("Email or ID not found! Please signup first")
            return render_template("forgotpassword.html")


@app.route('/verify1', methods=["GET", "POST"])
def verify1():
    if request.method == "POST":
        user_otp = request.form["otp"]
        if otp == int(user_otp):
            return render_template('CreatePassword.html')
        else:
            flash("Wrong OTP")
            msg = "Wrong OTP"
            return render_template('otp1.html', msg=msg)
    return render_template('otp1.html')


@app.route('/created', methods=["GET", "POST"])
def changepassword():
    password = request.form["password"]
    confirmpassword = request.form["confirmpassword"]

    hash_object = hashlib.sha256(password.encode())
    password = hash_object.hexdigest()

    hash_object1 = hashlib.sha256(confirmpassword.encode())
    confirmpassword = hash_object1.hexdigest()

    if password == confirmpassword:
        c.execute("Update student_signup Set Password =%s, ConfirmPassword =%s Where OTP =%s",
                  (password, confirmpassword, otp))
        c.fetchone()
        mydb.commit()
        mydb.close()
        flash("Successfully Created Account")
        msg = "Your account has been created. You can signin any time. "
        return render_template("index.html", msg=msg)


@app.route('/verify', methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        user_otp = request.form["otp"]
        if otp == int(user_otp):
            return render_template('resetpassword.html')
    return "Wrong OTP"


@app.route('/respass', methods=["GET", "POST"])
def respass():
    if request.method == "POST":
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']

        hash_object = hashlib.sha256(password.encode())
        password = hash_object.hexdigest()

        hash_object1 = hashlib.sha256(confirmpassword.encode())
        confirmpassword = hash_object1.hexdigest()
        if password == confirmpassword:
            c.execute("Update student_signup Set Password =%s, ConfirmPassword =%s Where OTP =%s",
                      (password, confirmpassword, otp))
            c.fetchone()
            mydb.commit()
            mydb.close()
            flash
            return render_template("index.html")
        else:
            flash("Incorrect password")
            return render_template("resetpassword.html")


@app.route('/edit_name', methods=["GET", "POST"])
def editname():
    if request.method == "POST":
        old_name = request.form['old_name']
        new_name = request.form['new_name']

        id = session.get('id')
        c.execute(
            "SELECT * FROM student_signup WHERE ID = %s AND Name = %s", (id, old_name))
        user = c.fetchone()

        if user is not None:
            c.execute(
                "UPDATE student_signup SET Name = %s WHERE ID = %s", (new_name, id))
            mydb.commit()
            flash('Username change successfully')
            msg = 'Username change successfully'
            return render_template("ChangeName.html", msg=msg)
        else:
            flash('Username change failed')
            msg = 'Can not Change Username'
            return render_template("ChangeName.html", msg=msg)
    return render_template("ChangeName.html")


@app.route('/edit_password', methods=["GET", "POST"])
def editpassword():
    if request.method == "POST":
        old_password = request.form['old_password']
        new_password = request.form['new_password']

        hash_object = hashlib.sha256(old_password.encode())
        old_password = hash_object.hexdigest()

        hash_object = hashlib.sha256(new_password.encode())
        new_password = hash_object.hexdigest()

        id = session.get('id')
        c.execute(
            "SELECT * FROM student_signup WHERE ID = %s AND Password = %s", (id, old_password))
        user = c.fetchone()

        if user is not None:
            c.execute("UPDATE student_signup SET Password = %s, ConfirmPassword = %s WHERE ID = %s",
                      (new_password, new_password, id))
            mydb.commit()
            flash('Password change successfully')
            msg = 'Password change successfully'
            return render_template("ChangePassword.html", msg=msg)
        else:
            flash('Password change failed')
            msg = 'Can not Change Password'
            return render_template("ChangePassword.html", msg=msg)
    return render_template("ChangePassword.html")


@app.route('/add_ticket', methods=["GET", "POST"])
def add_ticket():
    if request.method == "POST":
        froms = request.form.get('route1')
        tos = request.form.get('route2')

        if tos == 'Dhanmondi':
            c.execute(
                "Select * From route_diu_dhan Where Froms=%s AND Tos=%s", (froms, tos))
            dhans = c.fetchall()
            return render_template("Tickets.html", dhans=dhans)
        elif froms == 'Dhanmondi':
            c.execute(
                "Select * From route_diu_dhan1 Where Froms=%s AND Tos=%s", (froms, tos))
            dhans = c.fetchall()
            return render_template("Tickets.html", dhans=dhans)
        elif tos == 'Mirpur':
            c.execute(
                "Select * From route_diu_mir Where Froms=%s AND Tos=%s", (froms, tos))
            dhans = c.fetchall()
            return render_template("Tickets.html", dhans=dhans)
        elif froms == 'Mirpur':
            c.execute(
                "Select * From route_diu_mir1 Where Froms=%s AND Tos=%s", (froms, tos))
            dhans = c.fetchall()
            return render_template("Tickets.html", dhans=dhans)

        elif tos == 'Uttara':
            c.execute(
                "Select * From route_diu_utta Where Froms=%s AND Tos=%s", (froms, tos))
            dhans = c.fetchall()
            return render_template("Tickets.html", dhans=dhans)
        elif froms == 'Uttara':
            c.execute(
                "Select * From route_diu_utta1 Where Froms=%s AND Tos=%s", (froms, tos))
            dhans = c.fetchall()
            return render_template("Tickets.html", dhans=dhans)


@app.route('/SearchForAvailableBus', methods=['GET'])
def search_results():
    location1 = request.args.get('location1')
    location2 = request.args.get('location2')

    query = "SELECT * FROM ticket WHERE froms=%s AND tos=%s"
    c.execute(query, (location1, location2))

    tickets = c.fetchall()
    return render_template('SearchForAvailableBus.html', tickets=tickets)


@app.route('/buses', methods=["GET", "POST"])
def saves():
    if request.method == 'POST':
        id = session.get('id')

        save = request.form.getlist('save')
        froms = request.form.get('from')
        to = request.form.get('to')
        print(id, save)
        c.execute("Select * From student_signup Where ID Like '{}'".format(id))
        user = c.fetchone()
        query = "SELECT * FROM ticket WHERE froms=%s AND tos=%s"
        c.execute(query, (froms, to))
        # Fetch all the matching records
        tickets = c.fetchall()

        if user is not None and len(user) > 0:
            return render_template('SearchForAvailableBus.html', tickets=tickets)

        if save == 'on':
            query = "UPDATE student_signup SET Froms = %s, Tos = %s WHERE ID = %s"
            values = (froms, to, id)
            c.execute(query, values)
            mydb.commit()
            return render_template('SearchForAvailableBus.html', tickets=tickets)


@app.route('/Status.html')
def status():
    return render_template("Status.html")


@app.route('/filters',  methods=["GET", "POST"])
def filtering():
    if request.method == "POST":
        froms = request.form.get('froms')
        tos = request.form.get('tos')
        print(froms, tos)

        if froms == 'Dhanmondi':
            c.execute(
                "SELECT * FROM route_diu_dhan1 WHERE Froms=%s AND Tos=%s", (froms, tos))
            dhans = c.fetchall()
            return render_template("Status.html", dhans=dhans)
        elif tos == 'Dhanmondi':
            print(froms, tos)
            c.execute(
                "Select * From route_diu_dhan Where Froms=%s AND Tos=%s", (froms, tos))
            dhans = c.fetchall()
            return render_template("Status.html", dhans=dhans)
        elif tos == 'Mirpur':
            c.execute(
                "SELECT * FROM route_diu_mir WHERE Froms=%s AND Tos=%s", (froms, tos))
            dhans = c.fetchall()
            return render_template("Status.html", dhans=dhans)
        elif froms == 'Mirpur':
            c.execute(
                "SELECT * FROM route_diu_mir1 WHERE Froms=%s AND Tos=%s", (froms, tos))
            dhans = c.fetchall()
            return render_template("Status.html", dhans=dhans)
        elif tos == 'Uttara':
            c.execute(
                "SELECT * FROM route_diu_utta WHERE Froms=%s AND Tos=%s", (froms, tos))
            dhans = c.fetchall()
            return render_template("Status.html", dhans=dhans)
        elif froms == 'Uttara':
            c.execute(
                "SELECT * FROM route_diu_utta1 WHERE Froms=%s AND Tos=%s", (froms, tos))
            dhans = c.fetchall()
            return render_template("Status.html", dhans=dhans)

    return tos


@app.route('/search_buses', methods=["GET", "POST"])
def bus_search():
    if request.method == "POST":
        froms = request.form.get('from')
        tos = request.form.get('to')

        old_start = request.form.get('old_start_time')
        old_end = request.form.get('old_end_time')

        new_start = request.form.get('new_start_time')
        new_end = request.form.get('new_end_time')

        time_new = datetime.strptime(new_start, "%H:%M")
        time_old = datetime.strptime(old_start, "%H:%M")

        new_start = time_new.strftime("%I:%M %p")
        old_start = time_old.strftime("%I:%M %p")

        tk = request.form.get('tk')
        status = request.form.get('status')

        if tos == 'Dhanmondi':
            c.execute("Update route_diu_dhan SET Start_Time = %s, Ticket_Fair=%s, Bus_Status=%s Where Start_Time = %s",
                      (new_start, tk, status, old_start))
            mydb.commit()
            return render_template("home2.html")
        elif froms == 'Dhanmondi':
            c.execute("Update route_diu_dhan1 SET Start_Time = %s, Ticket_Fair=%s, Bus_Status=%s Where Start_Time = %s",
                      (new_start, tk, status, old_start))
            mydb.commit()
            return render_template("home2.html")
        elif tos == 'Mirpur':
            c.execute("Update route_diu_mir SET Start_Time = %s, Ticket_Fair=%s, Bus_Status=%s Where Start_Time = %s",
                      (new_start, tk, status, old_start))
            mydb.commit()
            return render_template("home2.html")
        elif froms == 'Mirpur':
            c.execute("Update route_diu_mir1 SET Start_Time = %s, Ticket_Fair=%s, Bus_Status=%s Where Start_Time = %s",
                      (new_start, tk, status, old_start))
            mydb.commit()
            return render_template("home2.html")

        elif tos == 'Uttara':
            c.execute("Update route_diu_utta SET Start_Time = %s, Ticket_Fair=%s, Bus_Status=%s Where Start_Time = %s",
                      (new_start, tk, status, old_start))
            mydb.commit()
            return render_template("home2.html")
        elif froms == 'Uttara':
            c.execute("Update route_diu_utta1 SET Start_Time = %s, Ticket_Fair=%s, Bus_Status=%s Where Start_Time = %s",
                      (new_start, tk, status, old_start))
            mydb.commit()
            return render_template("home2.html")


@app.route('/stdnt_view', methods=["GET", "POST"])
def stdnt_view():
    if request.method == "POST":
        froms = request.form.get('routes1')
        tos = request.form.get('routes2')

        if tos == 'Dhanmondi':
            c.execute(
                "Select * From route_diu_dhan Where Froms=%s AND Tos=%s", (froms, tos))
            dhans = c.fetchall()

            return render_template("ScheduleStudentView.html", dhans=dhans)
        elif froms == 'Dhanmondi':
            c.execute(
                "Select * From route_diu_dhan1 Where Froms=%s AND Tos=%s", (froms, tos))
            dhans = c.fetchall()
            return render_template("ScheduleStudentView.html", dhans=dhans)
        elif tos == 'Mirpur':
            c.execute(
                "Select * From route_diu_mir Where Froms=%s AND Tos=%s", (froms, tos))
            dhans = c.fetchall()
            return render_template("ScheduleStudentView.html", dhans=dhans)
        elif froms == 'Mirpur':
            c.execute(
                "Select * From route_diu_mir1 Where Froms=%s AND Tos=%s", (froms, tos))
            dhans = c.fetchall()
            return render_template("ScheduleStudentView.html", dhans=dhans)

        elif tos == 'Uttara':
            c.execute(
                "Select * From route_diu_utta Where Froms=%s AND Tos=%s", (froms, tos))
            dhans = c.fetchall()
            return render_template("ScheduleStudentView.html", dhans=dhans)
        elif froms == 'Uttara':
            c.execute(
                "Select * From route_diu_utta1 Where Froms=%s AND Tos=%s", (froms, tos))
            dhans = c.fetchall()
            return render_template("ScheduleStudentView.html", dhans=dhans)
        elif tos == 'None':
            msg = flash("Please select necessary location")
            return render_template("ScheduleStudentView.html", msg=msg)
        elif froms=='None':
            msg = flash("Please select necessary location")
            return render_template("ScheduleStudentView.html", msg=msg)
        # else:
        #     print(froms, tos)


@app.route("/delete_ticket", methods=["GET", "POST"])
def deletes():
    if request.method == "POST":
        froms = request.form.get('from')
        tos = request.form.get('to')

        start_time = request.form.get('start_time')
        time_new = datetime.strptime(start_time, "%H:%M")
        start_time = time_new.strftime("%I:%M %p")
        print(froms, tos, start_time)
        if tos == 'Dhanmondi':
            c.execute(
                "Delete From route_diu_dhan Where Start_Time=%s", (start_time,))
            mydb.commit()

            return render_template("home2.html")
        elif froms == 'Dhanmondi':
            c.execute(
                "Delete From route_diu_dhan1 Where Start_Time=%s", (start_time,))

            return render_template("home2.html")
        elif tos == 'Mirpur':
            c.execute(
                "Delete From route_diu_mir Where Start_Time=%s", (start_time,))

            return render_template("home2.html")
        elif froms == 'Mirpur':
            c.execute(
                "Delete From route_diu_mir1 Where Start_Time=%s", (start_time,))

            return render_template("home2.html")

        elif tos == 'Uttara':
            c.execute(
                "Delete From route_diu_utta Where Start_Time=%s", (start_time,))

            return render_template("home2.html")
        elif froms == 'Uttara':
            c.execute(
                "Delete From route_diu_utta1 Where Start_Time=%s", (start_time,))

            return render_template("home2.html")

@app.route("/pay", methods=["GET"])
def pay():
    settings = {'store_id': 'testbox',
                'store_pass': 'qwerty', 
                'issandbox': True}
    sslcz = SSLCOMMERZ(settings)

    userID = session.get('id')
    from_location = request.args.get('from')
    to_location = request.args.get('to')
    price = request.args.get('price')

    post_body = {}
    post_body['total_amount'] = price
    post_body['currency'] = "BDT"
    post_body['tran_id'] = "12345"
    post_body['success_url'] = "http://127.0.0.1:5000/pay_success?from=" + from_location + "&to=" + to_location + "&price=" + price + "&userID=" + userID
    post_body['fail_url'] = "http://127.0.0.1:5000/"
    post_body['cancel_url'] = "http://127.0.0.1:5000/"
    post_body['emi_option'] = 0
    post_body['cus_name'] = "test"
    post_body['cus_email'] = "test@test.com"
    post_body['cus_phone'] = "01700000000"
    post_body['cus_add1'] = "customer address"
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "Test"
    post_body['product_category'] = "Test Category"
    post_body['product_profile'] = "general"
    response = sslcz.createSession(post_body)
    return redirect(response["GatewayPageURL"])


@app.route('/search_bus', methods=["GET", "POST"])
def AddTickets():
    if request.method == 'POST':
        From = request.form.get('from')
        To = request.form.get('to')

        tk = request.form.get('tk')
        status = request.form.get('status')

        Start_Time = request.form.get('start_time')
        End_Time = request.form.get('end_time')

        time_new = datetime.strptime(Start_Time, "%H:%M")

        Start_Time = time_new.strftime("%I:%M %p")

        c.execute("INSERT INTO ticket SET Froms = %s, Tos = %s, Start_Time=%s, Ticket_Fair=%s, Bus_Status=%s",
                  (From, To, Start_Time, tk, status))
        mydb.commit()
        return render_template('home2.html')


@app.route('/find_bus', methods=["GET", "POST"])
def buses():
    if request.method == "POST":
        From = request.form['route']
        To = request.form['routes']

        return render_template('Tickets.html')


@app.route('/payment_method')
def payment_method():
    from_location = request.args.get('from')
    to_location = request.args.get('to')
    start_time = request.args.get('starttime')
    end_time = request.args.get('endtime')
    price = request.args.get('price')

    return render_template('PaymentMethod.html', from_location=from_location, to_location=to_location,
                           start_time=start_time, end_time=end_time, price=price)


@app.route('/pay_success', methods=["POST"])
def pay_success():
    from_location = request.args.get('from')
    to_location = request.args.get('to')
    price = request.args.get('price')
    user_id = request.args.get('userID')
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(current_date)
    insert_query = "INSERT INTO payment_details (from_location, to_location, price, user_id, Date) VALUES (%s, " \
                   "%s, %s, %s ,%s) "
    values = (from_location, to_location, price, user_id, current_date)
    c.execute(insert_query, values)
    mydb.commit()
    t = []
    f1 = []
    c.execute("Select * From payment_details Where user_id LIKE '{}' ORDER BY id DESC LIMIT 1".format(user_id))
    f = c.fetchone()
    
    if f is not None and len(f) > 0:
        f1 = f[1]
        t = f[2]
    
    print(f1, t)

    c.execute("SELECT * FROM student_signup WHERE ID = '{}'".format(user_id))
    user = c.fetchone()

    select_query = "SELECT * FROM payment_details WHERE user_id LIKE %s ORDER BY id LIMIT 1"
    vals = (user_id,)
    
    c.execute(select_query, vals)
    last_ticket = c.fetchone()
    
    return render_template('home1.html', Froms=f1, Tos=t, name=user[0], id=user_id, last_ticket=f)


if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0')