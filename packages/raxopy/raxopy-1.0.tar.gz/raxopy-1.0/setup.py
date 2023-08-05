import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '1.0' 
PACKAGE_NAME = 'raxopy'
AUTHOR = 'raxo1710' 
AUTHOR_EMAIL = 'raxopy@gmail.com' 

DESCRIPTION = 'Librería creada por un adolescente, para agilizar sobretodo procesos matemáticos.' 
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8') 


INSTALL_REQUIRES = [
      ]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
    include_package_data=True
)