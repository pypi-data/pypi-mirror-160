from gettext import install
from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))


long_description = "\n I'm Vu Vui Ve hehe" 
    
DESCRIPTION = "Hello world is easy"

## setting up
setup(
    name="vuvuive_helloworld_2",
    version="1.0.2",
    author="Hoang Xuan Vu",
    author_email="xuanvuzzz2601@gmail.com",
    description=DESCRIPTION,
    long_description= long_description,
    packages= find_packages(),
    install_requires =[],
    keywords=["python", "hello world", "hello python"],    
    classifiers=[
        "Development Status :: 1 - Planning",
        "Development Status :: 2 - Pre-Alpha",
        "Framework :: IPython",
        "Programming Language :: Cython", 
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: Implementation",
        "Intended Audience :: System Administrators",
        "Operating System :: Microsoft",
        "Operating System :: MacOS"
    ]
)
    