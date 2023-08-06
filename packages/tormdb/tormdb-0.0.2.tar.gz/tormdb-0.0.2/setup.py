# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'packages'}

packages = \
['tormdb']

package_data = \
{'': ['*']}

install_requires = \
['dataset>=1.3.2,<2.0.0']

setup_kwargs = {
    'name': 'tormdb',
    'version': '0.0.2',
    'description': '',
    'long_description': "# tormdb\n\n`tormdb` stands for Transposed Object Relational Mapping Database.\n`tormdb` stores your objects into SQLite for maintaining the accessibility across runtimes without you inheriting any customized Classes.\n\n## Usage\n\n### Save\n\n`tormdb.save(<object>)`\n\n```\nimport dataclasses\nfrom typing import List\n\nimport tormdb\n\n\n@dataclasses.dataclass\nclass Person:\n    name: str\n    age: int\n\n\n@dataclasses.dataclass\nclass Family:\n    husband: Person\n    wife: Person\n    children: List[Person] = dataclasses.field(default_factory=list)\n\n\nwife: Person = Person('Catherine', 24)\nhusband: Person = Person('Chris', 24)\ndaughter: Person\nson: Person\ndaughter = son = Person('Alex', 0)\n\nfamily = Family(\n    husband=husband,\n    wife=wife,\n    children=[daughter, son])\n\ntormdb.save(family)\n```\n\n### Load\n\n`<object> = tormdb.load(<List[Class]>)`\n\n```\nimport dataclasses\nfrom typing import List, Optional\n\nimport tormdb\n\n\n@dataclasses.dataclass\nclass Person:\n    name: str\n    age: int\n\n\n@dataclasses.dataclass\nclass Family:\n    husband: Person\n    wife: Person\n    children: List[Person] = dataclasses.field(default_factory=list)\n\n\nfamily: Optional[Family] = tormdb.load([Family, Person])\n```\n",
    'author': 'Johann Chang',
    'author_email': 'mr.changyuheng@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/changyuheng/tormdb.py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
