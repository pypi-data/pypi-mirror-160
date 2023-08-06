# info@codebasedlearning.dev, a.voss@fh-aachen.de

import unittest
from importlib.metadata import version

from cbl_tools import tools


class MyTestCase(unittest.TestCase):
    def test_something(self):
        n = 12
        cbl_tools_version = version('cbl_tools')
        self.assertEqual(f"{cbl_tools_version}-{n}", tools.version_n(n))


if __name__ == '__main__':
    unittest.main()
