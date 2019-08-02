#! /usr/bin/python
#from ptr_Log import attribute
import pymysql
import importlib
# Define import from Tags Attribute file.
attribute = importlib.import_module("attribute")
tag_File = attribute.Attributes()


class Indexing:
    def __init__(self):
        # Switch into the database
        self.database = tag_File.db_name
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
        data_log = tag_File.action("""select tags_Attributes, url_Referencing from tag_Referencing;""")
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
            try:
                final_tag = interim_tag.replace('[ ', "['").replace(', ', "', '").replace(' ]', "']")
                final_url = referenced[1]
                merger_all = (eval(final_tag), final_url)
                final_storage.append(merger_all)
            except SyntaxError:
                final_tag = interim_tag.replace("[ ", '["').replace(", ", '", "').replace(' ]', '"]')
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
        return generated_tags

    def setting_tags(self):
        """User input of Tags.
        :return: tags selected
        """
        user_data = []
        print("\n########## Or just press enter for all ptr: ")
        multiple_tags = input("Enter the desired tags: (Separate with a comma) and No Space: ")
        analyze_tag = eval(str('["' + multiple_tags + '"]').replace(',', '","'))

        for selected_tags in analyze_tag:
                print(user_data, selected_tags)
                for setter in self.searching():
                    for tags_only in setter[0]:
                        if selected_tags in tags_only:
                            user_data.append(setter)
        return user_data

    def push_loader(self):
        """
        Pushing all the final data into ptr_Loader
        :return: a list of all the url containing the username.
        """
        print("Total number of unique tags is %d" % len(self.all_available()))
        print("select tags from below \n%s" % str(self.all_available()))
        pure_urls = []
        for download_urls in self.setting_tags():
            pure_urls.append(download_urls[1])
        print("The total Number of files to be downloaded is %d" % len(pure_urls))
        return pure_urls


if __name__ == '__main__':
    pick = Indexing()
    pick.push_loader()

