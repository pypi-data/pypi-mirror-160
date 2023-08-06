from wdbse import functions
import unittest
from wsqluse.wsqluse import Wsqluse


class TestFunctions(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sql_shell = Wsqluse('wdb', 'watchman', 'hect0r1337', '192.168.100.118')

    def test_get_sudo_pass(self):
        response = functions.get_sudo_password(self.sql_shell, 'core_settings')
        print(response)

if __name__ == '__main__':
    unittest.main()
