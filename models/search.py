import sqlite3
from flask import Flask, request, render_template
import numpy as np
from pandas import DataFrame

class Hospital():

    def __init__(self):
        # self.table = 'hospitals'
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    ##不要看
    def hospital_id(self, id):
        # self.id = id
        sqlstr = "SELECT id, name, type, address FROM hospitals WHERE id < " + id
        results = self.cursor.execute(sqlstr).fetchall()

        res = ''
        for i in range(len(results)):
            res += (str(results[i]) + '\r')

        return res

    ##看這個就好
    def search_area(self, county, township):
        area = str(county + '%' + township + '%')
        sqlstr = "SELECT id, name, type, address FROM hospitals WHERE address LIKE '" + area + "'"
        results = self.cursor.execute(sqlstr).fetchall()  ##執行sqlstr，並列出所有結果到results

        x = np.array(results, dtype=str)
        context = []
        amount = len(results)

        # ##results是list，將results轉成字串res
        # res = ''
        # for i in range(len(results)):
        #     res += (str(results[i]) + '<br>')  ##<br>：換行符號
        # ##回傳字串res
        return Hospital().table(context=context, x=x, amount=amount)

    def table(self, context, x, amount):
        # sqlstr = "SELECT id, name, type, address FROM hospitals WHERE id <30"
        # results = self.cursor.execute(sqlstr).fetchall()

        for i in range(amount):
            context.append({
                    'id':(x[i,0]),
                    'name':(x[i,1]),
                    'type': (x[i, 2]),
                    'address': (x[i, 3]),
                })
        return render_template('testface.html', context = context)
        # return '<p>id：%s   name：%s</p>' % (hos_id, hos_name)
