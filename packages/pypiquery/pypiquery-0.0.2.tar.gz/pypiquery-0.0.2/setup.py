# -*- coding: utf-8 -*-

import re
import ast

from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('pypiquery.py', 'rb') as f:
    _version = str(ast.literal_eval(_version_re.search(f.read().decode('utf-8')).group(1)))


with open('./README.md', encoding='utf-8') as f:
    _long_desc = f.read()


setup(
    name = 'pypiquery',
    version = _version,
    description = '通过查询 pypi.org 网站获取指定软件包历史版本信息。',
    long_description = _long_desc,
    long_description_content_type = 'text/markdown',
    author = 'do0ob',
    license = 'MIT',
    install_requires = [
        'keyboard',
        'requests',
        'beautifulsoup4'
    ],
    py_modules = ['pypiquery',],
    entry_points = {
        'console_scripts': [
            'pypiquery = pypiquery:main',
            'ppq = pypiquery:main',
        ]
    },
    classifiers = [
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'
    ]
)