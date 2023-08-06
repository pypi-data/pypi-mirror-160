# info@codebasedlearning.dev, a.voss@fh-aachen.de
import importlib
import unittest
from importlib.metadata import version

import cbl_tools
#from cbl_tools import semver, __version__
#from cbl_tools import semver

class MyTestCase(unittest.TestCase):
    def test_something(self):
        cbl_tools_version = version('cbl_tools')
        #self.assertEqual(f"{cbl_tools_version}", __version__.__version__)

        #self.assertEqual(f"{cbl_tools_version}", semver.make_stage_version())

        stage = "rc"
        #self.assertEqual(f"{cbl_tools_version}-{stage}", semver.make_stage_version(stage))
        #print(__version__.__version__)
        #s = importlib.metadata.version()
        print(cbl_tools.semver.make_stage_version())


if __name__ == '__main__':
    unittest.main()
