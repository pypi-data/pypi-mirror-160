import unittest

# import cbl_tools.tools
from cbl_tools import tools


class MyTestCase(unittest.TestCase):
    def test_something(self):
        #self.assertEqual(True, False)  # add assertion here
        print(tools.version(12))


if __name__ == '__main__':
    unittest.main()
