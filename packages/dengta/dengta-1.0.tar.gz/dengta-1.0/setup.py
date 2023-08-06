import setuptools
from pathlib import Path

setuptools.setup(
    name='dengta',
    version=1.0,
    long_description=Path('README.md').read_text(),
    description='This is a program(doge), 这是个看灯塔的程序......',
    python_requires='>3.1',
    packages=setuptools.find_packages(exclude=['tests','data']),
    classifiers=['Development Status :: 4 - Beta',],
    author='algj0511',
    author_email='algj0511@126.com'
)