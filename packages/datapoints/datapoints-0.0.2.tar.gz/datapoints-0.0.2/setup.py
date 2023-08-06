# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datapoints', 'datapoints.utils']

package_data = \
{'': ['*']}

install_requires = \
['asyncua==0.9.94']

setup_kwargs = {
    'name': 'datapoints',
    'version': '0.0.2',
    'description': 'Управление данными',
    'long_description': '# data_connector\n\n## Описание\n\n- signal - элементарный тип данных. Кроме значения, хранит также время последнего чтения / записи, код качества, единицу измерения, пределы измерения.\n\n- channel - объект для связи signal с периферийными значениями.\n\n- driver - управляет объектами channel.\n\n- datapoint - объект для храненения данных. Связывает signal и channel.\n\n## Разработка\n\nУстановить виртуальное окружение\n\n```sh\npoetry install\n```\n\nОпубликовать пакет\n\n```sh\npoetry build && poetry publish\n```\n',
    'author': 'Konstantin-Dudersky',
    'author_email': 'Konstantin.Dudersky@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Konstantin-Dudersky/data_connector',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.0,<3.11.0',
}


setup(**setup_kwargs)
