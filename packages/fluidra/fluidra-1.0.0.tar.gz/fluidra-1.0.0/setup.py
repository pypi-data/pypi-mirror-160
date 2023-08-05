from setuptools import setup, find_packages
import codecs
import os


VERSION = '1.0.0'
DESCRIPTION = 'Fluidra Webtouch Automation Package'
LONG_DESCRIPTION = 'Package for accessing elements in webtouch to be able to automate tests'

# Setting Up
setup(
    name="fluidra",
    version=VERSION,
    author="Anthony Kahley",
    author_email="akahley@fluidra.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['selenium'],
    keywords=['fluidra','automation','test'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)
