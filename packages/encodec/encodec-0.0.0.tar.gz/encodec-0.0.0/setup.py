# author: adefossez
# Inspired from https://github.com/kennethreitz/setup.py

from pathlib import Path

from setuptools import setup

NAME = 'encodec'
DESCRIPTION = 'Deep learning based audio codec'

URL = 'https://github.com/facebookresearch/encodec'
EMAIL = 'defossez@fb.com'
AUTHOR = 'Alexandre Défossez'
REQUIRES_PYTHON = '>=3.8.0'
VERSION = "0.0.0"

HERE = Path(__file__).parent

REQUIRED = [i.strip() for i in open("requirements.txt")]

try:
    with open(HERE / "README.md", encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    py_modules=['encodec'],
    install_requires=REQUIRED,
    include_package_data=True,
    license='Creative Commons Attribution-NonCommercial 4.0 International',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)
