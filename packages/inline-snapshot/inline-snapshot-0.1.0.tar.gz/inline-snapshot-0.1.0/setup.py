# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['inline_snapshot']

package_data = \
{'': ['*']}

install_requires = \
['asttokens>=2.0.5,<3.0.0', 'executing>=0.9.0,<0.10.0']

entry_points = \
{'pytest11': ['inline_snapshot = inline_snapshot.pytest_pluin']}

setup_kwargs = {
    'name': 'inline-snapshot',
    'version': '0.1.0',
    'description': 'compare test results with snapshots from previous test runs',
    'long_description': 'inline-snapshot\n======================\n\ncreate and update inline snapshots in your code.\n\nFeatures\n--------\n\n* records current values during [pytest](https://github.com/pytest-dev/pytest) run `--update-snapshots=new`.\n* values are stored in the source code and not in separate files.\n* values can be updated with `--update-snapshots=failing`.\n\n\nInstallation\n------------\n\nYou can install "inline-snapshot" via [pip](https://pypi.org/project/pip/) from [PyPI](https://pypi.org/project)::\n\n    $ pip install inline-snapshot\n\n\nUsage\n-----\n\nYou can use `snapshot()` instead of the value which you want to compare with.\n\n``` python\ndef something():\n    return 1548 * 18489\n\n\ndef test_something():\n    assert something() == snapshot()\n```\n\nYou can now run the tests and record the correct values.\n\n    $ pytest --update-snapshots=new\n\n``` python\ndef something():\n    return 1548 * 18489\n\n\ndef test_something():\n    assert something() == snapshot(28620972)  # snapshot gets recorded\n```\n\nYour tests will break if you change your code later.\nYou get normal pytest failure messages, because `snapshot(value)` just returns `value` during normal test runs.\n\n``` python\ndef something():\n    return (1548 * 18489) // 18  # changed implementation\n\n\ndef test_something():\n    assert something() == snapshot(28620972)  # this will fail now\n```\n\nMaybe that is correct and you should fix your code, or\nyour code is correct and you want to update your test results.\n\n    $ pytest --update-snapshots=failing\n\nPlease verify the new results. `git diff` will give you a good overview over all changed results.\nUse `pytest -k test_something --update-snapshots=failing` if you only want to change one test.\n\n``` python\ndef something():\n    return (1548 * 18489) // 18\n\n\ndef test_something():\n    assert something() == snapshot(1590054)\n```\n\nThe code is generated without any formatting.\nUse the formatter of your choice to make it look nice,\nor maybe use [darker](https://pypi.org/project/darker/) if you only want to format your changes.\n\n\nMore than just numbers\n----------------------\n\nRequirements:\n* `snapshot(value)` can only be used for `==` comparison\n* the values should be comparable with `==`\n* `repr(value)` should return valid python code\n\n\nYou can use almost any python datatype and also complex values like `datatime.date` (you have to import the right modules to match the `repr()` output).\n\n``` python\nfrom inline_snapshot import snapshot\nimport datetime\n\n\ndef something():\n    return {\n        "name": "hello",\n        "one number": 5,\n        "numbers": list(range(10)),\n        "sets": {1, 2, 15},\n        "datetime": datetime.date(1, 2, 22),\n        "complex stuff": 5j + 3,\n        "bytes": b"fglecg\\n\\x22",\n    }\n\n\ndef test_something():\n    assert something() == snapshot(\n        {\n            "name": "hello",\n            "one number": 5,\n            "numbers": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],\n            "sets": {1, 2, 15},\n            "datetime": datetime.date(1, 2, 22),\n            "complex stuff": (3 + 5j),\n            "bytes": b\'fglecg\\n"\',\n        }\n    )\n```\n\n\n`snapshot()` can also be used in loops.\n\n``` python\nfrom inline_snapshot import snapshot\n\n\ndef test_loop():\n    for name in ["Mia", "Ava", "Leo"]:\n        assert len(name) == snapshot(3)\n```\n\n… and more to come :grin:.\n\nContributing\n------------\nContributions are very welcome.\nTests can be run with [tox](https://tox.readthedocs.io/en/latest/).\nPlease use [pre-commit](https://pre-commit.com/) for your commits.\n\nLicense\n-------\n\nDistributed under the terms of the [MIT](http://opensource.org/licenses/MIT) license, "inline-snapshot" is free and open source software\n\n\nIssues\n------\n\nIf you encounter any problems, please [file an issue](https://github.com/15r10nk/pytest-inline-snapshot/issues) along with a detailed description.\n',
    'author': 'Frank Hoffmann',
    'author_email': '15r10nk@polarbit.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/15r10nk/inline-snapshots',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
