from flask import Flask,send_from_directory,render_template
from flask import send_from_directory
from flask_bootstrap import Bootstrap
import json
import os

with open('config.json') as data_file:
    config = json.load(data_file)

app = Flask(__name__, static_url_path='')

bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict')
def predict():
    return render_template("predict.html")

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





if __name__ == '__main__':
    app.run(debug=True,host=config['host'],port=config['port'])

