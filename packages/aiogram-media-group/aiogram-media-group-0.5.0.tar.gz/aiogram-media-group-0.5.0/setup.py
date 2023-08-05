# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiogram_media_group', 'aiogram_media_group.storages']

package_data = \
{'': ['*']}

install_requires = \
['aiogram>2']

setup_kwargs = {
    'name': 'aiogram-media-group',
    'version': '0.5.0',
    'description': 'Aiogram handler for media groups (also known as albums)',
    'long_description': '# aiogram-media-group\n\naiogram handler for media groups (also known as albums)\n\n### Features\n\n- aiogram 3 support\n- Redis storage driver is supported and ready to work with multiple bot instances (aiogram 2 only)\n\n### Install\n\n```bash\npip install aiogram-media-group\n# or\npoetry add aiogram-media-group\n```\n\n### Usage\n\nMinimal usage example:\n\n```python\nfrom aiogram_media_group import media_group_handler\n\n@dp.message_handler(MediaGroupFilter(is_media_group=True), content_types=ContentType.PHOTO)\n@media_group_handler\nasync def album_handler(messages: List[types.Message]):\n    for message in messages:\n        print(message)\n```\n\nCheckout [examples](https://github.com/deptyped/aiogram-media-group/blob/main/examples) for complete usage examples\n',
    'author': 'deptyped',
    'author_email': 'deptyped@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/deptyped/aiogram-media-group',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
