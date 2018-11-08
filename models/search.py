import sqlite3
from pandas import DataFrame

class Hospital():

    def __init__(self):
        # self.table = 'hospitals'
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    ##不要看
    def hospital_id(self, id):
        # self.id = id
        sqlstr = "SELECT id, name, type, address FROM hospitals WHERE id < " + id
        results = self.cursor.execute(sqlstr).fetchall()

        res = ''
        for i in range(len(results)):
            res += (str(results[i]) + '\r')

        return res

    ##看這個就好
    def search_area(self, county, township):
        area = str(county + '%' + township + '%')
        sqlstr = "SELECT id, name, type, address FROM hospitals WHERE address LIKE '" + area + "'"
        results = self.cursor.execute(sqlstr).fetchall()  ##執行sqlstr，並列出所有結果到results

        ##results是list，將results轉成字串res
        res = ''
        for i in range(len(results)):
            res += (str(results[i]) + '<br>')  ##<br>：換行符號
        ##回傳字串res
        return res

        # return '<p>id：%s   name：%s</p>' % (hos_id, hos_name)
