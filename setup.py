#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

__description__ = "A tool used to parse, encrypt and decrypt Bitmap file easily."
__license__ = "MIT"


setup(
    name='encbmp',
    version='0.0.6',
    description=__description__,
    author='ZhanPw',
    author_email='zhanpw97@gmail.com',
    license=__license__,
    packages=find_packages(),
    install_requires=['Crypto',
                      'Pillow'],
    platforms=["all"],
    url='https://github.com/ZhanPwBibiBibi/AES_bmp',
    classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.6",
    ],
)