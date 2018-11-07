import sqlite3

class Hospital():

    def __init__(self):
        self.table = 'hospitals'
        db = sqlite3.connect('voyager.db')
        self.cursor = db.cursor()

    def hospital_id(self, id):
        self.id = id
        sqlstr = "SELECT * FROM hospitals WHERE id < " + str(self.id)
        results = self.cursor.execute(sqlstr).fetchall()

        res = ''
        for i in range(len(results)):
            res += (str(results[i]) + '\n')

        return res

    def get_type(self):
        sqlstr = "SELECT * FROM hospitals WHERE id < 3"
        # result = []
        # for res in self.cursor.execute(sqlstr).fetchone():
        #     result.append(res)
        res = self.cursor.execute(sqlstr).fetchone()
        return res


        # return '<p>id：%s   name：%s</p>' % (hos_id, hos_name)
