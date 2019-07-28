#! /usr/bin/python

import os
import pymysql

class Attributes:
    def __init__(self):
        self.url = "https://sf.co.ua"
        self.db_name = "ptr_Tags_DB"
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
        return

    def database_create(self):
        """
        To create a database of the storage of Tag names and reference URL's
        :return:
        """
        log_db = list(self.action("show databases"))
        # Eliminating unnecessary data in the list.
        present_db = eval((str(log_db).replace("(", "").replace(",)", '')))
        if self.db_name not in present_db:
            self.action("create database %s" % self.db_name)
            print("A database has been created by the name %s" % self.db_name)
            self.action('use %s' % self.db_name)
            # New database has been created, populate the db with tables.
            self.action("""create table tag_Referencing
            (id int(12) not null primary key auto_increment,
            tags_Attributes text not null,
            url_Referencing text)""")
        else:
            # Database already present, since only one database is needed.
            print("Database already exists.")
            pass
        return


test = Attributes()
test.database_create()
test.action('use ptr_Tags_DB')
print(test.action("show tables"))
