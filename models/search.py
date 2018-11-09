import sqlite3
from flask import Flask, request, render_template
import numpy as np

class Search():

    def __init__(self):
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    ##看這個就好
    def search_area(self, county, township):
        area = str(county + '%' + township + '%')
        sqlstr = "SELECT id,name,type,address FROM hospitals WHERE address LIKE '" + area + "'"
        results = self.cursor.execute(sqlstr).fetchall()  ##執行sqlstr，並列出所有結果到results[]

        ##將二維陣列results[]轉成numpy array，並計算總資料數
        n = np.array(results, dtype=str)
        amount = len(results)
        ##取得sqlstr中select的欄位，並以","做分割
        s = sqlstr.index("FROM") - 1
        column = (sqlstr[7:s]).split(',')
        return Search().table(n, amount, column)

    ##將搜尋結果寫進表格，需傳入(numpy array,總資料數,欄位名稱)
    def table(self, n, amount, column):
        context = []
        for i in range(amount):
            context.append({
                    column[0]: (n[i, 0]),
                    column[1]: (n[i, 1]),
                    column[2]: (n[i, 2]),
                    column[3]: (n[i, 3]),
                })
        return render_template('testface.html', context = context)
