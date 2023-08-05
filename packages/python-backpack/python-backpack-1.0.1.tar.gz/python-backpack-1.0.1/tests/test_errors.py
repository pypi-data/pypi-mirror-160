# ----------------------------------------------------------------------------------------
# Python-Backpack - Custom Exceptions UnitTest
# Maximiliano Rocamora / maxirocamora@gmail.com
# https://github.com/MaxRocamora/python-backpack
# ----------------------------------------------------------------------------------------

import os
import sys
import unittest

from backpack.custom_errors import EnvironmentVariableNotFound
from backpack.custom_errors import ApplicationNotFound

mod_path = os.path.dirname(__file__)
if mod_path not in sys.path:
    sys.path.append(mod_path)


def get_env_var(name: str):
    ''' call for an env var or raise EnvironmentVariableNotFound '''
    try:
        value = os.environ[name]
    except KeyError as e:
        raise EnvironmentVariableNotFound(name) from e
    return value


def get_app(name: str):
    ''' raisers error '''
    raise ApplicationNotFound(f'Background executable not found {name}')


class Test_Errors(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        pass

    def test_env_var_error(self):
        ''' testing module '''
        self.assertRaises(EnvironmentVariableNotFound, get_env_var, 'my_env_var')
        error = EnvironmentVariableNotFound('my_env_var')
        self.assertEqual(str(error), error.message)

    def test_env_app_error(self):
        ''' testing module '''
        self.assertRaises(ApplicationNotFound, get_app, 'my_app.exe')

        error = ApplicationNotFound('my_app.exe')
        self.assertEqual(str(error), error.message)


if __name__ == '__main__':
    unittest.main()
