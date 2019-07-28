#! /usr/bin/python

import os
import pymysql

class Attributes:
    def __init__(self):
        self.url = "https://sf.co.ua"
        self.store = []
        self.value = ""
        with open('st0r3.txt', 'r') as fyle:
            login_details = eval(str(fyle.readlines()).replace("\\n", ''))
            self.username = login_details[0]
            self.passwd = login_details[1]
            self.connection = MySQLdb.connect('localhost', "3306", self.username, self.passwd)
            self.cursor = self.connection.cursor()
        return

    def db_action(self, query):
        execute = self.cursor.execute(query)
        data = execute
        return
