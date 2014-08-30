#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests']
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


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
                        'misaka>=1.0.2',
                        'docutils'],
      tests_require=['pytest',
                     'pytest-random'],
      cmdclass={'test': PyTest},
      entry_points={
            "console_scripts": [
                  "mikoto = mikoto.__main__:main",
            ],
      }
)
