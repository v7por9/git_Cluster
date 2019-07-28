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
            self.connection = pymysql.connect(host='localhost',
                                              port=3306,
                                              user=self.username,
                                              passwd=self.passwd)
            self.cursor = self.connection.cursor()
        return

    def action(self, query):
        """
        :param query: Passing an SQL Command for execution.
        :return: The result or error from the query raised.
        """
        # TODO Catch the Errors from the raised query.
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except pymysql.err.ProgrammingError:
            print("There was an **SQL Syntax Error**")


test = Attributes()
print(test.action('show database'))