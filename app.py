from flask import Flask, redirect, request,send_from_directory,render_template,session, url_for,flash
from flask import send_from_directory
import json
import os
import hashlib
import pickle

with open('config.json') as data_file:
    config = json.load(data_file)

app = Flask(__name__, static_url_path='')


app.config.from_object(__name__)

@app.route('/')
def predict():
    return render_template("predict.html")

@app.route('/about-us')
def aboutus():
    return render_template("about-us.html")

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

if __name__ == '__main__':
    app.run(debug=True,host=config['host'],port=config['port'])

