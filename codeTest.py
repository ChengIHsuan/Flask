import sqlite3
import tkinter as tk
import numpy as np

db = sqlite3.connect('voyager.db')
c = db.cursor()

# disease = input("輸入疾病")
getId = c.execute("SELECT id FROM diseases WHERE (name LIKE '%消化%')")
diseaseId = (getId.fetchone()[0])


sqlstr = "SELECT id, name FROM hospitals"
results = c.execute(sqlstr).fetchall()  ##執行sqlstr，並列出所有結果到results[]
amount = len(results)

index_range = {
                1: range(1,6),
                2: range(6,12),
                3: range(12,16),
                4: range(16,19),
                5: range(19,23),
                6: range(23,28),
                7: range(28,32),
                8: range(32,34)
            }
length = 2
for index in index_range.get(diseaseId):
    length += 1
    sql = "select hospital_id, value || ' (分母:' || denominator || ')' from data where index_id = " + str(index)
    deno = c.execute(sql).fetchall()
    print(deno)
    for j in range(0, amount):  ##7134
        for i in range(0, len(deno)):  ##800
            if results[j][0] == deno[i][0]:
                results[j] += (deno[i][1],)
        if len(results[j]) < length:
            results[j] += "無相關資料",

##取得欄位名稱
columns = []
columns.append("醫院ID")
columns.append("醫院名稱")
for r in index_range.get(diseaseId):
    col = c.execute("SELECT abbreviation FROM indexes WHERE id = " + str(r)).fetchone()[0]
    columns.append(col)

##建立一個陣列，儲存整理好的資料結果
context = []
for k in range(len(results)):  ##7134
    ##建立一個dict，獎每一筆結果轉存成dict的型態
    d = {}
    for l in range(len(columns)):  ##4
        d[columns[l]] = results[k][l]
    context.append(d)
    long = len(columns)
print(context)