#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# DevVersion: Python3.9
# Date: 2022-07-21 09:13
# PyCharm|setup

from setuptools import (setup, find_packages)

requirements = ['MultiCloudOCR==1.0', 'matplotlib', 'numpy', 'time']

setup(
    # 包名
    name="MultiOCRPlot",
    # 版本
    version="2.0",
    # github地址[我学习的样例地址]
    url='https://github.com/snowroll/python-sdk.git',
    # 包的解释地址
    long_description=open('ReadMe.md', encoding='utf-8').read(),
    # 需要包含的子包列表
    packages=find_packages(),
    install_requires=requirements,  # 安装自定义工具包需要依赖的包
    python_requires='>=3.5'         # 自定义工具包对于python版本的要求
)
