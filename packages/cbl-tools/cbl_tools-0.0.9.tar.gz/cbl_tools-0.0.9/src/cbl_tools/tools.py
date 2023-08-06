# a.voss@fh-aachen.de

#import __version__
#from __version__ import __version__

#import .version
from version import __version__ as cbl_version

def version_n(n: int) -> str:
    return f"{cbl_version}-{n}"


if __name__ == "__main__":
    print(f"Version: {version_n(25)}")


"""

https://packaging.python.org/en/latest/tutorials/packaging-projects/
https://choosealicense.com/licenses/mit/
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps cbl_test_package==1.2.3


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
