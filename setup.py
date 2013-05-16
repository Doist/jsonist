# -*- coding: utf-8 -*-
import os
from setuptools import setup

def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except:
        return ''

setup(
    name='jsonist',
    version='1.0',
    author='Amir Salihefendic',
    author_email='amix@amix.dk',
    url='http://github.com/Doist/jsonist',
    description='Somewhat useful wrapper around cjson',
    long_description=read('README.rst'),
    py_modules=['jsonist'],
    install_requires=[
        'python-cjson',
    ],
)
