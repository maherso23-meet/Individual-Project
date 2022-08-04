from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyAuw7ZoeAE7YKkDuWbhjJ-3KEG8dPnIqME",
  "authDomain": "first-firebase-web-32cfb.firebaseapp.com",
  "projectId": "first-firebase-web-32cfb",
  "storageBucket": "first-firebase-web-32cfb.appspot.com",
  "messagingSenderId": "690175495951",
  "appId": "1:690175495951:web:14a2b43b24cccb0b10787a",
  "measurementId": "G-XNW9C2B0WT",
  "databaseURL": "https://st-pro-5f373-default-rtdb.europe-west1.firebasedatabase.app"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

@app.route('/', methods=['GET', 'POST'])
def signin():

    error = ""
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))
       except:
           error = "Authentication failed"
    return render_template("signin.html")



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error=""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            users = {"email" : request.form['email'], "password" : request.form['password'], "name" : request.form['name'], "username" : request.form['username'], "bio" : request.form['bio']}
            db.child("users").child(login_session['user']['localId']).set(users)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"

    return render_template("signup.html")


@app.route('/home', methods=['GET', 'POST'])
def home():
    error:""
    if request.method == 'POST':
        try:
            return render_template('home.html')
        except:
            error="Authentication failed"
    uid = login_session['user']['localId']
    print(uid)
    user = db.child("users").child(uid).get().val()
    username = user['username']
    return render_template('home.html', username = username)







if __name__ == '__main__':
    app.run(debug=True) 

