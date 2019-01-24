#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/16 14:02
# @Author : wangchong
# @Email: chongwangcc@gmail.com
# @File : App.py
# @Software: PyCharm
from setuptools import setup, find_packages

requires=[]
with open("requirements.txt", mode="r", encoding="utf8") as f:
    for line in f.readlines():
        requires.append(line.strip())

setup(name='person_time_manage_system',

      version='0.1',

      url='https://github.com/chongwangcc/person_time_manage_system',

      license='MIT',

      author='chongwangcc',

      author_email='chongwangcc@gmail.com',

      description='analysis where is you  time spent?',

      packages=find_packages(exclude=['person_time_manage_system']),

      include_package_data=True,

      long_description=open('README.md', encoding="utf8").read(),

      zip_safe=False,

      setup_requires=requires,

       package_dir={'': 'person_time_manage_system'}
      )