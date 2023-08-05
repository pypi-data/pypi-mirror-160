# ----------------------------------------------------------------------------------------
# Python-Backpack - TestUtils Tests
# Maximiliano Rocamora / maxirocamora@gmail.com
# https://github.com/MaxRocamora/python-backpack
# ----------------------------------------------------------------------------------------

import os
import sys
import time
import unittest

from backpack.test_utils import random_string
from backpack.test_utils import time_function_decorator

mod_path = os.path.dirname(__file__)
if mod_path not in sys.path:
    sys.path.append(mod_path)


@time_function_decorator
def one_second_delay():
    ''' one second delay to test time_function_decorator '''
    time.sleep(1)


class Test_Errors(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        pass

    def test_random_string(self):
        ''' testing module '''
        r = random_string(10)
        self.assertEqual(len(r), 10)
        self.assertEqual(isinstance(r, str), True)
        r = random_string(0)
        self.assertEqual(len(r), 0)

    def test_delay(self):
        one_second_delay()


if __name__ == '__main__':
    unittest.main()
