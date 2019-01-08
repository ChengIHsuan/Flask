import sqlite3
from flask import Flask, request, render_template, flash , redirect

class Sort():

    def __init__(self):
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    def reSort(self, index1, sql_where2, item, filter):

        items = item.split("//")
        del items[-1]
        sql_where = sql_where2.replace("//", " ")
        search_filter = filter.replace("//", " ")
        a = []
        name = self.cursor.execute("select name from column_name where abbreviation = '" + index1 + "'").fetchone()[
            0]
        a.append(name)
        for r in range(len(a)):
            v = a[r].replace('m.m_', 'm.l_')
            x = a[r].replace('m.m_', 'm.v_')
            new = (" order by " + v + " DESC , " + x + " DESC")

        sqlstr = "SELECT h.abbreviation, fr.star, fr.positive,  fr.negative, h.phone, h.address, cast(fr.star as float) FROM hospitals h JOIN final_reviews fr ON h.id = fr.hospital_id join merge_data m ON h.id = m.hospital_id" + sql_where + new

        normal = self.cursor.execute(sqlstr).fetchall()

        if normal == []:
            flash('抱歉，找不到您要的資料訊息。')
            return render_template("searchArea.html")
        else:
            return Sort().select_data2(normal, items, sql_where, search_filter, new)

    def select_data2(self, normal, items, sql_where, search_filter, new):
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
        sqlstr = "SELECT " + deno_substr + " FROM merge_data m JOIN hospitals h ON m.hospital_id = h.id JOIN final_reviews fr ON h.id = fr.hospital_id " + sql_where + new
        l_deno = self.cursor.execute(sqlstr).fetchall()
        ## 取得data指標值等級
        sqlstr = "SELECT " + level_substr + " FROM merge_data m JOIN hospitals h ON m.hospital_id = h.id JOIN final_reviews fr ON h.id = fr.hospital_id " + sql_where + new
        l_level = self.cursor.execute(sqlstr).fetchall()
        ## 取得data指標值
        sqlstr = "SELECT " + value_substr + " FROM merge_data m JOIN hospitals h ON m.hospital_id = h.id JOIN final_reviews fr ON h.id = fr.hospital_id " + sql_where + new
        l_value = self.cursor.execute(sqlstr).fetchall()
        return Result().get_column_name(normal, items, l_deno, l_level, l_value, search_filter, sql_where)

class Result():

    def __init__(self):
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    ## 取得欄位名稱
    def get_column_name(self, normal, items, l_deno, l_level, l_value, search_filter, sql_where):
        ## 先取得欄位的原始名字(m.m_?)，「醫院機構資訊」為固定欄位，直接手動新增
        getColumns = ['醫療機構資訊']
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
                full_name.append(
                    self.cursor.execute("SELECT name FROM indexes WHERE abbreviation = '" + fn + "'").fetchone()[0])
        indexes = columns[1:]
        return Result().table(normal, columns, full_name, l_deno, l_level, l_value, search_filter, indexes, sql_where, items)

    ## 將搜尋結果寫進表格
    def table(self, normal, columns, full_name, l_deno, l_level, l_value, search_filter, indexes, sql_where, items):
        ## 選取的指標數量，-1是因為扣掉第一欄的醫療機構資訊
        ck_len = len(columns) - 1
        ## 建立deno[]存放分母資料
        deno = []
        for i in range(len(l_deno)):  # ckbox[][]為Select().get_checkbox()取得的指標值
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
        item = ""
        for r in range(len(items)):
            item += (items[r] + "//")
        sql_where = sql_where.replace(" ", "//")
        search_filter2 = search_filter.replace(" ", "//")
        ## render至前端HTML，ck_len為指標的長度，columns為欄位名稱，z為醫院資訊和指標值的zip
        return render_template('searchArea.html', scroll='results', ck_len=ck_len, z_col=z_col, z=z, columns=columns, filter=search_filter, filter2=search_filter2, indexes=indexes,sql_where=sql_where, item=item)