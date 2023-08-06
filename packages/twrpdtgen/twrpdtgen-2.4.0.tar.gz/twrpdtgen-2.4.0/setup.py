# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['twrpdtgen', 'twrpdtgen.utils']

package_data = \
{'': ['*'], 'twrpdtgen': ['templates/*']}

install_requires = \
['GitPython>=3.1.27,<4.0.0',
 'Jinja2>=3.1.1,<4.0.0',
 'sebaubuntu-libs>=1.0.4,<2.0.0']

setup_kwargs = {
    'name': 'twrpdtgen',
    'version': '2.4.0',
    'description': 'A Python library/script to automatically generate TWRP-compatible device tree from a boot/recovery image',
    'long_description': "# twrpdtgen\n\n[![PyPi version](https://img.shields.io/pypi/v/twrpdtgen)](https://pypi.org/project/twrpdtgen/)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/ae7d7a75522b4d079c497ff6d9e052d1)](https://www.codacy.com/gh/twrpdtgen/twrpdtgen/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=twrpdtgen/twrpdtgen&amp;utm_campaign=Badge_Grade)\n\nCreate a [TWRP](https://twrp.me/)-compatible device tree only from an Android recovery image (or a boot image if the device uses non-dynamic partitions A/B) of your device's stock ROM\nIt has been confirmed that this script supports images built starting from Android 4.4 up to Android 12\n\nRequires Python 3.8 or greater\n\n## Installation\n\n```sh\npip3 install twrpdtgen\n```\n\nLinux only: Be sure to have cpio installed in your system (Install cpio using `sudo apt install cpio` or `sudo pacman -S cpio` based on what package manager you're using)\n\n## Instructions\n\n```sh\npython3 -m twrpdtgen <path to image>\n```\n\nWhen an image is provided, if everything goes well, there will be a device tree at `output/manufacturer/codename`\n\nYou can also use the module in a script, with the following code:\n\n```python\nfrom twrpdtgen.device_tree import DeviceTree\n\n# Get image info\ndevice_tree = DeviceTree(image_path)\n\n# Dump device tree to folder\ndevice_tree.dump_to_folder(output_path)\n```\n\n## License\n\n```\n#\n# Copyright (C) 2022 The Android Open Source Project\n#\n# SPDX-License-Identifier: Apache-2.0\n#\n```\n",
    'author': 'Sebastiano Barezzi',
    'author_email': 'barezzisebastiano@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/twrpdtgen/twrpdtgen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
