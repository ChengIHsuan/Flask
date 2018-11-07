from flask import Flask, request, render_template
from database import db_session, init_db, engine
import sqlite3
from models.search import Hospital
app = Flask(__name__)

@app.before_first_request  #在接收到第一個request執行
def init():
    init_db()  #初始化db

@app.teardown_appcontext  #正確關閉資料庫
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def index():
    return '<h1>Hello World</h1>'

@app.route('/say_hello', methods=['GET'])
def getdata():
    return render_template('index.html')

@app.route('/say_hello', methods=['POST'])
def submit():
 # return '{}, {}, {}'.format(input1, input2, input3)
 input1 = request.form.get("txt1")
 return Hospital().hospital_id(input1)

@app.route('/hospital/type')
def get_hospital_type():
    return Hospital().get_type()

@app.route('/search', methods=['GET'])
def get_name():
    return render_template('search.html')

@app.route('/search', methods=['POST'])
def submitt():
    name1 = request.form.get('inputCategory3')
    return name1

@app.route('/tuna')
def tuna():
    return '<h2>Tuna</h2>'

@app.route('/profile/<username>')
def profile(username):
    return "Hey there %s" % username

@app.route('/tuna/hospitals')
def hos():
    return '<h1>hospitals</h1>'

if __name__ == '__main__':
    app.jinja_env.auto_reloaded = True  ##jinja2 重新讀取template
    app.run(debug=True)