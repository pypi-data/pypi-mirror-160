import setuptools
from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

NAME = 'lambler'
VERSION = '0.0.6'
URL = 'https://github.com/SSripilaipong/lambler'
LICENSE = 'MIT'
AUTHOR = 'SSripilaipong'
EMAIL = 'SHSnail@mail.com'

setup(
    name=NAME,
    version=VERSION,
    packages=[package for package in setuptools.find_packages() if
              package == "lambler" or package.startswith('lambler.')],
    url=URL,
    license=LICENSE,
    author=AUTHOR,
    author_email=EMAIL,
    description=None,
    long_description=None,
    python_requires='>=3.8',
    install_requires=requirements,
    classifiers=[],
)
