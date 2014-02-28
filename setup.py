#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='mikoto',
      version='0.0.4',
      keywords=('markdown', 'Douban'),
      description='better Markdown Render',
      long_description='better Markdown Render, Support emoji,Task List,GFM',
      license='New BSD',

      url='https://github.com/qingfeng/mikoto',
      author='qingfeng',
      author_email='qingfeng@douban.com',

      packages=find_packages(exclude=['tests']),
      platforms='any',
      install_requires=['Pygments',
                        'chardet',
                        'pytest',
                        'pytest-random',
                        'misaka==1.0.3'
                        ],
      dependency_links=[
            'https://github.com/qingfeng/misaka/archive/master.zip#egg=misaka-1.0.3'
        ],
      entry_points={
            "console_scripts": [
                  "mikoto = mikoto:main",
            ],
      }
)
