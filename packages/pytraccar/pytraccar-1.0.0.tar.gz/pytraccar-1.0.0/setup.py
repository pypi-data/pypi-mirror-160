# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytraccar', 'pytraccar.models']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6,<4.0', 'pydantic>=1,<2']

setup_kwargs = {
    'name': 'pytraccar',
    'version': '1.0.0',
    'description': '',
    'long_description': '# [pytraccar](https://pypi.org/project/pytraccar/)\n\n[![codecov](https://codecov.io/gh/ludeeus/pytraccar/branch/main/graph/badge.svg)](https://codecov.io/gh/ludeeus/pytraccar)\n![python version](https://img.shields.io/badge/Python-3.9=><=3.10-blue.svg)\n[![PyPI](https://img.shields.io/pypi/v/pytraccar)](https://pypi.org/project/pytraccar)\n![Actions](https://github.com/ludeeus/pytraccar/workflows/Actions/badge.svg?branch=main)\n\n\n## Installation\n\n```bash\npython3 -m install pytraccar\n```\n\nLook at the file `example.py` for a usage example.\n\n\n## Contribute\n\n**All** contributions are welcome!\n\n1. Fork the repository\n2. Clone the repository locally and open the devcontainer or use GitHub codespaces\n3. Do your changes\n4. Lint the files with `make lint`\n5. Ensure all tests passes with `make test`\n6. Ensure 100% coverage with `make coverage`\n7. Commit your work, and push it to GitHub\n8. Create a PR against the `main` branch\n',
    'author': 'Ludeeus',
    'author_email': 'ludeeus@ludeeus.dev',
    'maintainer': 'Ludeeus',
    'maintainer_email': 'ludeeus@ludeeus.dev',
    'url': 'https://github.com/ludeeus/pytraccar',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
