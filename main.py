from flask import Flask, url_for, render_template, request, redirect, session, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
import PyPDF2
import pyttsx3
import os
from datetime import datetime
import random
from flask_mail import Mail, Message

app = Flask(__name__, template_folder='public', static_folder="src")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'abdulhannanzarrar001@gmail.com'
app.config['MAIL_PASSWORD'] = 'zkdfersdohilnblz'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, username, firstname, lastname, email, password):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password


class Audio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    user_id = db.Column(db.String(100))
    file = db.Column(db.String(100))

    def __init__(self, name, user_id, file):
        self.name = name
        self.user_id = user_id
        self.file = file


class ResstPassword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(100))
    user_id = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, token, user_id, email):
        self.token = token
        self.user_id = user_id
        self.email = email


@app.context_processor
def user():
    if 'user' in session:
        return {'user': User.query.get(session["user"])}
    else:
        return {}


@app.route('/', methods=['GET'])
def index():
    if 'user' in session:
        audios = Audio.query.all()
        return render_template('home.html', audios=audios)
    else:
        return render_template('index.html')


@app.route('/conversion/create', methods=['GET', 'POST'])
def pdfCreate():
    if request.method == 'GET':
        return render_template('/conversion/create.html')
    elif request.method == 'POST':
        name = request.form["name"]
        file = request.files['file']
        filename = f"audio{str(datetime.now().strftime('%y%m%d%S')) +''+str(random.randint(0, 100))}{session['user']}.mp3"
        pdf = PyPDF2.PdfFileReader(file)
        pages = pdf.numPages
        text = ""
        if pages <= 50:
            for i in range(pages):
                page = pdf.getPage(i)
                text += page.extractText()
            audio = pyttsx3.init()
            audio.save_to_file(text, f'src/audios/{filename}')
            audio.runAndWait()
            audio.stop()

            db.session.add(
                Audio(user_id=session['user'], name=name, file=filename))
            db.session.commit()
            flash("Pdf to Audio conversion successfully!", "success")
        else:
            flash("Only 50 pages are allowed to be convert!", "error")
        return redirect(url_for('index'))


@app.route('/conversion/update/<int:id>/', methods=['GET', 'POST'])
def pdfUpdate(id):
    audio = Audio.query.filter_by(id=id).first()
    if request.method == "GET":
        return render_template('/conversion/update.html', audio=audio)
    if request.method == "POST":
        name = request.form["name"]
        file = request.files['file']
        pdf = PyPDF2.PdfFileReader(file)
        pages = pdf.numPages
        if file.filename != "":
            try:
                os.remove(os.path.join('src/audios/', audio.file))
            except:
                pass
            if pages <= 50:
                filename = f"audio{str(datetime.now().strftime('%y%m%d%S')) +''+str(random.randint(0, 100))}{session['user']}.mp3"
                page = pdf.getPage(0)
                text = page.extractText()
                audio = pyttsx3.init()
                audio.save_to_file(text, f'src/audios/{filename}')
                audio.runAndWait()
                audio.stop()
                update = Audio.query.get(id)
                update.name = name
                update.file = filename
                db.session.commit()
                flash("Updated successfully!", "success")
            else:
                flash("Only 50 pages are allowed to be convert!", "danger")

            return redirect(url_for('index'))


@app.route('/conversion/delete/<int:id>/', methods=['GET'])
def pdfDelete(id):
    audio = Audio.query.filter_by(id=id).first()
    try:
        os.remove(os.path.join('./src/audios/', audio.file))
    except:
        pass
    db.session.delete(audio)
    db.session.commit()
    flash("Audio deleted successfully!", "success")
    return redirect(url_for('index'))


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html')
    elif request.method == 'POST':
        fullname = request.form["fullname"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        msg = Message('Easypdf customer query email',
                      sender='support@easypdf.com', recipients=[email])
        body = f'Hi! there, \n its <b> {fullname} </b> \n {message} \n <b>Phone :</b> {phone} \n Thanks \n Regards \n {fullname}.'
        msg.body = body
        mail.send(msg)
        flash("Email sent successfully!", "success")
    return render_template('contact.html')


@app.route('/terms-and-conditions', methods=['GET'])
def terms():
    return render_template('terms-and-conditions.html')


@app.route('/privacy-policy', methods=['GET'])
def privacy():
    return render_template('privacy-policy.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'GET':
        return render_template('profile.html')
    elif request.method == 'POST':
        user = User.query.get(session["user"])
        username = request.form["username"]
        first_name = request.form["firstname"]
        last_name = request.form["lastname"]
        email = request.form["email"]
        password = request.form["password"]
        if password == "":
            pwd = User.password
        else:
            pwd = password
        user.firstname = first_name
        user.lastname = last_name
        user.username = username
        user.email = email
        user.password = pwd
        db.session.commit()
        flash("Updated successfully!", "success")
        return render_template('profile.html')


@app.route('/help-center', methods=['GET'])
def help():
    return render_template('help-center.html')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        data = request.get_json()
        username = data["username"]
        firstname = data["firstname"]
        lastname = data["lastname"]
        email = data["email"]
        password = data["password"]

        if User.query.filter_by(username=username).first():
            return jsonify({"message": "This username already exists", "status": False})
        elif User.query.filter_by(email=email).first():
            return jsonify({"message": "This email already exists", "status": False})
        else:
            db.session.add(User(
                username=username,
                firstname=firstname,
                lastname=lastname,
                email=email,
                password=password))
            db.session.commit()
            return jsonify({"message": f"Account created successfully", "status": True})


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        data = User.query.filter_by(
            username=username, password=password).first()
        if data:
            session['user'] = data.id
            return jsonify({"message": "Login successfull!", "status": True})
        return jsonify({"message": "Incorrect credentials!", "status": False})


@app.route('/forgot-password/', methods=['GET', 'POST'])
def forgotpassword():
    if request.method == 'GET':
        return render_template('forgot-password.html')
    elif request.method == 'POST':
        email = request.form["email"]
        user = User.query.filter_by(email=email).first()
        if user:
            msg = Message('Password recovery email',
                          sender='support@easypdf.com', recipients=[email])
            token = f"{str(datetime.now().strftime('%y%m%d%S')) +''+str(random.randint(0, 100))}{user.id}"

            db.session.add(ResstPassword(
                token=token,
                user_id=user.id,
                email=email))
            db.session.commit()

            body = f"""
            Hi! there!, <br> This is a password verification link. click on it to change your password <br> 
            <a href="http://127.0.0.1:5000/recover-password/{user.id}/{token}/">Recover password</a>
            """
            msg.html = body
            mail.send(msg)
            flash("We sent you a verification link on your email address!", "success")
        else:
            flash("This email address does't exists in our database!", "danger")
        return render_template('forgot-password.html')


@app.route('/recover-password/<int:id>/<string:token>/', methods=['GET', 'POST'])
def changepassword(id, token):
    if request.method == 'GET':
        if ResstPassword.query.filter_by(user_id=id, token=token).first():
            return render_template('recover-password.html', token=token, id=id)
        else:
            flash("This token might be invalid!", "danger")
            return redirect(url_for('error404'))
    elif request.method == 'POST':
        password = request.form["password1"]
        user = User.query.get(id)
        if user:
            user.password = password
            db.session.commit()
            tokens = ResstPassword.query.filter_by(
                user_id=id, token=token).first()
            db.session.delete(tokens)
            db.session.commit()
            flash("Password changed successfully", "success")
            return redirect(url_for('login'))


@ app.route('/404', methods=['GET'])
def error404():
    return render_template('error404.html')


@ app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


if(__name__ == '__main__'):
    app.secret_key = "ThisIsNotASecret:p"
    db.create_all()
    app.run(debug=True)
