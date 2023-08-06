# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sbermarket_api']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'sbermarket-api',
    'version': '0.0.2',
    'description': 'Not official python client for product market sbermarket API.',
    'long_description': '# sbermarket-api\n\n<div align="center">\n\n[![Build status](https://github.com/nov1kov/sbermarket-api/workflows/build/badge.svg?branch=master&event=push)](https://github.com/nov1kov/sbermarket-api/actions?query=workflow%3Abuild)\n[![Python Version](https://img.shields.io/pypi/pyversions/sbermarket-api.svg)](https://pypi.org/project/sbermarket-api/)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/nov1kov/sbermarket-api/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/nov1kov/sbermarket-api/blob/master/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/nov1kov/sbermarket-api/releases)\n[![License](https://img.shields.io/github/license/nov1kov/sbermarket-api)](https://github.com/nov1kov/sbermarket-api/blob/master/LICENSE)\n![Coverage Report](assets/images/coverage.svg)\n\nNot official python client for product market Sbermarket.\n\n</div>\n\n## Задачи что преследовал:\n\n1. Поиск самого дешевого товара среди магазинов вокруг.\n2. Отлеживание в целом цен на продукты.\n3. Сделать алерт на дешевые товары.\n4. Вести статистику на цены товаров.\n\n## Что внутри?\n\nТокен получается только из статического js скрипта. Где содержится JSON вида:\n```json\n{"api-version":"3.0","client-token":"TOKEN","is-storefront-ssr":l.sk}\n```\nСкорее всего он у всех одинаковый.\n\n## Installation\n\n```bash\npip install -U sbermarket-api\n```\n\nor install with `Poetry`\n\n```bash\npoetry add sbermarket-api\n```\n\n## 📈 Releases\n\nYou can see the list of available releases on the [GitHub Releases](https://github.com/nov1kov/sbermarket-api/releases) page.\n\nWe follow [Semantic Versions](https://semver.org/) specification.\n\nWe use [`Release Drafter`](https://github.com/marketplace/actions/release-drafter). As pull requests are merged, a draft release is kept up-to-date listing the changes, ready to publish when you’re ready. With the categories option, you can categorize pull requests in release notes using labels.\n\n### List of labels and corresponding titles\n\n|               **Label**               |  **Title in Releases**  |\n| :-----------------------------------: | :---------------------: |\n|       `enhancement`, `feature`        |       🚀 Features       |\n| `bug`, `refactoring`, `bugfix`, `fix` | 🔧 Fixes & Refactoring  |\n|       `build`, `ci`, `testing`        | 📦 Build System & CI/CD |\n|              `breaking`               |   💥 Breaking Changes   |\n|            `documentation`            |    📝 Documentation     |\n|            `dependencies`             | ⬆️ Dependencies updates |\n\nYou can update it in [`release-drafter.yml`](https://github.com/nov1kov/sbermarket-api/blob/master/.github/release-drafter.yml).\n\nGitHub creates the `bug`, `enhancement`, and `documentation` labels for you. Dependabot creates the `dependencies` label. Create the remaining labels on the Issues tab of your GitHub repository, when you need them.\n\n## 🛡 License\n\n[![License](https://img.shields.io/github/license/nov1kov/sbermarket-api)](https://github.com/nov1kov/sbermarket-api/blob/master/LICENSE)\n\nThis project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/nov1kov/sbermarket-api/blob/master/LICENSE) for more details.\n\n## 📃 Citation\n\n```bibtex\n@misc{sbermarket-api,\n  author = {Nov1kov},\n  title = {Not official python client for product market sbermarket API.},\n  year = {2022},\n  publisher = {GitHub},\n  journal = {GitHub repository},\n  howpublished = {\\url{https://github.com/nov1kov/sbermarket-api}}\n}\n```\n\n## Credits [![🚀 Your next Python package needs a bleeding-edge project structure.](https://img.shields.io/badge/python--package--template-%F0%9F%9A%80-brightgreen)](https://github.com/TezRomacH/python-package-template)\n\nThis project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template)\n\n## Alternatives\n\n1. Sbermarket client on TypeScript https://github.com/x0rium/sbermarket-api\n',
    'author': 'Nov1kov',
    'author_email': 'spellh1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nov1kov/sbermarket-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
