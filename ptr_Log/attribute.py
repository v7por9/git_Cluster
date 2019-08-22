#! /usr/bin/python

import pymysql
import urllib.request


class Attributes:
    def __init__(self):
        self.url = "https://sf.co.ua/"
        self.db_name = "ptr_Tags_DB"
        self.start, self.stop = (0, 500000)
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
        except pymysql.err.ProgrammingError as e:
            print("There was an **SQL Syntax Error** %s" % e)
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
            url_Referencing text not null,
            tags_Attributes text,
            Resolution text)""")
        else:
            # Database already present, since only one database is needed.
            print("Database already exists.")
            pass
        return

    def db_insert(self, tag, urls, res):
        """
        Entering the data into a two column database.
        :return: Entering data into tags & urls.
        """
        self.action("""insert into tag_Referencing 
        (url_Referencing, tags_Attributes, Resolution) 
        values ('%s', '%s', '%s')""" % (tag, urls, res))
        return

    def db_commit(self):
        self.connection.commit()
        return

    def db_continue(self):
        data_range = []
        """
        Reading last location of file tags and continuing.
        :return: return range
        """
        self.action("use %s" % self.db_name)
        recorded_url = eval(str(list(self.action("select url_Referencing from tag_Referencing"))).
                            replace("(", "").
                            replace(",)", ""))
        try:
            renew_start = int(str(recorded_url[-1]).split('id')[-1])
        except IndexError:
            renew_start = 0
        if renew_start < self.start:
            data_range.append(self.start)
        else:
            data_range.append(renew_start)
        data_range.append(int(self.stop))
        data_tuple = eval(str(data_range).replace('[', "(").replace("]", ')'))
        return data_tuple

    def ptr_request(self):
        """Loading HTML file of the page to get all the details
        :return: the tags of the file, the url link, the image resolution,
        """
        for app_number in range(self.db_continue()[0], self.db_continue()[1]):
            full_url = self.url + "id" + str(app_number)
            try:
                request = urllib.request.urlopen(full_url).read()
                try:
                    resolution = str(request).split("Resolution")[1].split("/a><")[0].replace('<', "").replace('">', '')
                except IndexError:
                    resolution = 0
                try:
                    file_attributes = (str(request).
                                       split('content="HD Wallpapers, Desktop High Definition Wallpapers,')[1].
                                       split('content="width=device-width')[0].
                                       replace('n<meta name="viewport', "").replace('."/>\\"', ""))
                except IndexError:
                    file_attributes = "No Tags"
                self.db_insert(full_url, file_attributes, resolution)
                self.db_commit()
                # Combining the variables, i.e attributes, resolution, url link.
            except EnvironmentError:
                pass


if __name__ == '__main__':
    tags = Attributes()
    tags.database_create()
    tags.action('use ptr_Tags_DB')
    print("Picking up from %s" % str(tags.db_continue()))
    tags.ptr_request()
    tags.db_commit()
