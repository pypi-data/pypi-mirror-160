# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zdppy_orm']

package_data = \
{'': ['*']}

install_requires = \
['zdppy-mysql>=0.2.5,<0.3.0']

setup_kwargs = {
    'name': 'zdppy-orm',
    'version': '0.1.4',
    'description': 'Python的ORM框架',
    'long_description': '# zdppy_orm\n\nPython专用的ORM框架\n\n## 版本历史\n\n- v0.1.3 2022/07/15 新增：数据库连接池',
    'author': 'zhangdapeng520',
    'author_email': '1156956636@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zhangdapeng520/zdppy_orm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
