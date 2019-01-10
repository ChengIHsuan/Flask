import sqlite3
from flask import Flask, request, render_template, flash, redirect

class Search():

    def __init__(self):
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    ## 地點搜尋
    def search_area(self, county, township):
        try:
            ## 若使用者輸入臺北，將會出現臺北及新北資料
            i = county.find('臺北')
            ## 判斷使用者是否在縣市欄位輸入"臺北"，等於-1時為未找到"臺北"
            if i != -1:
                area = str("_北%" + township)
            else:
                area = str(county + '%' + township)
            ## 依照使用者在前端輸入的條件寫成SQL字串中的condition
            sql_where = "h.area LIKE '" + area + "%'"
            ## 驗證使用者是否輸入不存在的條件
            validate = self.cursor.execute("SELECT h.id FROM hospitals h WHERE " + sql_where).fetchall()
            if validate == []:
                return "抱歉，找不到您要的「{}{}」相關資訊。".format(county, township)
            else:
                # return CheckBox().print_ckbox(sql_where)
                return sql_where
        except:
            return "抱歉，操作失敗"

    ## 特殊疾病搜尋
    def search_disease(self, diseases):
        try:
            getStr = {
                1: "m.m_2, m.m_3, m.m_41",
                2: "m.m_6, m.m_7, m.m_8, m.m_9, m.m_10, m.m_11, m.m_42",
                3: "m.m_12, m.m_13, m.m_14, m.m_15, m.m_43",
                4: "m.m_16, m.m_17, m.m_18, m.m_44",
                5: "m.m_19, m.m_20, m.m_21, m.m_22, m.m_45",
                6: "m.m_23, m.m_24, m.m_25, m.m_26, m.m_27, m.m_46",
                7: "m.m_28, m.m_29, m.m_30, m.m_31, m.m_47",
                8: "m.m_32, m.m_33, m.m_48",
                9: "m.m_34, m.m_35, m.m_36, m.m_37, m.m_38, m.m_39, m.m_40, m.m_49",
                10: "m.m_38, m.m_39, m.m_40, m.m_50"
            }
            sub_str = ''
            while '' in diseases:
                diseases.remove('')
            for disease in diseases:
                getId = self.cursor.execute("SELECT id FROM diseases WHERE (name LIKE '%" + disease + "%' OR eng_name LIKE '%" + disease + "%')")
                diseaseId = getId.fetchone()[0]
                if disease != diseases[-1]:
                    sub_str += getStr.get(diseaseId) + ', '
                else:
                    sub_str += getStr.get(diseaseId)
            return sub_str
        except:
            return "抱歉，找不到您要的「{}」相關資訊。目前只有8個疾病相關的資訊，包括：氣喘疾病(Asthma)、急性心肌梗塞疾病(AMI)、糖尿病(DM，Diabetes)、人工膝關節手術(TKR，Total Knee Replace)、腦中風(Stroke)、鼻竇炎(Sinusitis)、子宮肌瘤手術(Myoma)、消化性潰瘍疾病(Ulcer)。".format(disease)

    ## 醫院層級搜尋
    def search_type(self, types):
        ## 建立一個tuple，使前端取回的type值可以對應正確的醫院層級
        getStr = {
            '1': "醫學中心",
            '2': "區域醫院",
            '3': "地區醫院",
            '4': "診所"
        }
        ## 建立一個SQL語法中condition的開頭字串
        sql_where = ''
        ## 對應正確的醫院層級後寫入condition字串中
        for type in types:
            ## 判斷若非陣列最後一個元素則不加"OR"
            if type != types[-1]:
                sql_where += "h.type = '" + getStr.get(type) + "' OR "
            else:
                sql_where += "h.type = '" + getStr.get(type) + "'"
        return sql_where

    ## 分類主題搜尋
    def search_category(self, keywords):
        getStr = {
            "1": "m.m_3, m.m_6, m.m_7, m.m_10, m.m_11, m.m_20, m.m_21, m.m_22, m.m_23, m.m_24, m.m_26, m.m_27, m.m_32, m.m_33",
            "2": "m.m_12, m.m_13, m.m_14, m.m_15, m.m_25, m.m_34, m.m_35, m.m_36, m.m_37, m.m_38, m.m_39, m.m_40",
            "3": "m.m_30",
            "4": "",
            "5": "m.m_2, m.m_8, m.m_18, m.m_31",
            "6": "m.m_9",
            "7": "m.m_16, m.m_17",
            "8": "m.m_19",
            "9": "m.m_28, m.m_29",
            "10": "m.m_41, m.m_42, m.m_43, m.m_44, m.m_45, m.m_46, m.m_47, m.m_48, m.m_49"
        }
        sub_str = ''
        ## 移除陣列中的空字串
        while '' in keywords:
            keywords.remove('')
        for keyword in keywords:
            if keyword != keywords[-1]:
                sub_str += getStr.get(keyword) + ', '
            else:
                sub_str += getStr.get(keyword)
        return sub_str

    ## 醫院名稱搜尋
    def search_name(self, names):
        try:
            ## 建立一個SQL語法中condition的開頭字串
            sql_where = ''
            ## 移除陣列中的空字串
            while '' in names:
                names.remove('')
            ## 寫入condition字串中，對應全名或是縮寫
            for name in names:
                ## 判斷若非陣列最後一個元素則不加"OR"
                if name != names[-1]:
                    sql_where += ("h.name LIKE '%" + name + "%' OR h.abbreviation LIKE '%" + name + "%' OR ")
                else:
                    sql_where += ("h.name LIKE '%" + name + "%' OR h.abbreviation LIKE '%" + name + "%'")
                validate = self.cursor.execute("SELECT h.id FROM hospitals h WHERE " + sql_where).fetchall()
                if validate == []:
                    return "抱歉，找不到您要的「{}」相關資訊。".format(name)
            return sql_where
        except:
            return "抱歉，操作失敗"

    ## 評價結果搜尋
    def search_reviews(self, star, positive, negative):
        sql_where = ''
        if star != '':
            sql_where += "fr.star >= " + star + " AND fr.star != 'N/A' AND "
        if positive != '':
            sql_where += "fr.positive >= " + positive + " AND fr.positive != 'N/A' AND "
        if negative != '':
            sql_where += "fr.negative >= " + negative+ " AND "
        sql_where = sql_where[:-4]
        return sql_where

    ## 查詢條件
    def search_filter(self, county, township, diseases, types, keywords, names, star, positive, negative):
        search_filter = "查詢條件："
        ## 地點搜尋
        if county+township != '':
            search_filter += (county+township) + ', '
        ## 特疾搜尋
        while '' in diseases:
            diseases.remove('')
        for disease in diseases:
            search_filter += disease + ', '
        ## 層級搜尋
        for type in types:
            getStr = {
                '1': "醫學中心",
                '2': "區域醫院",
                '3': "地區醫院",
                '4': "診所"
            }
            search_filter += getStr.get(type) + ', '
        ## 分類主題
        for keyword in keywords:
            getStr = {
                '1': "應服藥物",
                '2': "疾病檢查",
                '3': "住院日數",
                '4': "健保費用",
                '5': "再次住院",
                '6': "再次急診",
                '7': "手術感染",
                '8': "中風復健",
                '9': "器官損傷",
                '10': "組合分數"
            }
            search_filter += getStr.get(keyword) + ', '
        ## 名稱搜尋
        while '' in names:
            names.remove('')
        for name in names:
            search_filter += name + ', '
        ## 評價結果
        if star != '':
            search_filter += star + "星以上, "
        if positive != '':
            search_filter += "正面評論大於" + positive + ', '
        if negative != '':
            search_filter += "負面評論小於" + negative + ', '
        search_filter = search_filter[:-2]
        return search_filter

    ## 綜合搜尋
    def search_all(self, county, township, diseases, types, keywords, names, star, positive, negative):
        ## 取得查詢條件
        search_filter = Search().search_filter(county, township, diseases, types, keywords, names, star, positive, negative)
        sql_where = ''
        ## 取得地區搜尋的condition
        area_condition = Search().search_area(county, township)
        ## 若為錯誤訊息，以alert提示
        if area_condition.find('抱歉') != -1:
            return render_template('searchArea.html', alert=area_condition)
        else:
            area_condition = '(' + area_condition + ')'
        ## 取得醫院層級condition
        type_condition = '(' + Search().search_type(types) + ')'
        ## 取得醫院名稱condition
        name_condition = Search().search_name(names)
        ## 若為錯誤訊息，以alert提示
        if name_condition.find('抱歉') != -1:
            return render_template('searchArea.html', alert=name_condition)
        else:
            name_condition = '(' + name_condition + ')'
        ## 取得評價結果condition
        reviews_condition = '(' + Search().search_reviews(star, positive, negative) + ')'

        conditions = [area_condition, type_condition, name_condition, reviews_condition]
        ## 若沒有條件則移除
        while '()' in conditions:
            conditions.remove('()')
        ## 將所有condition相接
        for condition in conditions:
            if condition != '':
                if condition != conditions[-1]:
                    sql_where += condition + "AND "
                else:
                    sql_where +=condition

        disease_select = Search().search_disease(diseases)
        if disease_select.find('抱歉') != -1:
            return render_template('searchArea.html', alert=disease_select)
        category_select = Search().search_category(keywords)
        if category_select.find('抱歉') != -1:
            return render_template('searchArea.html', alert=category_select)
        disease_indexes = disease_select.split(", ")
        category_indexes = category_select.split(", ")
        both_indexes = []
        for index in disease_indexes:
            if index in category_indexes:
                both_indexes.append(index)

        if category_select != '':   # 有分類主題
            if disease_select != '':   #有分類主題、特疾
                return Ckbox(sql_where, search_filter).print_ckbox(both_indexes)
            else:   # 有分類主題沒有特疾
                return Ckbox(sql_where, search_filter).print_ckbox(category_indexes)
        else:   ##沒有分類主題
            if disease_select != '':  # 沒有分類主題有特疾
                return Ckbox(sql_where, search_filter).print_ckbox(disease_indexes)
            else:  # 都沒有
                return Ckbox(sql_where, search_filter).print_ckbox('')

class Ckbox():
    def __init__(self, sql_where, search_filter):
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()
        if sql_where != '':
            self.sql_where = ' WHERE ' + sql_where
        self.search_filter = search_filter

    def print_ckbox(self, indexes):
        try:
            ## 建立兩個list存放checkbox的value和指標名稱
            ckboxVal_1=[]
            ckboxVal_2=[]
            ckboxVal_3=[]
            ckboxVal_4=[]
            ckboxVal_5=[]
            ckboxVal_6=[]
            ckboxVal_7=[]
            ckboxVal_8=[]
            ckboxVal_9=[]
            ckboxVal_10 = []
            ckboxName_1=[]
            ckboxName_2=[]
            ckboxName_3=[]
            ckboxName_4=[]
            ckboxName_5=[]
            ckboxName_6=[]
            ckboxName_7=[]
            ckboxName_8=[]
            ckboxName_9=[]
            ckboxName_10 = []
            ## 若條件indexes == ''表示沒搜尋特殊疾病和分類主題，直接列出所有指標
            if indexes == '':
                all_indexes = self.cursor.execute("SELECT id, abbreviation, parent_id FROM indexes WHERE id != 1 AND id != 4 AND id != 5").fetchall()
                for i in range(len(all_indexes)):
                    if all_indexes[i][2] == 1:
                        ckboxVal_1.append('m.m_' + str(all_indexes[i][0]))  ##加上'm.m_'方便之後在資料庫搜尋
                        ckboxName_1.append(all_indexes[i][1])
                    if all_indexes[i][2] == 2:
                        ckboxVal_2.append('m.m_' + str(all_indexes[i][0]))  ##加上'm.m_'方便之後在資料庫搜尋
                        ckboxName_2.append(all_indexes[i][1])
                    if all_indexes[i][2] == 3:
                        ckboxVal_3.append('m.m_' + str(all_indexes[i][0]))  ##加上'm.m_'方便之後在資料庫搜尋
                        ckboxName_3.append(all_indexes[i][1])
                    if all_indexes[i][2] == 4:
                        ckboxVal_4.append('m.m_' + str(all_indexes[i][0]))  ##加上'm.m_'方便之後在資料庫搜尋
                        ckboxName_4.append(all_indexes[i][1])
                    if all_indexes[i][2] == 5:
                        ckboxVal_5.append('m.m_' + str(all_indexes[i][0]))  ##加上'm.m_'方便之後在資料庫搜尋
                        ckboxName_5.append(all_indexes[i][1])
                    if all_indexes[i][2] == 6:
                        ckboxVal_6.append('m.m_' + str(all_indexes[i][0]))  ##加上'm.m_'方便之後在資料庫搜尋
                        ckboxName_6.append(all_indexes[i][1])
                    if all_indexes[i][2] == 7:
                        ckboxVal_7.append('m.m_' + str(all_indexes[i][0]))  ##加上'm.m_'方便之後在資料庫搜尋
                        ckboxName_7.append(all_indexes[i][1])
                    if all_indexes[i][2] == 8:
                        ckboxVal_8.append('m.m_' + str(all_indexes[i][0]))  ##加上'm.m_'方便之後在資料庫搜尋
                        ckboxName_8.append(all_indexes[i][1])
                    if all_indexes[i][2] == 9:
                        ckboxVal_9.append('m.m_' + str(all_indexes[i][0]))  ##加上'm.m_'方便之後在資料庫搜尋
                        ckboxName_9.append(all_indexes[i][1])
                    if all_indexes[i][2] == 10:
                        ckboxVal_10.append('m.m_' + str(all_indexes[i][0]))  ##加上'm.m_'方便之後在資料庫搜尋
                        ckboxName_10.append(all_indexes[i][1])
            else:
                for i in range(len(indexes)):
                    spe_index = self.cursor.execute("SELECT abbreviation, parent_id FROM indexes WHERE id = " + indexes[i][4:]).fetchone()
                    if spe_index[1] == 1:
                        ckboxVal_1.append(indexes[i])
                        ckboxName_1.append(spe_index[0])
                    if spe_index[1] == 2:
                        ckboxVal_2.append(indexes[i])
                        ckboxName_2.append(spe_index[0])
                    if spe_index[1] == 3:
                        ckboxVal_3.append(indexes[i])
                        ckboxName_3.append(spe_index[0])
                    if spe_index[1] == 4:
                        ckboxVal_4.append(indexes[i])
                        ckboxName_4.append(spe_index[0])
                    if spe_index[1] == 5:
                        ckboxVal_5.append(indexes[i])
                        ckboxName_5.append(spe_index[0])
                    if spe_index[1] == 6:
                        ckboxVal_6.append(indexes[i])
                        ckboxName_6.append(spe_index[0])
                    if spe_index[1] == 7:
                        ckboxVal_7.append(indexes[i])
                        ckboxName_7.append(spe_index[0])
                    if spe_index[1] == 8:
                        ckboxVal_8.append(indexes[i])
                        ckboxName_8.append(spe_index[0])
                    if spe_index[1] == 9:
                        ckboxVal_9.append(indexes[i])
                        ckboxName_9.append(spe_index[0])
                    if spe_index[1] == 10:
                        ckboxVal_10.append(indexes[i])
                        ckboxName_10.append(spe_index[0])
            ## 用zip方法，將兩個list包在一起
            z_ckbox1 = zip(ckboxVal_1, ckboxName_1)
            z_ckbox2 = zip(ckboxVal_2, ckboxName_2)
            z_ckbox3 = zip(ckboxVal_3, ckboxName_3)
            z_ckbox4 = zip(ckboxVal_4, ckboxName_4)
            z_ckbox5 = zip(ckboxVal_5, ckboxName_5)
            z_ckbox6 = zip(ckboxVal_6, ckboxName_6)
            z_ckbox7 = zip(ckboxVal_7, ckboxName_7)
            z_ckbox8 = zip(ckboxVal_8, ckboxName_8)
            z_ckbox9 = zip(ckboxVal_9, ckboxName_9)
            z_ckbox10 = zip(ckboxVal_10, ckboxName_10)
            ## 將sql_where傳至前端暫存，value不接受空格，因此將空格以//取代
            sql_where = self.sql_where.replace(' ', '//')

            if ckboxName_1==[] and ckboxName_2==[] and ckboxName_3==[] and ckboxName_4==[] and ckboxName_5==[] and ckboxName_6==[] and ckboxName_7==[] and ckboxName_8==[] and ckboxName_9==[] and ckboxName_10==[]:
                flash('無相關指標。')
                return render_template('searchArea.html', scroll='checkBox')
            else:
                return render_template('searchArea.html', scroll='checkBox', sql_where=sql_where, tmp_filter=self.search_filter, z_ckbox1=z_ckbox1, z_ckbox2=z_ckbox2, z_ckbox3=z_ckbox3, z_ckbox4=z_ckbox4, z_ckbox5=z_ckbox5, z_ckbox6=z_ckbox6, z_ckbox7=z_ckbox7, z_ckbox8=z_ckbox8, z_ckbox9=z_ckbox9, z_ckbox10=z_ckbox10)
        except:
            alert = "綜合搜尋查詢錯誤。"
            return render_template("searchArea.html", alert=alert)

class Select():

    def __init__(self):
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    ## 前端按下button後進入的第一個方法
    ## 將暫存在前端的condition、使用者勾選的指標寫成陣列取回
    ## 取得醫院的基本資訊
    def select_normal(self, sql_where, items, search_filter):
        ## 將condition改回
        sql_where = sql_where.replace("//", " ")
        ## select醫院的基本資料：名字、分數＆星等、正向評論數、中立評論數、負向評論數、電話與地址並存入normal[]
        sqlstr = "SELECT h.abbreviation, fr.star, fr.positive,  fr.negative, h.phone, h.address, cast(fr.star as float) FROM merge_data m JOIN hospitals h ON m.hospital_id = h.id JOIN final_reviews fr ON h.id = fr.hospital_id  " + sql_where
        normal = self.cursor.execute(sqlstr).fetchall()
        ## 若未找到任何資料，出現錯誤訊息，若有則進入else
        if normal == []:
            alert = "抱歉，找不到您要的資料訊息。"
            return render_template("searchArea.html", alert=alert)
        else:
            return Select().select_data(normal, items, sql_where, search_filter)

    ## 取得使用者勾選的資訊
    def select_data(self, normal, items, sql_where, search_filter):
        deno_substr = 'm.hospital_id'
        level_substr = 'm.hospital_id'
        value_substr = 'm.hospital_id'
        for r in range(len(items)):
            deno_substr += (', ' + items[r])
            level = items[r].replace('m.m_', 'm.l_')
            level_substr += (', ' + level)
            value = items[r].replace('m.m_', 'm.v_')
            value_substr += (', ' + value)
        ## 取得data分母(就醫人數)
        sqlstr = "SELECT " + deno_substr + " FROM merge_data m JOIN hospitals h ON m.hospital_id = h.id JOIN final_reviews fr ON h.id = fr.hospital_id " + sql_where
        l_deno = self.cursor.execute(sqlstr).fetchall()
        ## 取得data指標值等級
        sqlstr = "SELECT " + level_substr + " FROM merge_data m JOIN hospitals h ON m.hospital_id = h.id JOIN final_reviews fr ON h.id = fr.hospital_id " + sql_where
        l_level = self.cursor.execute(sqlstr).fetchall()
        ## 取得data指標值
        sqlstr = "SELECT " + value_substr + " FROM merge_data m JOIN hospitals h ON m.hospital_id = h.id JOIN final_reviews fr ON h.id = fr.hospital_id " + sql_where
        l_value = self.cursor.execute(sqlstr).fetchall()
        return Result().get_column_name(normal, items, l_deno, l_level, l_value, search_filter, sql_where)

class Result():

    def __init__(self):
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    ## 取得欄位名稱
    def get_column_name(self, normal, items, l_deno, l_level, l_value, search_filter, sql_where):
        ## 先取得欄位的原始名字(m.m_?)，「醫院機構資訊」為固定欄位，直接手動新增
        getColumns=['醫療機構資訊']
        for r in range(len(items)):
            getColumns.append(items[r])
        ## 建立columns[]，存入從資料庫中取得的欄位名稱(縮寫)
        columns = []
        for c in getColumns:
            columns.append(self.cursor.execute("SELECT abbreviation FROM column_name WHERE name = '" + c + "'").fetchone()[0])
        ## 建立full_name[]，存入欄位名稱(縮寫)的完整名字
        full_name = ['醫療機構資訊']
        for fn in columns:
            if fn != '醫療機構資訊':
                full_name.append(self.cursor.execute("SELECT name FROM indexes WHERE abbreviation = '" + fn + "'").fetchone()[0])
        indexes = columns[1:]
        return Result().table(normal, columns, full_name, l_deno, l_level, l_value, search_filter, indexes, sql_where, items)

    ## 將搜尋結果寫進表格
    def table(self, normal, columns, full_name, l_deno, l_level, l_value, search_filter, indexes, sql_where, items):
        ## 選取的指標數量，-1是因為扣掉第一欄的醫療機構資訊
        ck_len = len(columns) - 1
        ## 建立deno[]存放分母資料
        deno = []
        for i in range(len(l_deno)):  #ckbox[][]為Select().get_checkbox()取得的指標值
            ## 建立一個dict，將每一筆結果轉存成dict的型態
            d = {}
            for j in range(ck_len):
                d[columns[j]] = l_deno[i][j + 1]
            deno.append(d)
        ## 建立level[]存放等級資料
        level = []
        for i in range(len(l_level)):  # ckbox[][]為Select().get_checkbox()取得的指標值
            ## 建立一個dict，將每一筆結果轉存成dict的型態
            d = {}
            for j in range(ck_len):
                d[columns[j]] = l_level[i][j + 1]
            level.append(d)
        ## 建立value[]存放指標值資料
        value = []
        for i in range(len(l_value)):  # ckbox[][]為Select().get_checkbox()取得的指標值
            ## 建立一個dict，將每一筆結果轉存成dict的型態
            d = {}
            for j in range(ck_len):
                d[columns[j]] = l_value[i][j + 1]
            value.append(d)
        ## 用zip()，讓多個List同時進行迭代
        z_col = zip(columns, full_name)
        z = zip(normal, deno, level, value)
        print(len(normal))
        print(normal[-1])
        print(len(deno))
        print(len(value))
        print(len(level))
        item = ''
        for r in range(len(items)):
            item += items[r]+'//'
        sql_where = sql_where.replace(' ', '//')
        search_filter2 = search_filter.replace(' ', '//')
        ## render至前端HTML，ck_len為指標的長度，columns為欄位名稱，z為醫院資訊和指標值的zip
        return render_template('searchArea.html', scroll = 'results', ck_len=ck_len, z_col=z_col, z=z, columns=columns, filter=search_filter, search_filter2=search_filter2, indexes=indexes, sql_where=sql_where, item=item)