from flask import Flask, request, render_template, flash
from database import db_session, init_db
from models.search import Search ##import search.py裡面的class Search()
from models.sort import Sort, Result
from models.test import Test

app = Flask(__name__)
app.secret_key = "mlkmslmpw"

#在接收到第一個request執行
@app.before_first_request
def init():
    init_db()  #初始化db

#正確關閉資料庫
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

##在地區搜尋介面取得使用者輸入的值/search_area
@app.route('/', methods=['GET'])
def renderSearch():
    return render_template('searchArea.html')

@app.route('/search', methods=['POST'])
def panduan():
    if request.method == 'POST':
        if 'searchArea' in request.form:
            #從前端searchArea.html的unputbox的name抓使用者輸入的值
            county = request.form.get("county")
            township = request.form.get("township")
            items = request.values.getlist('item')
            ##使用class Hospital()裡面的search_area方法
            return Search().search_area(county, township, items)
        elif 'searchDisease' in request.form:
            disease = request.form.get('disease')
            return Search().search_disease(disease)
        elif 'searchType' in request.form:
            types = request.values.getlist('type')
            items = request.values.getlist("item")
            return Search().search_type(types, items)
        elif 'searchCategory' in request.form:
            keyword1 = request.form.get('keyword1')
            keyword2 = request.form.get('keyword2')
            keyword3 = request.form.get('keyword3')
            keywords = []
            keywords.append(keyword1)
            keywords.append(keyword2)
            keywords.append(keyword3)
            return Search().search_category(keywords)
        elif 'searchName' in request.form:
            name1 = request.form.get('name1')
            name2 = request.form.get('name2')
            name3 = request.form.get('name3')
            names = []
            names.append(name1)
            names.append(name2)
            names.append(name3)
            items = request.values.getlist("item")
            return Search().search_name(names, items)
        elif 'area' in request.form:
            county = request.form.get("county")
            township = request.form.get("township")
            items = request.values.getlist('item')
            return Test().area_test(county, township, items)

@app.route('/sort', methods=['GET'])
def renderSort():
    return render_template('sortTest.html')

@app.route('/sort', methods=['POST'])
def sort_judge():
    if request.method == 'POST':
        if 'sortValue' in request.form:
            index1 = request.form.get('index1')
            index2 = request.form.get('index2')
            index3 = request.form.get('index3')
            indexes = []
            indexes.append(index1)
            indexes.append(index2)
            indexes.append(index3)
            return Sort().sort_value(indexes)
        elif 'reSort' in request.form:
            index = request.form.get('index')
            return Sort().reSort(index)

@app.route('/collection', methods=['GET'])
def renderCollection():
    return render_template('collection.html')

@app.route('/login', methods=['GET'])
def renderLogin():
    return render_template('login.html')

@app.route('/signup', methods=['GET'])
def renderSignup():
    return render_template('signup.html')

##########手機版##########
@app.route('/phone_search', methods=['GET'])
def renderPhoneSearch():
    return render_template('phoneHospital.html')

@app.route('/phone_search', methods=['POST'])
def phone_panduan():
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
        elif 'searchName' in request.form:
            name1 = request.form.get('name1')
            name2 = request.form.get('name2')
            name3 = request.form.get('name3')
            names = []
            names.append(name1)
            names.append(name2)
            names.append(name3)
            return Search().search_name(names)

@app.route('/phone_sort', methods=['GET'])
def renderPhoneSort():
    return render_template('phoneSort.html')

@app.route('/phone_collection', methods=['GET'])
def renderPhoneCollection():
    return render_template('phoneCollection.html')

@app.route('/phone_login', methods=['GET'])
def renderPhoneLogin():
    return render_template('phoneLogin.html')

@app.route('/phone_signup', methods=['GET'])
def renderPhoneSignup():
    return render_template('phoneSignup.html')

##啟動
if __name__ == '__main__':
    app.jinja_env.auto_reloaded = True  ##jinja2 重新讀取template
    app.run(debug=True)