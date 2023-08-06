# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['konstantin_docs',
 'konstantin_docs.dia',
 'konstantin_docs.dia.c4',
 'konstantin_docs.dia.c4.sprite_lib',
 'konstantin_docs.dia.c4.sprite_lib.tupadr3_lib',
 'konstantin_docs.dia.mermaid_er',
 'konstantin_docs.service']

package_data = \
{'': ['*']}

install_requires = \
['requests', 'typing_extensions']

setup_kwargs = {
    'name': 'konstantin-docs',
    'version': '0.0.12',
    'description': 'Генерация документации',
    'long_description': '# kroki-python\n\nLib for interaction with https://kroki.io\n\n## Запустить тест:\n\n```sh\npoetry run poe docs\n```\n\nИли запусить task в vs code - F1 -> Task: Run task -> docs\n\n## Загрузить пакет в pypi\n\nСобрать и опубликовать пакет\n\n```sh\npoetry build && poetry publish\n```\n\nЛогин: konstantin-dudersky\n\n## Задача poe\n\nДописать в файл pyproject.toml:\n\n```toml\ndocs = {script = "konstantin_docs.main:generate_images(path_src=\'test/dia_src\', path_dist=\'test/dia_dist\')"}\n```\n\n## Создать задачу vscode\n\nВ файле .vscode/tasks.json:\n\n```json\n{\n  "version": "2.0.0",\n  "tasks": [\n    {\n      "label": "docs",\n      "type": "shell",\n      "command": "poetry run poe docs"\n    }\n  ]\n}\n```\n',
    'author': 'Konstantin-Dudersky',
    'author_email': 'Konstantin.Dudersky@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Konstantin-Dudersky/konstantin_docs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
