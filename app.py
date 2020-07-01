from flask import Flask, render_template, request
from test import SignUpForm
app = Flask(__name__)
app.config['SECRET_KEY']= 'qaz123'

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/test', methods= ['GET','POST'])
def test():
    form=SignUpForm()
    if form.is_submitted():
        result= request.form
        print("resss")
        print(result)
    return render_template('start.html',form=form)

@app.route('/product/<url>')
def product(url):
    print(url)
    return 'Hello, World!'