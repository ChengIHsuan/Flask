import sqlite3
from flask import Flask, request, render_template, flash
import numpy as np

class Result():

    def __init__(self):
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    ##欄位名稱
    def get_column_name(self, results, sqlstr):
        amount = len(results)
        ##取得sqlstr中select的欄位，並以","做分割
        s = sqlstr.index("FROM") - 1
        getColumns = (sqlstr[7:s]).split(', ')
        ##取得欄位名稱
        columns = []
        for c in getColumns:
            col = self.cursor.execute("SELECT abbreviation FROM column_name WHERE name = '" + c + "'").fetchone()[0]
            columns.append(col)
        return Result().table(results, amount, columns)

    ##將搜尋結果寫進表格，需傳入(numpy array,總資料數,欄位名稱)
    def table(self, results, amount, columns):
        ##建立一個陣列，儲存整理好的資料結果
        context = []
        for i in range(len(results)):
            ##建立一個dict，獎每一筆結果轉存成dict的型態
            d = {}
            for j in range(len(columns)):
                d[columns[j]] = results[i][j]
            context.append(d)
        long = len(columns)
        return render_template('searchArea.html', scroll= 'results' ,context=context, columns=columns, long=long)


class Search():

    def __init__(self):
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    ##地點搜尋
    def search_area(self, county, township):
        ##若使用者輸入臺北，將會出現臺北及新北資料
        i = county.find('臺北')
        ##判斷使用者是否在縣市欄位輸入"臺北"，等於-1時為未找到"臺北"
        if i != -1:
            area = str("_北%" + township)
        else:
            area = str(county + '%' + township)
        sqlstr = "SELECT h.id, h.name, h.type, h.address FROM hospitals h WHERE address LIKE '" + area + "%'"
        results = self.cursor.execute(sqlstr).fetchall()  ##執行sqlstr，並列出所有結果到results[]
        ##若未找到任何資料，出現錯誤訊息，若有則進入else
        if results == []:
            flash('抱歉，找不到您要的資料訊息。')
            return render_template("hospital.html")
        else:
            return Result().get_column_name(results, sqlstr)

    ##特殊疾病搜尋
    def search_disease(self, disease):
        ##判斷使用者輸入的疾病ID
        getId = self.cursor.execute("SELECT id FROM diseases WHERE (name LIKE '%" + disease + "%' OR eng_name LIKE '%" + disease + "%')")
        diseaseId = (getId.fetchone()[0])

        index_range = {
            1: range(1, 6),
            2: range(6, 12),
            3: range(12, 16),
            4: range(16, 19),
            5: range(19, 23),
            6: range(23, 28),
            7: range(28, 32),
            8: range(32, 34)
        }

        sqlstr = "SELECT id, name FROM hospitals"
        results = self.cursor.execute(sqlstr).fetchall()  ##執行sqlstr，並列出所有結果到results[]
        amount = len(results)
        length = 2
        for index in index_range.get(diseaseId):
            length += 1
            sql = "select hospital_id, value || ' (分母：' || denominator || ')' from data where index_id = " + str(index)
            deno = self.cursor.execute(sql).fetchall()
            for j in range(0, amount):  ##7134
                for i in range(0, len(deno)):  ##800
                    if results[j][0] == deno[i][0]:
                        results[j] += (deno[i][1],)
                if len(results[j]) < length:
                    results[j] += "無相關資料",

        ##取得欄位名稱
        columns = []
        columns.append("醫院ID")
        columns.append("醫院名稱")
        for r in index_range.get(diseaseId):
            col = self.cursor.execute("SELECT abbreviation FROM indexes WHERE id = " + str(r)).fetchone()[0]
            columns.append(col)

        return Result().table(results, amount, columns)

        # try:
        #     getId = self.cursor.execute("SELECT id FROM diseases WHERE (name LIKE '%" + disease + "%' OR eng_name LIKE '%" + disease + "%')")
        #     diseaseId = (getId.fetchone()[0])
        #     str = {
        #         1: "f.h_1, f.h_2, f.h_3, f.h_4, f.h_5",
        #         2: "f.h_6, f.h_7, f.h_8, f.h_9, f.h_10, f.h_11",
        #         3: "f.h_12, f.h_13, f.h_14, f.h_15",
        #         4: "f.h_16, f.h_17, f.h_18",
        #         5: "f.h_19, f.h_20, f.h_21, f.h_22",
        #         6: "f.h_23, f.h_24, f.h_25, f.h_26, f.h_27",
        #         7: "f.h_28, f.h_29, f.h_30, f.h_31",
        #         8: "f.h_32, f.h_33"  ##substr
        #     }
        #     sqlstr = "SELECT h.id, h.name, " + str.get(diseaseId) + " FROM hospitals h JOIN final_data f ON h.id = f.hospital_id"
        #     # sqlstr = "SELECT h.id, h.name FROM hospitals h JOIN final_data f ON h.id = f.hospital_id"
        #     results = self.cursor.execute(sqlstr).fetchall()  ##執行sqlstr，並列出所有結果到results[]
        #     return Result().get_column_name(results, sqlstr)
        # except:
        #     # flash('抱歉，找不到您要的「{}」相關資訊。目前只有8個疾病相關的資訊，包括：氣喘疾病(Asthma)、急性心肌梗塞疾病(AMI)、糖尿病(DM，Diabetes)、人工膝關節手術(TKR，Total Knee Replace)、腦中風(Stroke)、鼻竇炎(Sinusitis)、子宮肌瘤手術(Myoma)、消化性潰瘍疾病(Ulcer)。'.format(disease))
        #     return render_template("searchArea.html")

    ##醫院層級搜尋
    def search_type(self, type):

        t = {
            '1': "醫學中心",
            '2': "區域醫院",
            '3': "地區醫院",
            '4': "診所"
        }
        sqlstr = "SELECT h.id, h.name, h.type, h.address FROM hospitals h WHERE type = '" + t.get(type) + "'"
        results = self.cursor.execute(sqlstr).fetchall()
        return Result().get_column_name(results, sqlstr)

    ##分類主題搜尋
    def search_category(self, keywords):
        try:
            substr = ''
            str = {
                1: ", f.h_3, f.h_6, f.h_7, f.h_10, f.h_11, f.h_20, f.h_21, f.h_22, f.h_23, f.h_24, f.h_26, f.h_27, f.h_32, f.h_33",
                2: ", f.h_12, f.h_13, f.h_14, f.h_15, f.h_25",
                3: ", f.h_30",
                4: ", f.h_1",
                5: ", f.h_2, f.h_4, f.h_8, f.h_18, f.h_31",
                6: ", f.h_5, f.h_9",
                7: ", f.h_16, f.h_17",
                8: ", f.h_19",
                9: ", f.h_28, f.h_29"
            }
            for keyword in keywords:
                if keyword != "":
                    getId = self.cursor.execute("SELECT id FROM category WHERE name = '" + keyword + "'")
                    keyId = getId.fetchone()[0]
                    substr += str.get(keyId)
            sqlstr = "SELECT h.name" + substr + " FROM hospitals h JOIN final_data f ON h.id = f.hospital_id"
            results = self.cursor.execute(sqlstr).fetchall()  ##執行sqlstr，並列出所有結果到results[]
            return Result().get_column_name(results, sqlstr)
        except:
            flash('抱歉，找不到您要的「{}」相關資訊。'.format(keyword))
            return render_template("hospital.html")

    def search_name(self, names):
        results = []
        for name in names:
            if name != "":
                sqlstr = "SELECT h.id, h.name, h.type, h.address FROM hospitals h WHERE h.name LIKE '%" + name + "%'"
                results += self.cursor.execute(sqlstr).fetchall()  ##執行sqlstr，並列出所有結果到results[]
        return Result().get_column_name(results, sqlstr)
