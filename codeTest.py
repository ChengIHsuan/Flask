import sqlite3

db = sqlite3.connect('voyager.db')
c = db.cursor()
# ======================================
sqlstr1 = "SELECT h.id, h.name, h.type, h.address FROM hospitals h WHERE h.id < 6"
normal = c.execute(sqlstr1).fetchall()
sqlstr2 = "SELECT hospital_id, m.m_1, m.m_2 FROM merge_data m WHERE hospital_id <6"
ckbox = c.execute(sqlstr2).fetchall()
columns = ['資訊', '指標一', '指標二']
col_len = len(columns)-1

context = []
for i in range(len(ckbox)):  ##0 1 2 3 4
    ##建立一個dict，獎每一筆結果轉存成dict的型態
    d = {}
    for j in range(1, len(columns)):   ##1, 2
        print(columns[j])
        print(ckbox[i][j])
        d[columns[j]] = ckbox[i][j]
    context.append(d)
##同時進行迭代
z = zip(normal, context)