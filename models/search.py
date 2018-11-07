import sqlite3
from pandas import DataFrame
class Hospital():

    def __init__(self):
        self.table = 'hospitals'
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    def hospital_id(self, id):
        # self.id = id
        sqlstr = "SELECT id, name, type, address FROM hospitals WHERE id < " + id
        results = self.cursor.execute(sqlstr).fetchall()

        res = ''
        for i in range(len(results)):
            res += (str(results[i]) + '\r')

        return res

    def search_area(self, county, township):
        # self.county = county
        # self.township = township
        area = str(county + '%' + township + '%')
        sqlstr = "SELECT id, name, type, address FROM hospitals WHERE address LIKE '" + area + "'"
        results = self.cursor.execute(sqlstr).fetchall()

        res = ''
        for i in range(len(results)):
            res += (str(results[i]) + '<br>')

        return res

        # return '<p>id：%s   name：%s</p>' % (hos_id, hos_name)
