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

    def searching(self):
        final_storage = []
        """
        Merging all the tags into a list
        :return: URL reference & the Tags Associated
        """
        for referenced in self.eliminate():
            interim_tag = '[' + referenced[0] + ']'
            final_tag = interim_tag.replace('[ ', "['").replace(', ', "', '").replace(' ]', "']")
            final_url = referenced[1]
            merger_all = (eval(final_tag), final_url)
            final_storage.append(merger_all)
        return final_storage

    def all_available(self):
        """
        Producing all available for user selection.
        :return: returns a single list of all tags.
        """
        generated_tags = []
        tester = []
        for tags_only in self.searching():
            for single_tags in tags_only[0]:
                tester.append(single_tags)
                if single_tags not in generated_tags:
                    generated_tags.append(single_tags)
                else:
                    pass
        print("Total number of unique tags is %d" % len(generated_tags))
        return generated_tags

    #def setting_tags

test = Indexing()
print(test.all_available())



