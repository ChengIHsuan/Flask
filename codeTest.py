import sqlite3
from flask import Flask, request, render_template, flash, redirect
from models.search import Search

class Disease():

    def __init__(self, dbName):
        db = sqlite3.connect(dbName)
        self.cursor = db.cursor()
        self.dbName = dbName

    def printName(self):
        sqlstr = "SELECT name FROM user"
        user = self.cursor.execute(sqlstr).fetchone()
        print(self.dbName)
        print(user)

Disease('aaa.db').printName()
Disease('bbb.db').printName()

    # def test(self, aa):
    #     sqlstr = "SELECT v_12, v_13, v_14 FROM merge_data WHERE hospital_id <5"
    #     sqlstr2 = "SELECT id, name FROM hospitals WHERE id<5"
    #     a = self.cursor.execute(sqlstr).fetchall()
    #     b = self.cursor.execute(sqlstr2).fetchall()
    #     print(a)
    #     print(b)
    #     # print(sorted(a, reverse=True))  ## 遞減
    #     # print(sorted(a))  ## 遞增
    #     # print(sorted(a, key=lambda l : l[1]))  ## 按index1排序
    #     z =zip(a, b)
    #     print(sorted(z, key = lambda l: l[0][2], reverse=True))  ##按照zip中「0位置的陣列」中的「2位置的資料」遞增排序-->a[2]的資料

# Disease().test('aaaa')