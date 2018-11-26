import sqlite3
from flask import Flask, request, render_template, flash

class Sort():

    def __init__(self):
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    def sort_value(self, indexes):
        try:
            substr = ''
            for index in indexes:
                if index != "":
                    getId = self.cursor.execute("SELECT id FROM indexes WHERE (name LIKE '%" + index + "%')")
                    indexId = (getId.fetchone()[0])
                    substr += ', m.m_' + str(indexId)
                sqlstr = "SELECT h.name"+ substr + " FROM hospitals h JOIN merge_data m ON h.id = m.hospital_id"
            results = self.cursor.execute(sqlstr).fetchall()  ##執行sqlstr，並列出所有結果到results[]
            print(sqlstr)
            print('return囉')
            return Result().get_column_name(results, sqlstr)
        except:
            flash('抱歉，找不到您要的「{}」相關資訊。'.format(index))
            return render_template("sortTest.html")

    def reSort(self, index):
        li = index.split("&")
        print(li)
        pre_sqlstr = li[1].replace("//", " ")
        print(pre_sqlstr)
        name = self.cursor.execute("select name from column_name where abbreviation = '" + li[0] + "'").fetchone()[0]
        sqlstr = pre_sqlstr + " order by " + name + " DESC"
        print(sqlstr)
        results = self.cursor.execute(sqlstr).fetchall()  ##執行sqlstr，並列出所有結果到results[]
        print('return囉')
        return Result().get_column_name(results, sqlstr)


class Result():

    def __init__(self):
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    def get_column_name(self, results, sqlstr):
        ##將二維陣列results[]轉成numpy array，並計算總資料數
        amount = len(results)
        ##取得sqlstr中select的欄位，並以","做分割
        s = sqlstr.index("FROM") - 1
        getColumns = (sqlstr[7:s]).split(', ')
        ##取得欄位名稱
        columns = []
        for c in getColumns:
            print(c)
            col = self.cursor.execute("SELECT abbreviation FROM column_name WHERE name = '" + c + "'").fetchone()[0]
            columns.append(col)
        indexes = columns[1:]
        print(indexes)
        return Result().table(results, amount, columns, indexes, sqlstr)

    ##將搜尋結果寫進表格，需傳入(numpy array,總資料數,欄位名稱)

    def table(self, results, amount, columns, indexes, sqlstr):
        ##建立一個陣列，儲存整理好的資料結果
        context = []
        for i in range(len(results)):
            ##建立一個dict，獎每一筆結果轉存成dict的型態
            d = {}
            for j in range(len(columns)):
                d[columns[j]] = results[i][j]
            context.append(d)
        long = len(columns)
        sqlstr = sqlstr.replace(" ", "//")
        print("===")
        print(sqlstr)
        return render_template('sortTest.html', scroll = 'results' , context=context, columns=columns, long=long, indexes=indexes, sqlstr=sqlstr)