#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/2/13 11:41 
# @Author : wangchong 
# @Email: chongwangcc@gmail.com
# @File : est.py 
# @Software: PyCharm
import pandas as pd
data = pd.DataFrame({'id':['学习','学习','整理','D','E','F'],'value':['学习','学习','整理','D','E','F']})
print(data)
print(data.columns)
data1 = data.groupby(by='id')['value'].sum()
print(data1)
