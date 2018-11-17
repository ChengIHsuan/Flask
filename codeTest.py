import sqlite3
from pandas import DataFrame
import numpy as np

db = sqlite3.connect('voyager.db')
c = db.cursor()

getId = c.execute("SELECT id FROM diseases WHERE name = '氣喘疾病'")
diseaseId = (getId.fetchone()[0])
r = {
    1: range(1,6),
    2: range(6,12),
    3: range(12,16),
    4: range(16,19),
    5: range(19,23),
    6: range(23,28),
    7: range(28,32),
    8: range(32,34)  ##substr
}
select= ''
for i in r.get(diseaseId):
    select += (", (select value from data where index_id = " + str(i) + ") as index"+ str(i))


sqlstr = "SELECT h.name" + select + " FROM hospitals h JOIN final_data f ON h.id = f.hospital_id where hospital_id =1"
res = c.execute(sqlstr).fetchone()
print(res)
