from flask import Flask,send_from_directory,render_template
from flask import send_from_directory
import json
import os

with open('config.json') as data_file:
    config = json.load(data_file)

app = Flask(__name__, static_url_path='')



@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/predict')
def predict():
    return app.send_static_file('predict.html')


if __name__ == '__main__':
    app.run(debug=True,host=config['host'],port=config['port'])

