from flask import Flask, request, render_template, flash
from database import db_session, init_db
from models.search import Search ##import search.py裡面的class Search()

app = Flask(__name__)
app.secret_key = 'anldomokmoj'

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
@app.route('/search', methods=['GET'])
def renderSearch():
    return render_template('searchArea.html')

@app.route('/search', methods=['POST'])
def panduan():
    if request.method == 'POST':
        if 'searchArea' in request.form:
            #從前端searchArea.html的unputbox的name抓使用者輸入的值
            county = request.form.get("county")
            township = request.form.get("township")
            ##使用class Hospital()裡面的search_area方法
            return Search().search_area(county, township)
        elif 'searchDisease' in request.form:
            disease = request.form.get('disease')
            return Search().search_disease(disease)
        elif 'searchType' in request.form:
            type = request.form.get('type')
            return Search().search_type(type)
        elif 'searchCategory' in request.form:
            keyword1 = request.form.get('keyword1')
            keyword2 = request.form.get('keyword2')
            keyword3 = request.form.get('keyword3')
            keywords = []
            keywords.append(keyword1)
            keywords.append(keyword2)
            keywords.append(keyword3)
            return Search().search_category(keywords)

@app.route('/sort', methods=['GET'])
def renderSort():
    return render_template('Sort.html')

@app.route('/collection', methods=['GET'])
def renderCollection():
    return render_template('Collection.html')

@app.route('/login', methods=['GET'])
def renderLogin():
    return render_template('Login.html')

@app.route('/signup', methods=['GET'])
def renderSignup():
    return render_template('Signup.html')

##啟動
if __name__ == '__main__':
    app.jinja_env.auto_reloaded = True  ##jinja2 重新讀取template
    app.run(debug=True)