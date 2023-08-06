# info@codebasedlearning.dev, a.voss@fh-aachen.de

import unittest
#import importlib.metadata

import cbl_tools
#from cbl_tools import versioning
from cbl_tools.versioning import semver_of, package_semver_of, __version__ as cbl_tools_versioning_version


class VersioningTestCase(unittest.TestCase):
    def test_versioning_import(self):
        self.assertEqual(1,1)


if __name__ == '__main__':
    unittest.main()
