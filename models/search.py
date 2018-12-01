import sqlite3
from flask import Flask, request, render_template, flash

class Result():

    def __init__(self):
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    ##欄位名稱
    def get_column_name(self, normal, ckbox, items):
        print(items)
        ##總資料數
        amount = len(ckbox)
        ##取得sqlstr中select的欄位，並以","做分割
        getColumns=['醫院資訊']
        for rr in range(len(items)):
            getColumns.append(items[rr])
        print(getColumns)
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
        return render_template('searchArea.html', normal=normal, ck_len=ck_len, context=context, columns=columns, z=z)

class Select():

    def __init__(self):
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    ##取得醫院的基本資訊
    def get_normal(self, sql_where, items):
        sql_where = sql_where.replace("//", " ")
        ##select醫院的基本資料：名字、分數＆星等、正向評論數、中立評論數、負向評論數、電話與地址並存入normal[]
        sqlstr = "SELECT id, name, type, address FROM hospitals h" + sql_where
        normal = self.cursor.execute(sqlstr).fetchall()
        ##若未找到任何資料，出現錯誤訊息，若有則進入else
        if normal == []:
            flash('抱歉，找不到您要的資料訊息。')
            return render_template("searchArea.html")
        else:
            return Select().get_checkbox(normal, items, sql_where)

    def get_checkbox(self, normal, items, sql_where):
        s = 'm.hospital_id'
        for rr in range(len(items)):
            s += (', ' + items[rr])
        sqlstr = "SELECT "+s+" FROM merge_data m JOIN hospitals h ON m.hospital_id = h.id" + sql_where
        ckbox = self.cursor.execute(sqlstr).fetchall()
        return Result().get_column_name(normal, ckbox, items)

class CheckBox():
    def __init__(self):
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    def print_ckbox(self, sql_where):
        fetch = self.cursor.execute("SELECT name FROM indexes").fetchall()
        ckboxList = []
        ckboxNum = []
        for j in range(33):
            ckboxList.append(fetch[j][0])
            ckboxNum.append(j + 1)
        z_ckbox = zip(ckboxNum, ckboxList)
        return render_template('searchArea.html', scroll='checkBox', sql_where=sql_where, ckboxList=ckboxList, z_ckbox=z_ckbox)

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
        sql_where = " WHERE h.address LIKE '" + area + "%'"
        sql_where = sql_where.replace(" ", "//")
        return CheckBox().print_ckbox(sql_where)

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
    def search_type(self, types):
        t = {
            '1': "醫學中心",
            '2': "區域醫院",
            '3': "地區醫院",
            '4': "診所"
        }
        t_str = ' WHERE'
        for type in types:
            t_str += " h.type = '" + t.get(type) + "' OR"
        sql_where = t_str[:-3]
        return Select().get_normal(sql_where, items)
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
                9: ", m.m_28, m.m_29",
                10: ", mr.better, mr.normal, mr.worse"
            }
            for keyword in keywords:
                if keyword != "":
                    getId = self.cursor.execute("SELECT id FROM category WHERE name = '" + keyword + "'")
                    keyId = getId.fetchone()[0]
                    substr += getStr.get(keyId)
            sqlstr = "SELECT h.id, h.name" + substr + " FROM hospitals h JOIN merge_data m ON h.id = m.hospital_id JOIN merge_reviews mr ON h.id = mr.hospital_id"
            results = self.cursor.execute(sqlstr).fetchall()  ##執行sqlstr，並列出所有結果到results[]
            return Result().get_column_name(results, sqlstr)
        except:
            flash('抱歉，找不到您要的「{}」相關資訊。'.format(keyword))
            return render_template("searchArea.html")

    def search_name(self, names, items):
        n_str = ' WHERE'
        for name in names:
            if name != "":
                n_str += (" h.name LIKE '%" + name + "%' OR h.abbreviation LIKE '%" + name + "%' OR")
        print(n_str)
        sql_where = n_str[:-3]
        return Select().get_normal(sql_where, items)
