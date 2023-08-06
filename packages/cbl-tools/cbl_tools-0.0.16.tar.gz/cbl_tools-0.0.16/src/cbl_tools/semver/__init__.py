# info@codebasedlearning.dev, a.voss@fh-aachen.de

import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))  # enables relative local imports

import __version__


def make_stage_version(stage: str = "") -> str:
    """Example package function. Combine package version with stage (if given)."""
    return f"{__version__.__version__}{f'-{stage}' if stage else ''}"


if __name__ == "__main__":
    print(f"SemVer: {make_stage_version()}")
    print(f"Stage Version: {make_stage_version('rc')}")


"""

https://packaging.python.org/en/latest/tutorials/packaging-projects/
https://choosealicense.com/licenses/mit/
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps cbl_test_package==1.2.3
https://itsmycode.com/importerror-attempted-relative-import-with-no-known-parent-package/

python3 -m build  
python3 -m twine upload --repository testpypi dist/* 
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps cbl_test_package@1.2.3 

https://packaging.python.org/en/latest/tutorials/packaging-projects/

python3 -m build  
python3 -m twine upload dist/* 
python3 -m pip install cbl_test_package==1.2.3 
pip install cbl-test-package==1.2.3
pip install cbl-test-package==2.3.4

pip install cbl_tools
"""
