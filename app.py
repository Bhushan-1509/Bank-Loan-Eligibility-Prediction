from flask import Flask,send_from_directory,render_template
from flask import send_from_directory
import json
import os

with open('config.json') as data_file:
    config = json.load(data_file)

app = Flask(__name__, static_url_path='')



@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict')
def predict():
    return render_template("predict.html")


if __name__ == '__main__':
    app.run(debug=True,host=config['host'],port=config['port'])

