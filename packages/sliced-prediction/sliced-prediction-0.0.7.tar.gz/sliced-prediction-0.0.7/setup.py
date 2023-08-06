# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sliced_prediction']

package_data = \
{'': ['*']}

install_requires = \
['beartype>=0.10.4,<0.11.0', 'loguru>=0.6.0,<0.7.0', 'sahi>=0.10.1,<0.11.0']

extras_require = \
{':sys_platform == "linux"': ['yolov5>=6.1.6,<7.0.0']}

entry_points = \
{'console_scripts': ['sliced-prediction = '
                     'sliced_prediction.sliced_prediction:app']}

setup_kwargs = {
    'name': 'sliced-prediction',
    'version': '0.0.7',
    'description': 'Provides a way to perform sliced inferencing on a directory of images',
    'long_description': '# sliced-prediction\n## Installation & Use\n\n```shell\n# Install sliced-prediction\n> pip install sliced-prediction\n\n> sliced-prediction --help\n```\n\n## Example\n```shell\nsliced-prediction \\\n--overlap_width_ratio 0 \\\n--overlap_height_ratio 0 \\\n--slice_width 1024 \\\n--slice_height 1024 \\\n--input_directory ./tests/data \\\n--output_manifest_file ./tmp/manifest.jsonl \\\n--model_path ./tmp/best.pt \\\n--confidence_threshold .2 \\\n--device cpu\n```',
    'author': 'Michael Mohamed',
    'author_email': 'michael@foundationstack.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fsai-dev/fsai-cli-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
