"""
本类是用来导出所做项目的依赖
"""
import os

path = os.path.dirname(os.path.abspath(__name__))

os.system(f'pipreqs "{path}" --encoding=utf8 --force --proxy="http://127.0.0.1:30809"')
