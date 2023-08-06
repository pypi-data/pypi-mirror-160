# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['plugin']
install_requires = \
['Jinja2>=3.0.3,<4.0.0', 'requests>=2.27.1,<3.0.0']

entry_points = \
{'mkdocs.plugins': ['drawio_file = '
                    'mkdocs_drawio_file.plugin:drawio_file_plugin']}

setup_kwargs = {
    'name': 'mkdocs-drawio-file',
    'version': '1.2.0',
    'description': 'Mkdocs plugin that renders .drawio files',
    'long_description': '# Embedding files of Diagrams.net (Draw.io) into MkDocs\n\n[![](https://github.com/onixpro/mkdocs-drawio-file/workflows/Deploy/badge.svg)](https://github.com/onixpro/mkdocs-drawio-file/actions)\n[![PyPI](https://img.shields.io/pypi/v/mkdocs-drawio-file)](https://pypi.org/project/mkdocs-drawio-file/)\n\n\n\n[Buy me a 🍜](https://www.buymeacoffee.com/SergeyLukin)\n\n## Features\n\nWith the plugin configured, you can now proceed to embed images by simply embedding the `*.drawio` diagram file as you would with any image file:\n\n```markdown\n![My alt text](my-diagram.drawio)\n```\n\n\n## Dependencies\n\n## Setup\n\nInstall plugin using pip:\n\n```\npip install mkdocs-drawio-file\n```\n\nNext, add the plugin to your `mkdocs.yml`\n\n```yaml\nplugins:\n  - drawio_file\n```\n',
    'author': 'Sergey Lukin',
    'author_email': 'onixpro@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/onixpro/mkdocs-drawio-file/',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
