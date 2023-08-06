# info@codebasedlearning.dev, a.voss@fh-aachen.de

import unittest
#from importlib.metadata import version
import importlib.metadata

import cbl_tools
from cbl_tools import semver
from cbl_tools.semver import make_stage_version, __version__ as cbl_tools_base_version


class MyTestCase(unittest.TestCase):
    def test_something(self):
        cbl_tools_lib_version = importlib.metadata.version('cbl_tools')
        self.assertEqual(f"{cbl_tools_lib_version}", cbl_tools_base_version.__version__)

        self.assertEqual(f"{cbl_tools_lib_version}", cbl_tools.semver.make_stage_version())
        self.assertEqual(f"{cbl_tools_lib_version}", semver.make_stage_version())
        self.assertEqual(f"{cbl_tools_lib_version}", make_stage_version())

        stage = "rc"
        self.assertEqual(f"{cbl_tools_lib_version}-{stage}", make_stage_version(stage))


if __name__ == '__main__':
    unittest.main()
