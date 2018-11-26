import sqlite3

db = sqlite3.connect('voyager.db')
c = db.cursor()

sqlstr  = "select h.id, h.name, mr.better, mr.normal, mr.worse from hospitals h join merge_reviews mr on h.id = mr.hospital_id"
results = c.execute(sqlstr).fetchall()
for i in range(len(results)):
    test = ("情緒分數為1的評論數：" + str(results[i][2]) + "<p>情緒分數為0的評論數：" + str(results[i][3]) + "<p>情緒分數為-1的評論數："+str(results[i][4]))
    results[i] = results[i][:2]
    results[i] += (test,)
print(results[0])
print(results)