# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['twiskey']
install_requires = \
['Misskey.py>=4.1.0,<5.0.0',
 'click>=8.1.3,<9.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'tweepy>=4.10.0,<5.0.0']

setup_kwargs = {
    'name': 'twiskey',
    'version': '0.1.0',
    'description': 'TwitterとMisskeyに同時投稿出来るコマンドです。',
    'long_description': None,
    'author': 'Comamoca',
    'author_email': 'comamoca.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
