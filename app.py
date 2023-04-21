from flask import Flask, redirect, request,send_from_directory,render_template,session, url_for,flash
from flask import send_from_directory
from flask_session import Session
from flask_bootstrap import Bootstrap
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
from flask_mysqldb import MySQL
import MySQLdb.cursors
import json
import os
import hashlib
import bcrypt
import pickle

with open('config.json') as data_file:
    config = json.load(data_file)

app = Flask(__name__, static_url_path='')


# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123'
app.config['MYSQL_DB'] = 'loansys'
# Intialize MySQL
mysql = MySQL(app)

# app.secret_key = "abc"
SESSION_PERMANENT = False
SESSION_TYPE = 'filesystem'
SECRET_KEY = 'abc'
SESSION_COOKIE_SECURE = True
REMEMBER_COOKIE_SECURE = True

app.config.from_object(__name__)
bootstrap = Bootstrap(app)





@app.route('/')
def index():
    if session.get('loggedin') is not None:
        return redirect(url_for('dashboard'))
    return render_template("index.html")

@app.route('/predict')
def predict():
    if session.get('loggedin') is not None:
         return render_template("predict.html")
    return redirect(url_for('signin'))


# Gender,Married,Dependents,Education,Self_Employed,ApplicantIncome,CoapplicantIncome,LoanAmount,Loan_Amount_Term,Credit_History,Property_Area,Loan_Status,LoanAmountOverIncome,Total_Income
# "Gender","Married","Dependents","Education","Self_Employed","ApplicantIncome","CoapplicantIncome","Credit_History","Property_Area"
@app.route("/loan-status-prediction",methods=["POST"])
def loan_status_predictor():
    if request.method == "POST":
        # credit_history = None
        gender = int(request.form.get("gender"))
        married = int(request.form.get("marital_status"))
        dependents = int(request.form.get('dependents'))
        self_employed = int(bool(request.form.get('self_employed',False)))
        applicant_income = int(request.form.get('applicant_income').split("₹")[1])
        coapplicant_income = int(request.form.get('coapplicant_income').split("₹")[1])
        loan_amount = int(request.form.get('loan_amount').split("₹")[1])
        credit_history = int(request.form.get('credit_history'))
        property_area = int(request.form.get('property_area')) 

		# Forming an input array
        input_array = [[gender,married,dependents,self_employed,applicant_income,coapplicant_income,loan_amount,credit_history,property_area]]

		# Loading Loan Status Predictor Model
        loan_status_predictor_model = pickle.load(open('model.pkl', 'rb'))

		# Prediction
        status_predicted = loan_status_predictor_model.predict(input_array)
        if status_predicted == 1:
            status_predicted = 'Y'
        elif status_predicted == 0:
            status_predicted = 'N'
		# Predicting Probability
        predict_proba = loan_status_predictor_model.predict_proba(input_array) * 100
        return render_template('loan_status_predictor.html',
                	        status_predicted = status_predicted,
                	        predict_proba = predict_proba)


@app.route('/sign-in')
def signin():
    return render_template("sign-in.html")

@app.route('/sign-up')
def signup():
    return render_template("sign-up.html")

@app.route('/about-us')
def aboutus():
    return render_template("about-us.html")

@app.route('/business')
def business():
    return render_template("business.html")

@app.route('/features')
def features():
    return render_template("features.html")


@app.route('/news')
def news():
    return render_template("news.html")

@app.route('/support')
def support():
    return render_template("support.html")

@app.route('/register',methods =['POST'])
def register():
    if request.method == 'POST' and 'firstName' in request.form and 'lastName' in request.form and 'email' in request.form and 'password' in request.form:
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = %s', [email])
        # Fetch one record and return result
        account = cursor.fetchone()
        if account:
            flash("Account already exists!", "danger")
            return render_template("sign-up.html")

        else:
        # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL,%s, %s, %s, %s)', (firstName,lastName, email,password))
            mysql.connection.commit()
            flash("You have successfully registered!", "success")
            return redirect(url_for('signin'))
       


@app.route("/login",methods = ["POST"])
@cross_origin(supports_credentials=True)
def login():
    if session.get('loggedin') is not None:
        return redirect(url_for('dashboard'))
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = %s AND password = %s', (email, password))
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['name'] = account['first_name']
           
            return render_template("dashboard.html",name=session['name'])
        else:
            # Account doesnt exist or username/password incorrect
            flash("Incorrect username/password!", "danger")
    return render_template("sign-in.html")
    
        

@app.route('/dashboard')
@cross_origin(supports_credentials=True)
def dashboard():
    if session.get('loggedin') is not None:
        return render_template('dashboard.html')
    return redirect(url_for('signin'))

@app.route("/logout")
def logout():
    session.pop('loggedin',None)
    session.pop('name',None)
    return redirect(url_for('signin'))


if __name__ == '__main__':
    app.run(debug=True,host=config['host'],port=config['port'])

