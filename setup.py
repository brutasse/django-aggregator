# -*- coding: utf-8 -*-
import os
from distutils.core import setup
from setuptools import find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-aggregator',
    version='0.1',
    author=u'Bruno Renié',
    author_email='bruno@renie.fr',
    packages=find_packages(),
    include_package_data=True,
    url='http://github.com/brutasse/django-aggregator',
    license='BSD',
    description='A planet app for your Django project',
    long_description=read('README.rst'),
    zip_safe=False,
)
