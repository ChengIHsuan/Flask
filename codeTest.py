import sqlite3

db = sqlite3.connect('voyager.db')
c = db.cursor()

#
# def get_column_name(self, results, sqlstr, indexs):
#     ##將二維陣列results[]轉成numpy array，並計算總資料數
#     print('1')
#     print(indexs)
#     length = len(indexs)
#     amount = len(results)
#     print(length)
#     ##取得sqlstr中select的欄位，並以","做分割
#     s = sqlstr.index("FROM") - 1
#
#     getColumns = (sqlstr[7:s]).split(', ')
#     print(getColumns)
#     ##取得欄位名稱
getColumns = []
getColumns.append('h.name')
columns = []
for co in getColumns:
    col = c.execute("SELECT chi_name FROM column_name WHERE name = '" + co + "'").fetchone()[0]
    columns.append(col)
    print(columns)
        # return Result().table(results, amount, columns, length)