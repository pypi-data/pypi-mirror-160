# a.voss@fh-aachen.de

#import __version__
from __version__ import __version__


def version(n: int) -> str:
    return f"{__version__}-{n}"


if __name__ == "__main__":
    print(f"Version: {version(25)}")


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
