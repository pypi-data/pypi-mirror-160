#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# DevVersion: Python3.9
# Date: 2022-07-21 09:13
# PyCharm|setup

from setuptools import (setup, find_packages)

setup(
    # 包名
    name="MultiOCRPlot",
    # 版本
    version="1.0",
    # github地址[我学习的样例地址]
    url='https://github.com/snowroll/python-sdk.git',
    # 包的解释地址
    long_description=open('ReadMe.md', encoding='utf-8').read(),
    # 需要包含的子包列表
    packages=find_packages()
)
