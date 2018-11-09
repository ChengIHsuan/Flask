import sqlite3
from pandas import DataFrame
import numpy as np


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

    def table(self):
        sqlstr = "SELECT id,name,type,address FROM hospitals WHERE id <3"
        results = self.cursor.execute(sqlstr).fetchall()
        x = np.array(results, dtype=str)
        # context = [
        #     {
        #         'id':str(results[0,1]),
        #         'name':str(results[0,2]),
        #     }
        # ]
        a = sqlstr.index("FROM")-1
        column = (sqlstr[7:a]).split(',')
        print(sqlstr[7:a])
        print(column[1])
        print(len(column))

abc = Hosid()
# abc.search_area('桃園', '桃園')
abc.table()
