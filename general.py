from flask import Flask,request

import test

app = Flask(__name__)
app1 = test.App()

@app.route("/")
def home():
	app1.start()

@app.route('/example', methods=['POST'])
def example():
    if request.method == 'POST':
        data = request.form['data']
        print(data)
        return f"The data you sent is: {data}"

@app.route("/about")
def about():
	return "HELLO about"