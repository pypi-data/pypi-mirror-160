#!/usr/bin/env python
from distutils.core import setup
from setuptools import find_packages
setup(
    name='ccproxy',
    version='0.0.1',
    description='get free proxy',
    long_description='get free proxy!',
    author='duan',
    author_email='2096258508@qq.com',
    license='MIT License',
    packages=find_packages(),
    install_requires=['requests', 'lxml']
)
