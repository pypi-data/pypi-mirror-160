# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File:           mongo_client.py
   Description:
   Author:        
   Create Date:    2020/07/21
-------------------------------------------------
   Modify:
                   2020/07/21:
-------------------------------------------------
"""
import pymongo
from log_handler import LogHandler


class MongodbClient:

    def __init__(self, database, datatable):
        self.logging = LogHandler('mongo_db')
        self.db_client = pymongo.MongoClient('mongodb://localhost:27017/')
        # 有密码验证时self.db_client = pymongo.MongoClient('mongodb://用户名:密码@ip:端口/'+database)#
        self.database = database
        self.db_name = self.db_client[database]
        self.collection_name = self.db_name[datatable]

    def checkDataBase(self):
        db_list = self.db_client.list_database_names()
        if self.database in db_list:
            self.logging.info("数据库：%s 存在" % self.database)
            self.isCheckOK = 1
        else:
            self.logging.info("数据库：%s 不存在" % self.database)
            self.isCheckOK = 0

    def insert_one(self, tupstr):
        try:
            self.collection_name.insert_one(tupstr)
            self.logging.info("数据插入成功!")
        except Exception as e:
            self.logging.info("执行函数：insert_one失败，错误信息%s" % e)

    def insert_many(self, listStr):
        try:
            result = self.collection_name.insert_many(listStr)
            self.logging.info("数据插入成功!")
        except Exception as e:
            self.logging.info("执行函数：insert_many失败，错误信息：%s" % e)

    def find_one(self):
        try:
            self.checkDataBase()
            if self.isCheckOK == 0:
                self.logging.info("当前数据库不存在，无法执行查询操作")
                return
            dit = self.collection_name.find_one()
            self.logging.info("首数据查询成功")
            return dit
        except Exception as e:
            self.logging.info("执行函数：find_one失败，错误信息：%s" % e)

    def find_all(self):
        try:
            self.checkDataBase()
            if self.isCheckOK == 0:
                self.logging.info("当前数据库不存在，无法执行查询操作")
                return
            dits = self.collection_name.find()
            self.logging.info("全部数据查询成功")
            return dits
        except Exception as e:
            self.logging.info("执行函数：find_all失败，错误信息%s" % e)

    def find_partShow(self, rules):
        try:
            self.checkDataBase()
            if self.isCheckOK == 0:
                self.logging.info("当前数据库不存在，无法执行查询操作")
                return
            dits = self.collection_name.find({}, rules)
            self.logging.info("按照条件，数据查询成功")
            return dits
        except Exception as e:
            self.logging.info("执行函数：find_partShow失败，错误信息%s" % e)

    def find_rules(self, rules):
        try:
            self.checkDataBase()
            if self.isCheckOK == 0:
                self.logging.info("当前数据库不存在，无法执行查询操作")
                return
            dits = self.collection_name.find(rules)
            self.logging.info("按照条件，数据查询成功")
            return dits
        except Exception as e:
            self.logging.info("执行函数：find_rules失败，错误信息%s" % e)

    def find_limit(self, num):
        try:
            self.checkDataBase()
            if self.isCheckOK == 0:
                self.logging.info("当前数据库不存在，无法执行查询操作")
                return
            dits = self.collection_name.find().limit(num)
            self.logging.info("按照行数查询数据成功")
            return dits
        except Exception as e:
            self.logging.info("执行函数：find_limit失败，错误信息%s" % e)

    def update_one(self, rules, newValue):
        try:
            self.checkDataBase()
            if self.isCheckOK == 0:
                self.logging.info("当前数据库不存在，无法执行查询操作")
                return
            self.collection_name.update_one(rules, newValue)
            self.logging.info("首条匹配数据修改成功")
        except Exception as e:
            self.logging.info("执行函数：updata_one失败，错误信息%s" % e)

    def update_many(self, rules, newValue):
        try:
            self.checkDataBase()
            if self.isCheckOK == 0:
                self.logging.info("当前数据库不存在，无法执行查询操作")
                return
            dits = self.collection_name.update_one(rules, newValue)
            return dits
        except Exception as e:
            self.logging.info("")

    def sort(self, key, order=1):
        try:
            self.checkDataBase()
            if self.isCheckOK == 0:
                self.logging.info("当前数据库不存在，无法执行查询操作")
                return

            mydoc = self.collection_name.find().sort(key, order)
            return mydoc
        except Exception as e:
            self.logging.info("执行函数：sort 失败:错误信息%s" % e)

    def delete_one(self, rule):
        try:
            self.checkDataBase()
            if self.isCheckOK == 0:
                self.logging.info("当前数据库不存在，无法执行查询操作")
                return

            self.collection_name.delete_one(rule)
            self.logging.info("单条数据删除成功")
        except Exception as e:
            self.logging.info("执行函数delete_one失败，错误信息%s" % e)

    def delete_many(self, rules):
        try:
            self.checkDataBase()
            if self.isCheckOK == 0:
                self.logging.info("当前数据库不存在，无法执行查询操作")
                return

            self.collection_name.delete_many(rules)
            self.logging.info("数据删除成功")
        except Exception as e:
            self.logging.info("执行函数delete_many失败，错误信息%s" % e)

    def delete_all(self):
        try:
            self.checkDataBase()
            if self.isCheckOK == 0:
                self.logging.info("当前数据库不存在，无法执行删除操作")
                return

            self.collection_name.delete_many({})
            self.logging.info("全部数据删除成功")
        except Exception as e:
            self.logging.info("执行函数delete_all失败，错误信息%s" % e)

    def drop(self):
        try:
            self.checkDataBase()
            if self.isCheckOK == 0:
                self.logging.info("当前数据库不存在，无法执行删除表操作")
                return

            self.collection_name.drop()
            self.logging.info("表删除成功")
        except Exception as e:
            self.logging.info("执行函数drop失败，错误信息%s" % e)


# 测试用例
def tesInsert():
    database = "runoobdb"  # 数据库
    datatable = "sitesTest"  # 数据表
    db = MongodbClient(database, datatable)

    # 测试单条数据
    mydict = {"name": "RUNOOB", "alexa": "10000", "url": "https://www.runoob.com"}
    db.insert_one(mydict)

    # 测试多条数据
    mylist = [
        {"name": "RUNOOB", "cn_name": "菜鸟教程"},
        {"name": "Google", "address": "Google 搜索"},
        {"name": "Facebook", "address": "脸书"},
        {"name": "Taobao", "address": "淘宝"},
        {"name": "Zhihu", "address": "知乎"}
    ]
    db.insert_many(mylist)


def tesFind():
    database = "runoobdb"  # 数据库
    datatable = "sitesTest"  # 数据表
    db = MongodbClient(database, datatable)
    # 查找单条数据
    x = db.find_one()
    print(x)

    # 查找全部数据
    x1 = db.find_all()
    for data in x1:
        print(data)

    # 按照规则查询
    myqurey1 = {'_id': 0, 'name': 1, 'address': 1}
    x2 = db.find_partShow(myqurey1)
    for data in x2:
        print(data)
    # 仅显示一条数据
    myqurey2 = {'name': 1}
    x3 = db.find_partShow(myqurey2)
    for data in x3:
        print(data)

    # 高级查询
    myqurey3 = {"name": {"$gt": "H"}}  # 查询首字符大于H的数据
    x4 = db.find_rules(myqurey3)
    for data in x4:
        print(data)

    # 按照指定数据显示
    myqurey4 = {"name": "Taobao"}
    x5 = db.find_rules(myqurey4)
    for data in x5:
        print(data)

    # 正则表达式查询
    myqurey5 = {"name": {"$regex": "R"}}  # 查询首字母为R的数据
    x6 = db.find_rules(myqurey5)
    for data in x6:
        print(data)

    # 查询指定的数据量
    x7 = db.find_limit(10)
    for data in x7:
        print(data)





if __name__ == '__main__':
    tesInsert()