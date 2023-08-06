# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['essnapshot']

package_data = \
{'': ['*']}

install_requires = \
['elasticsearch>=7.8.1,<8.0.0', 'pyyaml>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['essnapshot = essnapshot.cli:main']}

setup_kwargs = {
    'name': 'essnapshot',
    'version': '0.1.1',
    'description': 'Tool for Elasticsearch snapshot creation and rotation.',
    'long_description': "# essnapshot\n\n## installation\n\n### globally used python >= 3.6\n\n```\npip install essnapshot\n```\n\n### python2 and python >= 3.6 installed at the same time\n\n```\npip3 install essnapshot\n```\n\n## current state\n\nThe goal is to deliver a snapshot rotation tool for elasticsearch snapshots. \nThe functionality should be rather simple as most of it is already implemented in ES.\n\nSo I just stick to creating a repository, create snapshots within it and delete old ones.\nI assume that most people will use `cron` to call this script, so no daemon functionality \nor similar will be implemented. \n\nThe tool is not built to monitor the successfull write to disk of your snapshots.\nYou have to monitor the `STATE` of the snapshots yourself.\n\nAt the Moment only Python 3.6, 3.7 and 3.8 are supported. Support for older Python versions\nis not planned at the moment.\n\n## usage/configuration\n\nAt the moment the tool supports only one parameter (excecpt for help):\n\n````\nUsage: cli.py [options]\n\nOptions:\n  -h, --help            show this help message and exit\n  -c FILE, --config=FILE\n                        Path to configuration file. See example and\n                        documentation at https://github.com/gricertg/essnapshot\n````\n\nYou must provide a `yaml`configuration file like this:\n\n```\n---\nes_connections:\n  - host: 'localhost'\n    port: 9200\nrepository_name: 'essnapshot'\nrepository:\n  type: 'fs'\n  settings:\n    location: '/mnt/snapshot'\n    compress: 'true'\nretention_time: '7d'\n```\n\nThe parameters should be self explanatory (if you're familiar with ES).\n\nA short help to get you started with the main parameters:\n\n### es_connections\n\nA list(array) of hashes(dictionaries) to which ES can connect to.\nTo understand how this works see the [Elasticsearch API documentation](https://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch).\nEach Host is a `Dictionary` in the `List`.\nThe Options per Host are the ones for `Urllib3HttpConnection`s.\nSee [Connection](https://elasticsearch-py.readthedocs.io/en/master/connection.html#elasticsearch.Urllib3HttpConnection) in the API documentation.\nHere you can configre authentication too.\n\nPlease ensure that this configuration file can only be read by the user/container\ndesignated for the backup if you put any credentials in this configuration file\n(and please don't put it into a public git repository).\n\n### repository_name\n\nThis is the name of the repository which will be created and the snapshots created in.\n\n### repository\n\nThis represents the configuration of the ES repository. It's a representation of the JSON sent to ES\nand is described in the ES documentation in [Register a snapshot repository](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-register-repository.html).\n\n### retention_time\n\nThe maximum backup age before snapshots will be deleted.\n\n\n## execution\n\nThe script is intended to run at regular intervals via `cron`. I recommend to created a\ndedicated user for the snapshots and that only this user can access the configuration file.\n\nA crontab entry for this user could look like this:\n\n```\n4 1 * * * essnapshot > /dev/null\n```\n\nSTDOUT is suppressed. If any error occurs the error message will be sent via mail\nto the snapshot user (depending on your configuration of the system).\n\n## development\n\n- the feature set should be kept small\n- the project should have a high test coverage (there is still room to improve it!)\n- try to hold on to styleguides and improve code quality\n\nYou need [poetry](https://python-poetry.org) and [docker](https://www.docker.com) (for tests) installed. \n\nNecessary improvements and development steps should be documentated as github issues.\n",
    'author': 'gricertg',
    'author_email': 'gricertg@posteo.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gricertg/essnapshot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
