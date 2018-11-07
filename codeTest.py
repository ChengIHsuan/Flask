import sqlite3



class Hosid():

    def __init__(self, id):
        self.id = id
        db = sqlite3.connect("voyager.db")
        self.cursor = db.cursor()
    def hospital_id(self):
        sqlstr = "SELECT * FROM hospitals WHERE id < " + str(self.id)
        results = self.cursor.execute(sqlstr).fetchall()

        res = ''
        for i in range(len(results)):
            res += str(results[i]) + '\n'

        print(str(res))
        # print(results)
        # return res
abc = Hosid('5')
abc.hospital_id()

