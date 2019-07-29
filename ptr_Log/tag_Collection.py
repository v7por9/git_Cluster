#! /usr/bin/python
from ptr_Log import attribute
import pymysql

# Define import from Tags Attribute file.
tag_File = attribute.Attributes()


class Indexing:
    def __init__(self):
        # Use test database...
        self.database = 'test_ptr_Tags_DB'
        # Switch to actual database
        #self.database = tag_File.db_name
        self.no_tags = []

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

    def db_preparation(self):
        db = tag_File.action("show databases")
        try:
            tag_File.action('use %s' % self.database)
        except EnvironmentError:
            print("Only the following databases are available %s" % str(db))
        return db

    def collect_tags(self):
        """ Read from the database the url & tags to the file.
        :return: return url & tags
        """
        # Execute and confirm database use & presence other than use in __main__
        self.db_preparation()
        data_log = tag_File.action("""select url_Referencing, tags_Attributes from tag_Referencing;""")
        return list(data_log)

    def eliminate(self):
        """
        To eliminate untagged References
        :return: Only tagged references
        """
        # Storing the Tags & Referencing.
        store = []

        for refer in self.collect_tags():
            if refer[0] != "No Tags":
                store.append(refer)
            else:
                self.no_tags.append(refer[1])
        return store
    


test = Indexing()
print(test.eliminate())
print(len(test.eliminate()))
print(len(test.no_tags))


