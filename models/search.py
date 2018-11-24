import sqlite3
from flask import Flask, request, render_template, flash

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
            print('fetch')
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
            return render_template("searchArea.html")
        else:
            return Result().get_column_name(results, sqlstr)

    ##特殊疾病搜尋
    def search_disease(self, disease):
        try:
            getId = self.cursor.execute("SELECT id FROM diseases WHERE (name LIKE '%" + disease + "%' OR eng_name LIKE '%" + disease + "%')")
            diseaseId = (getId.fetchone()[0])
            getStr = {
                1: "m.m_1, m.m_2, m.m_3, m.m_4, m.m_5",
                2: "m.m_6, m.m_7, m.m_8, m.m_9, m.m_10, m.m_11",
                3: "m.m_12, m.m_13, m.m_14, m.m_15",
                4: "m.m_16, m.m_17, m.m_18",
                5: "m.m_19, m.m_20, m.m_21, m.m_22",
                6: "m.m_23, m.m_24, m.m_25, m.m_26, m.m_27",
                7: "m.m_28, m.m_29, m.m_30, m.m_31",
                8: "m.m_32, m.m_33"
            }
            sqlstr = "SELECT h.id, h.name, " + getStr.get(diseaseId) + " FROM hospitals h JOIN merge_data m ON h.id = m.hospital_id"
            results = self.cursor.execute(sqlstr).fetchall()  ##執行sqlstr，並列出所有結果到results[]
            return Result().get_column_name(results, sqlstr)
        except:
            flash('抱歉，找不到您要的「{}」相關資訊。目前只有8個疾病相關的資訊，包括：氣喘疾病(Asthma)、急性心肌梗塞疾病(AMI)、糖尿病(DM，Diabetes)、人工膝關節手術(TKR，Total Knee Replace)、腦中風(Stroke)、鼻竇炎(Sinusitis)、子宮肌瘤手術(Myoma)、消化性潰瘍疾病(Ulcer)。'.format(disease))
            return render_template("searchArea.html")

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
            getStr = {
                1: ", m.m_3, m.m_6, m.m_7, m.m_10, m.m_11, m.m_20, m.m_21, m.m_22, m.m_23, m.m_24, m.m_26, m.m_27, m.m_32, m.m_33",
                2: ", m.m_12, m.m_13, m.m_14, m.m_15, m.m_25",
                3: ", m.m_30",
                4: ", m.m_1",
                5: ", m.m_2, m.m_4, m.m_8, m.m_18, m.m_31",
                6: ", m.m_5, m.m_9",
                7: ", m.m_16, m.m_17",
                8: ", m.m_19",
                9: ", m.m_28, m.m_29"
            }
            for keyword in keywords:
                if keyword != "":
                    getId = self.cursor.execute("SELECT id FROM category WHERE name = '" + keyword + "'")
                    keyId = getId.fetchone()[0]
                    substr += getStr.get(keyId)
            sqlstr = "SELECT h.id, h.name" + substr + " FROM hospitals h JOIN merge_data m ON h.id = m.hospital_id"
            results = self.cursor.execute(sqlstr).fetchall()  ##執行sqlstr，並列出所有結果到results[]
            return Result().get_column_name(results, sqlstr)
        except:
            flash('抱歉，找不到您要的「{}」相關資訊。'.format(keyword))
            return render_template("searchArea.html")

    def search_name(self, names):
        results = []
        for name in names:
            if name != "":
                sqlstr = "SELECT h.id, h.name, h.type, h.address FROM hospitals h WHERE h.name LIKE '%" + name + "%'"
                results += self.cursor.execute(sqlstr).fetchall()  ##執行sqlstr，並列出所有結果到results[]
        return Result().get_column_name(results, sqlstr)
