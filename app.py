from flask import Flask, redirect, request,send_from_directory,render_template,session, url_for
from flask import send_from_directory
from flask_session import Session
from flask_bootstrap import Bootstrap
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
import json
import os
import hashlib
import bcrypt
import pickle

with open('config.json') as data_file:
    config = json.load(data_file)

app = Flask(__name__, static_url_path='')
# app.secret_key = "abc"
SESSION_PERMANENT = False
SESSION_TYPE = 'filesystem'
SECRET_KEY = 'abc'
app.config.from_object(__name__)
bootstrap = Bootstrap(app)
# mongodb connection
client = MongoClient('localhost', 27017)
Session(app)
CORS(app)




@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict')
def predict():
    return render_template("predict.html")

@app.route("/loan-status-prediction",methods=["POST"])
def loan_status_predictor():
    if request.method == "POST":
        # credit_history = None
        credit_history = float(request.form.get('credit_history'))
        loan_amount = float(request.form.get('loan_amount').split("₹")[1])
        applicant_income = float(request.form.get('applicant_income').split("₹")[1])
        coapplicant_income = float(request.form.get('coapplicant_income').split("₹")[1])
        dependents = float(request.form.get('dependents'))

		# Forming an input array
        input_array = [[credit_history, loan_amount, applicant_income, coapplicant_income, dependents]]

		# Loading Loan Status Predictor Model
        loan_status_predictor_model = pickle.load(open('model.pkl', 'rb'))

		# Prediction
        status_predicted = loan_status_predictor_model.predict(input_array)

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
    msg = ""
    if request.method == 'POST' and 'firstName' in request.form and 'lastName' in request.form and 'email' in request.form and 'password' in request.form:
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        sysDb = client['loansys']
        customersCollection = sysDb['customers']
        result = sysDb.customersCollection.find_one({"email":email})
        if result != None:
            hasAccount = True
        else:
            bytes = password.encode('utf-8')
  
            # generating the salt
            salt = bcrypt.gensalt(14)
        
            # Hashing the password
            hashValue = bcrypt.hashpw(bytes, salt)
            record = {
                "firstName" : firstName,
                "lastName"  : lastName,
                "email" : email,
                "password" : str(hashValue)
            }
            customersCollection.insert_one(record)
            # msg = "You have successfully registered !"
            hasAccount = False
        return render_template("register_success.html",msg=msg)

@app.route('/dashboard')
@cross_origin(supports_credentials=True)
def dashboard():
    return render_template("dashboard.html")

@app.route("/login",methods = ["POST"])
@cross_origin(supports_credentials=True)
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        sysDb = client['loansys']
        customers = sysDb.customers
        account = sysDb.customers.find_one({"email":email})
        # encoding user password
        if account:
            if bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt(14)) == account['password'].encode('utf-8'):
                session['loggedin'] = True
                session['email'] = str(account['email'])
                session['firstName'] = str(account['firstName'])
                session['lastName'] = str(account['lastName'])
                msg = 'Logged in successfully !'
            return redirect(url_for('dashboard'))
        msg = "No such account exists !"
        return render_template("sign-in.html",msg=msg)
        


if __name__ == '__main__':
    app.run(debug=True,host=config['host'],port=config['port'])

