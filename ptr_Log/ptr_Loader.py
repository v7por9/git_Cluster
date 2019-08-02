#! /usr/bin/python3
import os
import urllib.request
import shutil
import sys
import importlib
tag = importlib.import_module('tag_Collection')
tag_Collection = tag.Indexing()
print(dir(tag_Collection))
exit()


class Activity:
    def __init__(self):
        self.url = "https://sf.co.ua/"
        # Items returned from collection is a list.
        self.item = tag_Collection.push_loader()
        self.path = os.path.join(os.getcwd(), '../..')
        os.chdir(self.path)
        try:
            os.mkdir('ptr_Loaded')
        except FileExistsError:
            print("File already present")
            pass
        self.full_path = os.path.join(self.path, 'ptr_Loaded')
        print(self.full_path)
        return

    def payload(self):
        for picked_ptr in self.item:

            try:
                request = urllib.request.urlopen(picked_ptr).read()
                # Getting the path to the image file
                image_location = request.split(b'<img src=')[-1]
                only_image = eval(image_location.split(b" ")[0])

                # Download path && Download to temp_file and path to download
                temp_name = urllib.request.urlretrieve(self.url + '/' + only_image)[0]

                # Renaming the file from image_only to filename
                filename = only_image.split('/')[-1]

                try:
                    if sys.platform.startswith('win'):
                        shutil.move(temp_name, os.path.abspath(self.full_path + filename))
                        print(os.path.abspath(self.full_path + filename))

                    elif sys.platform.startswith('linux'):
                        shutil.move(temp_name, os.path.join(self.full_path, filename))
                        print(os.path.join(self.full_path, filename))

                except FileExistsError:
                    os.remove(os.path.join(self.full_path, filename))
                    os.remove(temp_name)

            except EnvironmentError:
                pass


if __name__ == '__main__':
    take = Activity()
    take.payload()
