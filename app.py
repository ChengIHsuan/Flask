from flask import Flask, request, render_template, flash
from database import db_session, init_db
from models.search import Search, Select ##import search.py裡面的class Search()
from models.sort import Sort
import sqlite3


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
        if 'choose' in request.form:
            items = request.values.getlist('item')
            sql_where = request.form.get('sqlstr')
            search_filter = request.form.get('tmp_filter')
            return Select().select_normal(sql_where, items, search_filter)
        elif 'searchAll' in request.form:
            ## 地區
            county = request.form.get("county")
            if county.find('台') != -1:
                county = county.replace('台', '臺')
            township = request.form.get("township")
            ## 特殊疾病
            disease1 = request.form.get('disease1')
            disease2 = request.form.get('disease2')
            disease3 = request.form.get('disease3')
            diseases = [disease1, disease2, disease3]
            ## 醫院層級
            types = request.values.getlist('type')
            ## 分類主題
            keywords = request.values.getlist('keyword')
            ## 醫院名稱
            name1 = request.form.get('name1')
            name2 = request.form.get('name2')
            name3 = request.form.get('name3')
            names = [name1, name2, name3]
            ## 評價結果
            star = request.form.get("star")
            positive = request.form.get("positive")
            negative = request.form.get("negative")
            return Search().search_all(county, township, diseases, types, keywords, names, star, positive, negative)
            # return Search().filter(county, township, diseases, types, keywords, names)
        elif 'reSort' in request.form:
            index1 = request.form.get('index4')
            item = request.form.get('items')
            sql_where2 = request.form.get('sql_where')
            filter = request.form.get('filter2')
            return Sort().reSort(index1, sql_where2, item, filter)
##啟動
if __name__ == '__main__':
    app.jinja_env.auto_reloaded = True  ##jinja2 重新讀取template
    app.run(debug=True)