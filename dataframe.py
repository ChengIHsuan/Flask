from pandas import DataFrame
import sqlite3

db = sqlite3.connect('voyager.db')
c = db.cursor()
sqlstr = "SELECT id, name, type, address FROM hospitals WHERE id < 30"
cursor = c.execute(sqlstr)

# id = []
# name = []
# type = []
# address = []
# row = cursor.fetchone()
# while row is not None:
#     id.append(row[0])
#     name.append(row[1])
#     type.append(row[2])
#     address.append(row[3])
#     row = cursor.fetchone()

row = cursor.fetchall()
d1 = {
    "" : row
}
print(DataFrame(d1))


# groups = ["Modern Web", "DevOps", "Cloud", "Big Data", "Security", "自我挑戰組"]
# ironmen = [59, 9, 19, 14, 6, 77]
#
# ironmen_dict = {
#                 "groups": groups,
#                 "ironmen": ironmen
# }
#
# ironmen_df = DataFrame(ironmen_dict)
# print(ironmen_df)