from flask import Flask, request, render_template
from database import db_session, init_db
import sqlite3
from models.search import Hospital ##import search.py裡面的class Hoapital()
app = Flask(__name__)

#在接收到第一個request執行
@app.before_first_request
def init():
    init_db()  #初始化db

#正確關閉資料庫
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def index():
    return '<h1>Hello World</h1>'

##在地區搜尋介面取得使用者輸入的值/search_area
@app.route('/search_area', methods=['GET'])
def render():
    return render_template('searchArea.html')

##顯示搜尋結果/search_area
@app.route('/search_area', methods=['POST'])
def searchArea():
    ##從前端searchArea.html的unputbox的name抓使用者輸入的值
    county = request.form.get("county")
    township = request.form.get("township")
    ##使用class Hospital()裡面的search_area方法
    return Hospital().search_area(county, township)

@app.route('/say_hello', methods=['GET'])
def getdata():
    return render_template('index.html')

@app.route('/say_hello', methods=['POST'])
def submit():
 # return '{}, {}, {}'.format(input1, input2, input3)
 input1 = request.form.get("txt1")
 return Hospital().hospital_id(input1)

@app.route('/tuna')
def tuna():
    return '<h2>Tuna</h2>'

@app.route('/profile/<username>')
def profile(username):
    return "Hey there %s" % username

@app.route('/tuna/hospitals')
def hos():
    return '<h1>hospitals</h1>'

##啟動
if __name__ == '__main__':
    app.jinja_env.auto_reloaded = True  ##jinja2 重新讀取template
    app.run(debug=True)