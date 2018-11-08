import sqlite3
from pandas import DataFrame


class Hosid():

    def __init__(self):
        db = sqlite3.connect("voyager.db")
        self.cursor = db.cursor()

    def search_area(self, county, township):
        # self.county = county
        # self.township = township
        area = str(county + '%' + township + '%')
        sqlstr = "SELECT * FROM hospitals WHERE address LIKE '" + area + "'"
        results = self.cursor.execute(sqlstr).fetchall()
        # d1 = {
        #     "": results
        # }
        # print(DataFrame(d1))
        res = ''
        for i in range(len(results)):
            res += (str(results[i]) + '\n')

        print(res)

abc = Hosid()
abc.search_area('桃園', '桃園')

