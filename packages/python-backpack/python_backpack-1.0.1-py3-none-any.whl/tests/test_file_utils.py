# ----------------------------------------------------------------------------------------
# Python-Backpack - FolderUtils Tests
# Maximiliano Rocamora / maxirocamora@gmail.com
# https://github.com/MaxRocamora/python-backpack
# ----------------------------------------------------------------------------------------

import os
import sys
import unittest
import shutil

from backpack.file_utils import replace_strings_in_file, remove_line_from_file

mod_path = os.path.dirname(__file__)
if mod_path not in sys.path:
    sys.path.append(mod_path)

# test folders
BASE_FILE = os.path.join(mod_path, 'test_files', 'origin.txt')
EDITED_FILE = os.path.join(mod_path, 'test_files', 'edited.txt')
STRINGS = ['to be replaced!', 'also replaced']
NEW_STRING = 'REPLACED'


class Test_Errors(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        pass

    def test_replace_strings_in_file(self):
        ''' testing module '''
        shutil.copy(BASE_FILE, EDITED_FILE)
        replace_strings_in_file(EDITED_FILE, STRINGS, NEW_STRING)

    def test_remove_line_from_file(self):
        ''' testing module '''
        source_file = os.path.join(mod_path, 'test_files', 'origin_remove.txt')
        test_file = os.path.join(mod_path, 'test_files', 'edited_remove.txt')
        shutil.copy(source_file, test_file)
        remove_line_from_file(test_file, ['REMOVE_ME', 'to be replaced!'])


if __name__ == '__main__':
    unittest.main()
