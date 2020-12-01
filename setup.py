# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elysian_wishlist',
 'elysian_wishlist.modules',
 'elysian_wishlist.modules.cron',
 'elysian_wishlist.modules.cronChart',
 'elysian_wishlist.modules.crud',
 'elysian_wishlist.modules.forum',
 'elysian_wishlist.modules.third_party_api',
 'elysian_wishlist.modules.user_login']

package_data = \
{'': ['*'],
 'elysian_wishlist': ['static/graphics/*',
                      'static/images/*',
                      'static/styles/*',
                      'templates/*']}

install_requires = \
['Flask-SQLAlchemy>=2.4.4,<3.0.0',
 'Flask>=1.1.2,<2.0.0',
 'aiohttp>=3.6.2,<4.0.0',
 'bs4>=0.0.1,<0.0.2',
 'flask_apscheduler>=1.11.0,<2.0.0',
 'gunicorn>=20.0.4,<21.0.0',
 'matplotlib>=3.3.3,<4.0.0',
 'psycopg2-binary>=2.8.6,<3.0.0',
 'requests>=2.24.0,<3.0.0',
 'sqlalchemy_serializer>=1.3.4,<2.0.0']

setup_kwargs = {
    'name': 'elysian-wishlist',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Naeem Meman',
    'author_email': 'naeemmeman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
