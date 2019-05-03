import sqlite3
from flask import Flask, request, render_template, flash, redirect
from models.search import Search

class Hosp():

    def __init__(self):
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    def search_all(self, county, township, names, types, star):
        print('search_all')
        try:
            reserved = Search().hosp_reserved(county, township, names, types, star)
            print(reserved)
            sql_where = ''
            ## 取得地區、名稱、層級、星等的condition
            area_condition = Search().search_area(county, township)
            name_condition = Search().search_name(names)
            type_condition = Search().search_type(types)
            reviews_condition = Search().search_star(star)

            conditions = [area_condition, name_condition, type_condition, reviews_condition]
            print(conditions)
            ## 若沒有條件則移除
            while '' in conditions:
                conditions.remove('')
            for condition in conditions:
                if condition.find('抱歉') != -1:     #若為錯誤訊息，以alert提示#
                    return render_template('search.html', alert=condition)
                else:
                    condition = '(' + condition + ')'  #若不為錯誤訊息則在條件句前後加上括號-->之後放在SQL中才不會出錯#
                    ## 將所有condition相接，若不為最後一個condition則加上'AND'
                    if condition != ( '(' + conditions[-1] + ')' ):
                        sql_where += condition + "AND "
                    else:
                        sql_where += condition
            if sql_where != '':
                sql_where = 'WHERE ' + sql_where
            return Select().select_normal(sql_where, reserved)
        except BaseException as e:
            print('search_all Exception' + e)
            return  render_template('search.hml')

class Select():

    def __init__(self):
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    def select_normal(self, sql_where, reserved):
        print('select_normal')
        sqlstr = "SELECT h.abbreviation, h.type, cast(fr.star as float), fr.reviews, h.phone, h.address FROM hospitals h JOIN final_reviews fr ON h.id = fr.hospital_id  " + sql_where
        normal = self.cursor.execute(sqlstr).fetchall()  ## normal = [ (名稱, GOOGLE星等, 正向評論數, 負向評論數, 電話, 地址), ......]

        if normal == []:
            alert = "抱歉，找不到您要的資料訊息。"
            return render_template("search.html", alert=alert)
        else:
            return render_template("hospResult.html", normal=normal, reserved=reserved)

