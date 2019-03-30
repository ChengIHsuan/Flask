import sqlite3
from flask import Flask, request, render_template, flash, redirect

class Search():

    def __init__(self):
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    ## 地點搜尋
    def search_area(self, county, township):
        try:
            area = county + township
            ## 依照使用者在前端輸入的條件寫成SQL字串中的condition
            sql_where = "h.area LIKE '%" + area + "%'"
            ## 驗證使用者是否輸入不存在的條件
            validate = self.cursor.execute("SELECT h.id FROM hospitals h WHERE " + sql_where).fetchall()
            if validate == []:
                return "抱歉，找不到您要的「{}{}」相關資訊。".format(county, township)
            else:
                return sql_where
        except:
            return "抱歉，操作失敗。"

    ## 特殊疾病搜尋
    def search_disease(self, disease):
        try:
            ## 取得各疾病名稱
            getStr = {
                '1': "氣喘",
                '2': "急性心肌梗塞",
                '3': "糖尿病",
                '4': "人工膝關節手術",
                '5': "腦中風",
                '6': "鼻竇炎",
                '7': "子宮肌瘤手術",
                '8': "消化性潰瘍",
                '9': "血液透析",
                '10': "腹膜透析"
            }
            return getStr.get(disease)
        except:
            return "抱歉，操作失敗。"

    # ## 特殊疾病指標
    # def search_index(self, indexes):
    #     for index in indexes:
    #         index = 'f.v_'

    ## 醫院層級搜尋
    def search_type(self, types):
        try:
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
                ## 判斷若非陣列最後一個元素則加"OR"
                if type != types[-1]:
                    sql_where += "h.type = '" + getStr.get(type) + "' OR "
                else:
                    sql_where += "h.type = '" + getStr.get(type) + "'"
            return sql_where
        except:
            return "抱歉，操作失敗。"

    ## 醫院名稱搜尋
    def search_name(self, names):
        try:
            ## 建立一個SQL語法中condition的開頭字串
            sql_where = ''
            ## 寫入condition字串中，對應全名或是縮寫
            for name in names:
                ## 檢查使用者輸入之名稱是否存在
                validate = self.cursor.execute("SELECT h.id FROM hospitals h WHERE h.name LIKE '%" + name + "%' OR h.abbreviation LIKE '%" + name + "%'").fetchall()
                if validate == []:
                    return "抱歉，找不到您要的「{}」相關資訊。".format(name)
                else:
                    ## 判斷若非陣列最後一個元素則加"OR"
                    if name != names[-1]:
                        sql_where += ("h.name LIKE '%" + name + "%' OR h.abbreviation LIKE '%" + name + "%' OR ")
                    else:
                        sql_where += ("h.name LIKE '%" + name + "%' OR h.abbreviation LIKE '%" + name + "%'")
            return sql_where
        except:
            return "抱歉，操作失敗"

    ## 評價結果搜尋
    def search_reviews(self, star):
        sql_where = ''
        if star != '':
            sql_where += "fr.star >= " + star + " AND fr.star != 'N/A' "
        # if positive != '':
        #     sql_where += "fr.positive >= " + positive + " AND fr.positive != 'N/A' AND "
        # if negative != '':
        #     sql_where += "fr.negative <= " + negative+ " AND "
        # sql_where = sql_where[:-4]
        return sql_where

    ## 查詢條件
    def search_filter(self, county, township, disease, types, names, star):
        search_filter = "查詢條件："
        ## 地點搜尋
        if county+township != '':
            search_filter += (county+township) + ', '
        ## 特疾搜尋
        diseaseStr = {
            '1': "氣喘",
            '2': "急性心肌梗塞",
            '3': "糖尿病",
            '4': "人工膝關節手術",
            '5': "腦中風",
            '6': "鼻竇炎",
            '7': "子宮肌瘤手術",
            '8': "消化性潰瘍",
            '9': "血液透析",
            '10': "腹膜透析"
        }
        search_filter += diseaseStr.get(disease) + ', '
        ## 層級搜尋
        for type in types:
            getStr = {
                '1': "醫學中心",
                '2': "區域醫院",
                '3': "地區醫院",
                '4': "診所"
            }
            search_filter += getStr.get(type) + ', '
        ## 名稱搜尋
        for name in names:
            search_filter += name + ', '
        ## 評價結果
        if star != '':
            search_filter += star + "星以上, "
        ## 判斷是否有查詢條件，因為每個條件皆是以", "做結尾，因此不取查詢條件最後兩個位子
        if search_filter != "查詢條件：":
            search_filter = search_filter[:-2]
        else:
            search_filter = "無查詢條件"
        return search_filter

    ## 綜合搜尋
    def search_all(self, county, township, disease, types, names, star, indexes):
        ## 取得查詢條件
        search_filter = Search().search_filter(county, township, disease, types, names, star)
        ##########
        sql_where = ''
        ## 取得地區的condition
        area_condition = Search().search_area(county, township)
        if area_condition.find('抱歉') != -1:     #若為錯誤訊息，以alert提示#
            return render_template('search.html', alert=area_condition)
        else:
            area_condition = '(' + area_condition + ')'
        ## 取得醫院層級condition
        type_condition = '(' + Search().search_type(types) + ')'
        ## 取得醫院名稱condition
        name_condition = Search().search_name(names)
        if name_condition.find('抱歉') != -1:     #若為錯誤訊息，以alert提示#
            return render_template('search.html', alert=name_condition)
        else:
            name_condition = '(' + name_condition + ')'
        ## 取得評價結果condition
        reviews_condition = '(' + Search().search_reviews(star) + ')'

        conditions = [area_condition, type_condition, name_condition, reviews_condition]
        ## 若沒有條件則移除
        while '()' in conditions:
            conditions.remove('()')
        ## 將所有condition相接
        for condition in conditions:
            if condition != conditions[-1]:
                sql_where += condition + "AND "
            else:
                sql_where +=condition

        if sql_where != '':
            sql_where = 'WHERE ' + sql_where
        return Select().add_sql_where(indexes, sql_where, search_filter)

# class Ckbox():
#     def __init__(self, sql_where, search_filter):
#         db = sqlite3.connect('voyager.db')
#         self.cursor = db.cursor()
#         if sql_where != '':
#             self.sql_where = ' WHERE ' + sql_where
#         self.search_filter = search_filter
#
#     def print_ckbox(self, indexes):
#         try:
#             ## 建立兩個list存放checkbox的value和指標名稱
#             ckboxVal_1=[]
#             ckboxVal_2=[]
#             ckboxVal_3=[]
#             ckboxVal_4=[]
#             ckboxVal_5=[]
#             ckboxVal_6=[]
#             ckboxVal_7=[]
#             ckboxVal_8=[]
#             ckboxVal_9=[]
#             ckboxVal_10 = []
#             ckboxName_1=[]
#             ckboxName_2=[]
#             ckboxName_3=[]
#             ckboxName_4=[]
#             ckboxName_5=[]
#             ckboxName_6=[]
#             ckboxName_7=[]
#             ckboxName_8=[]
#             ckboxName_9=[]
#             ckboxName_10 = []
#             ## 若條件indexes == ''表示沒搜尋特殊疾病和分類主題，直接列出所有指標
#             if indexes == '':
#                 all_indexes = self.cursor.execute("SELECT id, abbreviation, parent_id FROM indexes WHERE id != 1 AND id != 4 AND id != 5").fetchall()
#                 for i in range(len(all_indexes)):
#                     if all_indexes[i][2] == 1:
#                         ckboxVal_1.append('m.v_' + str(all_indexes[i][0]))  ##加上'm.v_'方便之後在資料庫搜尋
#                         ckboxName_1.append(all_indexes[i][1])
#                     if all_indexes[i][2] == 2:
#                         ckboxVal_2.append('m.v_' + str(all_indexes[i][0]))  ##加上'm.v_'方便之後在資料庫搜尋
#                         ckboxName_2.append(all_indexes[i][1])
#                     if all_indexes[i][2] == 3:
#                         ckboxVal_3.append('m.v_' + str(all_indexes[i][0]))  ##加上'm.v_'方便之後在資料庫搜尋
#                         ckboxName_3.append(all_indexes[i][1])
#                     if all_indexes[i][2] == 4:
#                         ckboxVal_4.append('m.v_' + str(all_indexes[i][0]))  ##加上'm.v_'方便之後在資料庫搜尋
#                         ckboxName_4.append(all_indexes[i][1])
#                     if all_indexes[i][2] == 5:
#                         ckboxVal_5.append('m.v_' + str(all_indexes[i][0]))  ##加上'm.v_'方便之後在資料庫搜尋
#                         ckboxName_5.append(all_indexes[i][1])
#                     if all_indexes[i][2] == 6:
#                         ckboxVal_6.append('m.v_' + str(all_indexes[i][0]))  ##加上'm.v_'方便之後在資料庫搜尋
#                         ckboxName_6.append(all_indexes[i][1])
#                     if all_indexes[i][2] == 7:
#                         ckboxVal_7.append('m.v_' + str(all_indexes[i][0]))  ##加上'm.v_'方便之後在資料庫搜尋
#                         ckboxName_7.append(all_indexes[i][1])
#                     if all_indexes[i][2] == 8:
#                         ckboxVal_8.append('m.v_' + str(all_indexes[i][0]))  ##加上'm.v_'方便之後在資料庫搜尋
#                         ckboxName_8.append(all_indexes[i][1])
#                     if all_indexes[i][2] == 9:
#                         ckboxVal_9.append('m.v_' + str(all_indexes[i][0]))  ##加上'm.v_'方便之後在資料庫搜尋
#                         ckboxName_9.append(all_indexes[i][1])
#                     if all_indexes[i][2] == 10:
#                         ckboxVal_10.append('m.v_' + str(all_indexes[i][0]))  ##加上'm.v_'方便之後在資料庫搜尋
#                         ckboxName_10.append(all_indexes[i][1])
#             else:
#                 for i in range(len(indexes)):
#                     spe_index = self.cursor.execute("SELECT abbreviation, parent_id FROM indexes WHERE id = " + indexes[i][4:]).fetchone()
#                     if spe_index[1] == 1:
#                         ckboxVal_1.append(indexes[i])
#                         ckboxName_1.append(spe_index[0])
#                     if spe_index[1] == 2:
#                         ckboxVal_2.append(indexes[i])
#                         ckboxName_2.append(spe_index[0])
#                     if spe_index[1] == 3:
#                         ckboxVal_3.append(indexes[i])
#                         ckboxName_3.append(spe_index[0])
#                     if spe_index[1] == 4:
#                         ckboxVal_4.append(indexes[i])
#                         ckboxName_4.append(spe_index[0])
#                     if spe_index[1] == 5:
#                         ckboxVal_5.append(indexes[i])
#                         ckboxName_5.append(spe_index[0])
#                     if spe_index[1] == 6:
#                         ckboxVal_6.append(indexes[i])
#                         ckboxName_6.append(spe_index[0])
#                     if spe_index[1] == 7:
#                         ckboxVal_7.append(indexes[i])
#                         ckboxName_7.append(spe_index[0])
#                     if spe_index[1] == 8:
#                         ckboxVal_8.append(indexes[i])
#                         ckboxName_8.append(spe_index[0])
#                     if spe_index[1] == 9:
#                         ckboxVal_9.append(indexes[i])
#                         ckboxName_9.append(spe_index[0])
#                     if spe_index[1] == 10:
#                         ckboxVal_10.append(indexes[i])
#                         ckboxName_10.append(spe_index[0])
#             ## 用zip方法，將兩個list包在一起
#             z_ckbox1 = zip(ckboxVal_1, ckboxName_1)
#             z_ckbox2 = zip(ckboxVal_2, ckboxName_2)
#             z_ckbox3 = zip(ckboxVal_3, ckboxName_3)
#             z_ckbox4 = zip(ckboxVal_4, ckboxName_4)
#             z_ckbox5 = zip(ckboxVal_5, ckboxName_5)
#             z_ckbox6 = zip(ckboxVal_6, ckboxName_6)
#             z_ckbox7 = zip(ckboxVal_7, ckboxName_7)
#             z_ckbox8 = zip(ckboxVal_8, ckboxName_8)
#             z_ckbox9 = zip(ckboxVal_9, ckboxName_9)
#             z_ckbox10 = zip(ckboxVal_10, ckboxName_10)
#             ## 將sql_where傳至前端暫存，value不接受空格，因此將空格以//取代
#             sql_where = self.sql_where.replace(' ', '//')
#
#             if ckboxName_1==[] and ckboxName_2==[] and ckboxName_3==[] and ckboxName_4==[] and ckboxName_5==[] and ckboxName_6==[] and ckboxName_7==[] and ckboxName_8==[] and ckboxName_9==[] and ckboxName_10==[]:
#                 flash('無相關指標。')
#                 return render_template('search.html', scroll='checkBox')
#             else:
#                 return render_template('search.html', scroll='checkBox', sql_where=sql_where, tmp_filter=self.search_filter, z_ckbox1=z_ckbox1, z_ckbox2=z_ckbox2, z_ckbox3=z_ckbox3, z_ckbox4=z_ckbox4, z_ckbox5=z_ckbox5, z_ckbox6=z_ckbox6, z_ckbox7=z_ckbox7, z_ckbox8=z_ckbox8, z_ckbox9=z_ckbox9, z_ckbox10=z_ckbox10)
#         except:
#             alert = "綜合搜尋查詢錯誤。"
#             return render_template("search.html", alert=alert)

class Select():

    def __init__(self):
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    ## 前端按下button後進入的第一個方法
    ## 將暫存在前端的condition、使用者勾選的指標寫成陣列取回
    ## 加上所選標皆不為-1之條件
    def add_sql_where(self, indexes, sql_where, search_filter):
        try:
            str = ''
            for index in indexes:
                if index != indexes[-1]:
                    str += '(m.v_' + index + ' != -1) OR '
                else:
                    str += '(m.v_' + index + ' != -1)'
            ## 將condition改回，並加上指標皆不為-1之條件
            sql_where += ' AND (' + str + ')'
            return Select().select_normal(indexes, sql_where, search_filter)
        except:
            alert = "請選擇指標。"
            return render_template('search.html', alert=alert)

    ## 取得醫療機構資訊
    def select_normal(self, indexes, sql_where, search_filter):
        ## select醫療機構資訊'：名稱、分數＆星等、正向評論數、負向評論數、電話與地址並存入normal[]
        sqlstr = "SELECT h.abbreviation, cast(fr.star as float), fr.positive,  fr.negative, h.phone, h.address FROM merge_data m JOIN hospitals h ON m.hospital_id = h.id JOIN final_reviews fr ON h.id = fr.hospital_id  " + sql_where
        normal = self.cursor.execute(sqlstr).fetchall()  ## normal = [ (名稱, GOOGLE星等, 正向評論數, 負向評論數, 電話, 地址), ......]
        ## 若未找到任何資料，出現錯誤訊息，若有則進入else
        if normal == []:
            alert = "抱歉，找不到您要的資料訊息。"
            return render_template("search.html", alert=alert)
        else:
            return Select().select_data(normal, indexes, sql_where, search_filter)

    ## 取得使用者勾選的資訊
    def select_data(self, normal, indexes, sql_where, search_filter):
        value_substr = 'm.hospital_id'
        deno_substr = 'm.hospital_id'
        level_substr = 'm.hospital_id'
        for r in range(len(indexes)):
            value_substr += (', ' + 'm.v_' + indexes[r])
            level_substr += (', ' + 'm.l_' + indexes[r])
            deno_substr += (', ' + 'm.m_' + indexes[r])
        ## 取得data指標值
        sqlstr = "SELECT " + value_substr + " FROM merge_data m JOIN hospitals h ON m.hospital_id = h.id JOIN final_reviews fr ON h.id = fr.hospital_id " + sql_where
        l_value = self.cursor.execute(sqlstr).fetchall()  ## l_value = [(hospital_id, 指標1之指標值, 指標2之指標值, 指標3之指標值, ......), ......]
        ## 取得data分母(就醫人數)
        sqlstr = "SELECT " + deno_substr + " FROM merge_data m JOIN hospitals h ON m.hospital_id = h.id JOIN final_reviews fr ON h.id = fr.hospital_id " + sql_where
        l_deno = self.cursor.execute(sqlstr).fetchall()
        ## 取得data指標值等級
        sqlstr = "SELECT " + level_substr + " FROM merge_data m JOIN hospitals h ON m.hospital_id = h.id JOIN final_reviews fr ON h.id = fr.hospital_id " + sql_where
        l_level = self.cursor.execute(sqlstr).fetchall()
        ## 將醫療機構資訊、指標值、就醫人數、指標值等級包裝成zip
        z_data = zip(normal, l_value, l_deno, l_level)
        return Result().get_column_name(indexes, z_data, sql_where, search_filter)

class Result():

    def __init__(self):
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    ## 取得欄位名稱
    def get_column_name(self, indexes, z_data, sql_where, search_filter):
        ## 先取得欄位的原始名字(m.v_?)，「醫院機構資訊」為固定欄位，直接手動新增
        getColumns=['醫療機構資訊']
        for r in range(len(indexes)):
            getColumns.append(indexes[r])
        ## 建立columns[]，存入從資料庫中取得的欄位名稱(縮寫)
        columns = []
        for c in getColumns:
            columns.append(self.cursor.execute("SELECT abbreviation FROM column_name WHERE name = '" + str(c) + "'").fetchone()[0])

        ## 建立full_name[]，存入欄位名稱(縮寫)的完整名字
        full_name = ['醫療機構資訊']
        for fn in columns:
            if fn != '醫療機構資訊':
                full_name.append(self.cursor.execute("SELECT name FROM indexes WHERE abbreviation = '" + fn + "'").fetchone()[0])

        ## 將欄位名稱、欄位詳細說明包裝成zip
        z_col = zip(columns, full_name)
        ## 選取的指標數量，-1是因為扣掉第一欄的醫療機構資訊
        ck_len = len(columns) - 1
        ## 取得使用者所選指標將放進排序選單中，第一個為醫療機構資訊，所以不取
        sort_indexes = columns[1:]
        return Result().table(z_data, z_col, ck_len, search_filter, indexes, sql_where, sort_indexes)

    ## 將搜尋結果寫進表格
    def table(self, z_data, z_col, ck_len, search_filter, indexes, sql_where, sort_indexes):
        tmp_indexes = ''
        for r in range(len(indexes)):
            tmp_indexes += indexes[r] + '//'
        sql_where = sql_where.replace(' ', '//')
        tmp_filter = search_filter.replace(' ', '//')
        z_indexes = zip(indexes, sort_indexes)
        ## render至前端HTML，ck_len為指標的長度，columns為欄位名稱，z為醫院資訊和指標值的zip
        return render_template('result.html', scroll = 'results', ck_len=ck_len, z_col=z_col, z_data=z_data, search_filter=search_filter, tmp_filter=tmp_filter, sql_where=sql_where, tmp_indexes=tmp_indexes, z_indexes=z_indexes)