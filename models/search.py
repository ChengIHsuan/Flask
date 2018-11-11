import sqlite3
from flask import Flask, request, render_template, flash
import numpy as np
from tkinter import messagebox

class Search():

    def __init__(self):
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    ##看這個就好
    def search_area(self, county, township):
        ##若使用者輸入臺北，將會出現臺北及新北資料
        i = county.find('臺北')
        if i != -1:
            area = str("_北%" + township)
        else:
            area = str(county + '%' + township)
        sqlstr = "SELECT id,name,type,address FROM hospitals WHERE address LIKE '" + area + "%'"
        results = self.cursor.execute(sqlstr).fetchall()  ##執行sqlstr，並列出所有結果到results[]

        if results == []:
            return "none"
        else:
            ##將二維陣列results[]轉成numpy array，並計算總資料數
            n = np.array(results, dtype=str)
            amount = len(results)
            ##取得sqlstr中select的欄位，並以","做分割
            s = sqlstr.index("FROM") - 1
            column = (sqlstr[7:s]).split(',')
            return Search().table(n, amount, column)

    def search_type(self, type):
        t = {
            '1': "醫學中心",
            '2': "區域醫院",
            '3': "地區醫院",
            '4': "診所"
        }
        sqlstr = "SELECT id,name,type,address FROM hospitals WHERE type = '" + t.get(type) + "'"
        results = self.cursor.execute(sqlstr).fetchall()

        ##將二維陣列results[]轉成numpy array，並計算總資料數
        n = np.array(results, dtype=str)
        amount = len(results)
        ##取得sqlstr中select的欄位，並以","做分割
        s = sqlstr.index("FROM") - 1
        column = (sqlstr[7:s]).split(',')
        return Search().table(n, amount, column)

    ##將搜尋結果寫進表格，需傳入(numpy array,總資料數,欄位名稱)
    def table(self, n, amount, column):
        ##建立一個陣列，儲存整理好的資料結果
        context = []
        for i in range(amount):
            ##建立一個dict，獎每一筆結果轉存成dict的型態
            d = {}
            for j in range(len(column)):
                d[column[j]] = n[i,j]
            context.append(d)
        return render_template('searchArea.html', context = context)
