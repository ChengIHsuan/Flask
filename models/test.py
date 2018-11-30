import sqlite3
from flask import Flask, request, render_template, flash

class Result():

    def __init__(self):
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    ##欄位名稱
    def get_column_name(self, normal, ckbox, index):
        ##總資料數
        amount = len(ckbox)
        ##取得sqlstr中select的欄位，並以","做分割
        getColumns=['醫院資訊']
        for rr in range(len(index)):
            getColumns.append(index[rr])
        ##取得欄位名稱
        columns = []
        for c in getColumns:
            col = self.cursor.execute("SELECT abbreviation FROM column_name WHERE name = '" + c + "'").fetchone()[0]
            columns.append(col)
        return Result().table(normal, ckbox, columns)

    ##將搜尋結果寫進表格，需傳入(numpy array,總資料數,欄位名稱)
    def table(self, normal, ckbox, columns):
        ##選取的指標數量，-1是因為扣掉第一欄的醫院資訊
        ck_len = len(columns) - 1
        context = []
        for i in range(len(ckbox)):  ##0 1 2 3 4
            ##建立一個dict，獎每一筆結果轉存成dict的型態
            d = {}
            for j in range(ck_len):  ##0  1
                d[columns[j + 1]] = ckbox[i][j + 1]
            context.append(d)
        ##同時進行迭代
        z = zip(normal, context)
        return render_template('test.HTML', normal=normal, ck_len=ck_len, context=context, columns=columns, z=z)

class Select():

    def __init__(self):
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    ##取得醫院的基本資訊
    def get_normal(self, sql_where, items):
        ##select醫院的基本資料：名字、分數＆星等、正向評論數、中立評論數、負向評論數、電話與地址並存入normal[]
        sqlstr = "SELECT id, name, type, address FROM hospitals h" + sql_where
        normal = self.cursor.execute(sqlstr).fetchall()
        ##若未找到任何資料，出現錯誤訊息，若有則進入else
        if normal == []:
            flash('抱歉，找不到您要的資料訊息。')
            return render_template("test.html")
        else:
            return Select().get_checkbox(normal, items, sql_where)

    def get_checkbox(self, normal, items, sql_where):
        s = 'm.hospital_id'
        for rr in range(len(items)):
            s += (', ' + items[rr])
        sqlstr = "SELECT "+s+" FROM merge_data m JOIN hospitals h ON m.hospital_id = h.id" + sql_where
        print(sqlstr)
        ckbox = self.cursor.execute(sqlstr).fetchall()
        return Result().get_column_name(normal, ckbox, items)
        ############################




class Test():
    def __init__(self):
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    def area_test(self, county, township, items):
        ##若使用者輸入臺北，將會出現臺北及新北資料
        i = county.find('臺北')
        ##判斷使用者是否在縣市欄位輸入"臺北"，等於-1時為未找到"臺北"
        if i != -1:
            area = str("_北%" + township)
        else:
            area = str(county + '%' + township)
        sql_where = " WHERE h.address LIKE '" + area + "%'"
        return Select().get_normal(sql_where, items)



