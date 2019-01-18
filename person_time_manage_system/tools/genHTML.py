#!/usr/bin/python
# -*- coding: utf-8 -*
from __future__ import print_function
import jinja2

template_path="./template.html"

def randerHTML(HTML_write_path,time_list,timeMin,timeMax,type_bar,user_name):
    template_str = ""
    with open(template_path, encoding="utf8") as f:
        template_str=f.read()
    template = jinja2.Template(template_str)
    rendered = template.render(WeekTimeSum=time_list,timeMin=timeMin,timeMax=timeMax,type_bar=type_bar,user_name=user_name)
    with open(HTML_write_path, 'w',encoding="utf8") as f:
        f.write(str(rendered))
    return str(rendered)

def main():
    time_list=[["11-111","1111"],["222","222"],["333","3333"]]
    rendered=randerHTML("index",time_list,None,None)
    print(rendered)

if __name__ == '__main__':
    main()

