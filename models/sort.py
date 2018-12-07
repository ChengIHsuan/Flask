import sqlite3
from flask import Flask, request, render_template, flash

class Sort():

    def __init__(self):
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    def sort_value(self, indexes):
     #  try:
            substr = ''
            for index in indexes:
                if index != "":
                    getId = self.cursor.execute("SELECT id FROM indexes WHERE (name LIKE '%" + index + "%')")
                    indexId = (getId.fetchone()[0])
                    substr += ', m.m_' + str(indexId)

                sqlstr = "SELECT h.name"+ substr + " FROM hospitals h JOIN merge_data m ON h.id = m.hospital_id"
            results = self.cursor.execute(sqlstr).fetchall()  ##執行sqlstr，並列出所有結果到results[]
            print(sqlstr)
            print('return囉1')
            return Sort().get_normal(results, sqlstr)
     #  except:
     #       flash('抱歉，找不到您要的「{}」相關資訊。'.format(index))
     #       return render_template("sortTest.html")

    def reSort(self, index1,index2,index3):
        print(index1)
        print(index2)
        print(index3)
        li = index1.split("&")
        print(1)
        print(li)

        a = []
        a.append(li[0])
        a.append(index2)
        a.append(index3)
        while '請選擇排序' in a:
            a.remove('請選擇排序')
        print(a)

        pre_sqlstr = li[1].replace("//", " ")
        print(2)
        print(pre_sqlstr)
        names =[]
        for rr in a:
           name = self.cursor.execute("select name from column_name where abbreviation = '" + rr + "'").fetchone()[0]
           names.append(name)

        change = ""
        for tt in range(len(names)):
            x = names[tt].replace("m.m" , "f.v")
            if names[tt] != names[-1]:
              change += (x + " DESC, ")
            else :
              change += (x + " DESC")

        print(change)

        sqlstr = pre_sqlstr + " Join final_data f ON h.id = f.hospital_id order by " + change
        print(3)
        print(sqlstr)
        results = self.cursor.execute(sqlstr).fetchall()  ##執行sqlstr，並列出所有結果到results[]
        print('return囉2')
        return Sort().get_normal2(results, sqlstr ,change)


    def get_normal(self, results, sqlstr):
        ## 將condition改回

        ## select醫院的基本資料：名字、分數＆星等、正向評論數、中立評論數、負向評論數、電話與地址並存入normal[]
        sqlstr2 = "SELECT h.name, 'GOOGLE分數', '正面評論數：'||mr.better,  '負面評論數：'||mr.worse, '中立評論數：'||mr.normal, h.phone, h.address FROM hospitals h JOIN merge_reviews mr ON h.id=mr.hospital_id"
        print(sqlstr)
        normal = self.cursor.execute(sqlstr2).fetchall()
        ## 若未找到任何資料，出現錯誤訊息，若有則進入else
        if normal == []:
            flash('抱歉，找不到您要的資料訊息。')
            return render_template("searchArea.html")
        else:
            return Result().get_column_name(normal, results, sqlstr)

    def get_normal2(self, results, sqlstr , change):
        ## 將condition改回

        ## select醫院的基本資料：名字、分數＆星等、正向評論數、中立評論數、負向評論數、電話與地址並存入normal[]
        sqlstr2 = "SELECT h.name, 'GOOGLE分數', '正面評論數：'||mr.better,  '負面評論數：'||mr.worse, '中立評論數：'||mr.normal, h.phone, h.address FROM hospitals h JOIN merge_reviews mr ON h.id=mr.hospital_id  Join final_data f ON h.id = f.hospital_id order by " + change
        print(sqlstr2)
        normal = self.cursor.execute(sqlstr2).fetchall()
        ## 若未找到任何資料，出現錯誤訊息，若有則進入else
        if normal == []:
            flash('抱歉，找不到您要的資料訊息。')
            return render_template("searchArea.html")
        else:
            return Result().get_column_name(normal, results, sqlstr)


class Result():

    def __init__(self):
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    def get_column_name(self,normal ,results, sqlstr ):
        ##將二維陣列results[]轉成numpy array，並計算總資料數
        amount = len(results)
        ##取得sqlstr中select的欄位，並以","做分割
        s = sqlstr.index("FROM") - 1
        getColumns = (sqlstr[7:s]).split(', ')
        print(1)
        print(getColumns)

        ##取得欄位名稱
        columns = []
        for c in getColumns:
            print(c)
            col = self.cursor.execute("SELECT abbreviation FROM column_name WHERE name = '" + c + "'").fetchone()[0]
            columns.append(col)
        indexes = columns[1:]
        print(columns)
        print(indexes)
        return Result().table(normal ,results, columns, indexes, sqlstr)

    ##將搜尋結果寫進表格，需傳入(numpy array,總資料數,欄位名稱)

    def table(self,normal ,results, columns, indexes, sqlstr ):
        ##建立一個陣列，儲存整理好的資料結果
        context = []
        for i in range(len(results)):
            ##建立一個dict，獎每一筆結果轉存成dict的型態
            d = {}
            for j in range(len(columns)):
                d[columns[j]] = results[i][j]
            context.append(d)
        long = len(columns)
     #   z = zip(normal,context)
        sqlstr = sqlstr.replace(" ", "//")
        z = zip(normal, context)
        print("===")
        print(sqlstr)
        return render_template('sortTest.html', scroll = 'results' , context=context, columns=columns, long=long, indexes=indexes, sqlstr=sqlstr, z=z)