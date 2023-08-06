from ast import keyword
from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='snrandymylib',
    version='0.1.0',
    description='A very basic calculator library',
    long_description=open('README.txt').read()+'\n\n'+open('CHANGELOG.txt').read(),
    author='snrandy',
    author_email='nfonandrew73@gmail.com',
    url='',
    license='MIT',
    packages=find_packages(),
    keywords='calculator',
    install_requires=[''],

)