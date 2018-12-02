import sqlite3
from flask import Flask, request, render_template, flash

class Search():

    def __init__(self):
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    ## 地點搜尋
    def search_area(self, county, township):
        ## 若使用者輸入臺北，將會出現臺北及新北資料
        i = county.find('臺北')
        ## 判斷使用者是否在縣市欄位輸入"臺北"，等於-1時為未找到"臺北"
        if i != -1:
            area = str("_北%" + township)
        else:
            area = str(county + '%' + township)
        ## 依照使用者在前端輸入的條件寫成SQL字串中的condition
        sql_where = " WHERE h.area LIKE '" + area + "%'"
        test = self.cursor.execute("SELECT * FROM hospitals h " + sql_where).fetchall()
        print(test)
        return CheckBox().print_ckbox(sql_where)

    ## 特殊疾病搜尋
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
            sqlstr = "SELECT h.name, 'GOOGLE分數', '正面評論數：'||mr.better,  '負面評論數：'||mr.worse, '中立評論數：'||mr.normal, '地址電話' FROM hospitals h JOIN merge_reviews mr ON h.id=mr.hospital_id"
            normal = self.cursor.execute(sqlstr).fetchall()
            sqlstr = "SELECT h.id, " + getStr.get(diseaseId) + " FROM hospitals h JOIN merge_data m ON h.id = m.hospital_id"
            ckbox = self.cursor.execute(sqlstr).fetchall()  ##執行sqlstr，並列出所有結果到results[]
            items = getStr.get(diseaseId).split(", ")
            return Result().get_column_name(normal, ckbox, items)
        except:
            flash('抱歉，找不到您要的「{}」相關資訊。目前只有8個疾病相關的資訊，包括：氣喘疾病(Asthma)、急性心肌梗塞疾病(AMI)、糖尿病(DM，Diabetes)、人工膝關節手術(TKR，Total Knee Replace)、腦中風(Stroke)、鼻竇炎(Sinusitis)、子宮肌瘤手術(Myoma)、消化性潰瘍疾病(Ulcer)。'.format(disease))
            return render_template("searchArea.html")

    ## 醫院層級搜尋
    def search_type(self, types):
        ## 建立一個tuple，使前端取回的type值可以對應正確的醫院層級
        t = {
            '1': "醫學中心",
            '2': "區域醫院",
            '3': "地區醫院",
            '4': "診所"
        }
        ## 建立一個SQL語法中condition的開頭字串
        t_str = ' WHERE'
        ## 對應正確的醫院層級後寫入condition字串中
        for type in types:
            t_str += " h.type = '" + t.get(type) + "' OR"
        ## 擷取字串中第一位至倒數第三位(原會以「 OR」結尾)
        sql_where = t_str[:-3]
        return CheckBox().print_ckbox(sql_where)

    ## 分類主題搜尋
    def search_category(self, keywords):

        try:
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
            substr = ''
            for keyword in keywords:
                if keyword != "":
                    getId = self.cursor.execute("SELECT id FROM category WHERE name = '" + keyword + "'")
                    keyId = getId.fetchone()[0]
                    substr += getStr.get(keyId)
            sqlstr = "SELECT h.id" + substr + " FROM hospitals h JOIN merge_data m ON h.id = m.hospital_id"
            results = self.cursor.execute(sqlstr).fetchall()  ##執行sqlstr，並列出所有結果到results[]
            return CheckBox().category_ckbox(substr)
        except:
            print('except_cat')
            flash('抱歉，找不到您要的「{}」相關資訊。'.format(keyword))
            return render_template("searchArea.html")

    ## 醫院名稱搜尋
    def search_name(self, names):
        ## 建立一個SQL語法中condition的開頭字串
        n_str = ' WHERE'
        ## 若前端inputbox不為空，寫入condition字串中，對應全名或是縮寫
        for name in names:
            if name != "":
                n_str += (" h.name LIKE '%" + name + "%' OR h.abbreviation LIKE '%" + name + "%' OR")
        ## 擷取字串中第一位至倒數第三位(原會以「 OR」結尾)
        sql_where = n_str[:-3]
        return CheckBox().print_ckbox(sql_where)

class CheckBox():

    def __init__(self):
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    ## 印出相關的指標供使用者選擇，大部分搜尋方式只需列出33個指標
    def print_ckbox(self, sql_where):
        ## 列出33個指標存入fetch[]，格式為二維陣列，[('指標名稱',), ('指標名稱',)]
        indexes = self.cursor.execute("SELECT id, name FROM indexes").fetchall()
        ## 建立兩個List，一個存放傳至前端checkbox時的value，一個存放checkbox會顯示的名稱
        ckboxNum = []
        ckboxList = []
        for i in range(len(indexes)):
            ckboxNum.append('m.m_' + str(indexes[i][0]))  ##加上'm.m_'方便之後在資料庫搜尋
            ckboxList.append(indexes[i][1])
        ## 用zip()將兩個List打包
        z_ckbox = zip(ckboxNum, ckboxList)
        ## 因為要將condition暫存至前端的隱藏欄位value，因為value不接受空格所以先轉成//
        sql_where = sql_where.replace(" ", "//")
        ##r ender至前端HTML，將condition傳至前端暫存，z_ckbox為checkbox的值和名稱zip
        return render_template('searchArea.html', scroll='checkBox', sql_where=sql_where, z_ckbox=z_ckbox)

    def category_ckbox(self, substr):
        indexes = substr.split(", ")
        del indexes[0]
        ckboxNum = []
        ckboxList = []
        for i in range(len(indexes)):
            ckboxNum.append(indexes[i])
            ckboxList.append(self.cursor.execute("SELECT name FROM indexes WHERE id = " + indexes[i][4:]).fetchone()[0])
            ## 用zip()將兩個List打包
            z_ckbox = zip(ckboxNum, ckboxList)
        return render_template('searchArea.html', scroll='checkBox', sql_where='', z_ckbox=z_ckbox)

class Select():

    def __init__(self):
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    ## 前端按下button後進入的第一個方法
    ## 將暫存在前端的condition、使用者勾選的指標寫成陣列取回
    ## 取得醫院的基本資訊
    def get_normal(self, sql_where, items):
        ## 將condition改回
        sql_where = sql_where.replace("//", " ")
        ## select醫院的基本資料：名字、分數＆星等、正向評論數、中立評論數、負向評論數、電話與地址並存入normal[]
        sqlstr = "SELECT h.name, 'GOOGLE分數', '正面評論數：'||mr.better,  '負面評論數：'||mr.worse, '中立評論數：'||mr.normal, '地址電話' FROM hospitals h JOIN merge_reviews mr ON h.id=mr.hospital_id" + sql_where
        normal = self.cursor.execute(sqlstr).fetchall()
        ## 若未找到任何資料，出現錯誤訊息，若有則進入else
        if normal == []:
            flash('抱歉，找不到您要的資料訊息。')
            return render_template("searchArea.html")
        else:
            return Select().get_checkbox(normal, items, sql_where)

    ## 取得使用者勾選的資訊
    def get_checkbox(self, normal, items, sql_where):
        s = 'm.hospital_id'
        for r in range(len(items)):
            s += (', ' + items[r])
        sqlstr = "SELECT " + s + " FROM merge_data m JOIN hospitals h ON m.hospital_id = h.id" + sql_where
        print(sqlstr)
        ckbox = self.cursor.execute(sqlstr).fetchall()
        return Result().get_column_name(normal, ckbox, items)

class Result():

    def __init__(self):
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    ## 取得欄位名稱
    def get_column_name(self, normal, ckbox, items):
        ## 先取得欄位的原始名字，「醫院資訊」為固定欄位，直接手動新增
        getColumns=['醫院資訊']
        for r in range(len(items)):
            getColumns.append(items[r])
        ## 從資料庫中取得欄位名稱
        columns = []
        for c in getColumns:
            col = self.cursor.execute("SELECT abbreviation FROM column_name WHERE name = '" + c + "'").fetchone()[0]
            columns.append(col)
        return Result().table(normal, ckbox, columns)

    ## 將搜尋結果寫進表格
    def table(self, normal, ckbox, columns):
        ## 選取的指標數量，-1是因為扣掉第一欄的醫院資訊
        ck_len = len(columns) - 1
        ## 建立context[]存放與指標直相關資料
        context = []
        for i in range(len(ckbox)):  #ckbox[][]為Select().get_checkbox()取得的指標值
            ## 建立一個dict，將每一筆結果轉存成dict的型態
            d = {}
            for j in range(ck_len):
                d[columns[j + 1]] = ckbox[i][j + 1]
            context.append(d)
        ## 用zip()，讓兩個List同時進行迭代
        z = zip(normal, context)
        ## render至前端HTML，ck_len為指標的長度，columns為欄位名稱，z為醫院資訊和指標值的zip
        return render_template('searchArea.html', scroll = 'results', ck_len=ck_len, columns=columns, z=z)
