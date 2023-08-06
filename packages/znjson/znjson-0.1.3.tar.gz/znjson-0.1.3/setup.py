# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['znjson',
 'znjson..ipynb_checkpoints',
 'znjson.converter',
 'znjson.converter..ipynb_checkpoints',
 'znjson.exceptions']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'znjson',
    'version': '0.1.3',
    'description': 'A Python Package to Encode/Decode some common file formats to json',
    'long_description': '[![Coverage Status](https://coveralls.io/repos/github/zincware/ZnJSON/badge.svg?branch=main)](https://coveralls.io/github/zincware/ZnJSON?branch=main)\n[![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black/)\n[![Tests](https://github.com/zincware/ZnJSON/actions/workflows/pytest.yaml/badge.svg)](https://coveralls.io/github/zincware/ZnJSON?branch=main)\n[![PyPI version](https://badge.fury.io/py/znjson.svg)](https://badge.fury.io/py/znjson)\n\n\n# ZnJSON\n\nPackage to Encode/Decode some common file formats to json\n\nAvailable via ``pip install znjson``\n\nIn comparison to `pickle` this allows having readable json files combined with some\nserialized data.\n\n# Example\n\n````python\nimport numpy as np\nimport json\nimport znjson\n\ndata = json.dumps(\n    obj={"data_np": np.arange(2), "data": [x for x in range(10)]},\n    cls=znjson.ZnEncoder,\n    indent=4\n)\n_ = json.loads(data, cls=znjson.ZnDecoder)\n````\nThe resulting ``*.json`` file is partially readable and looks like this:\n\n````json\n{\n    "data_np": {\n        "_type": "np.ndarray_small",\n        "value": [\n            0,\n            1\n        ]\n    },\n    "data": [\n        0,\n        1,\n        2,\n        3,\n        4\n    ]\n}\n````\n\n# Custom Converter\n\nZnJSON allows you to easily add custom converters.\nLet\'s write a serializer for ``datetime.datetime``. \n\n````python\nfrom znjson import ConverterBase\nfrom datetime import datetime\n\nclass DatetimeConverter(ConverterBase):\n    """Encode/Decode datetime objects\n\n    Attributes\n    ----------\n    level: int\n        Priority of this converter over others.\n        A higher level will be used first, if there\n        are multiple converters available\n    representation: str\n        An unique identifier for this converter.\n    instance:\n        Used to select the correct converter.\n        This should fulfill isinstance(other, self.instance)\n        or __eq__ should be overwritten.\n    """\n    level = 100\n    representation = "datetime"\n    instance = datetime\n\n    def _encode(self, obj: datetime) -> str:\n        """Convert the datetime object to str / isoformat"""\n        return obj.isoformat()\n    def _decode(self, value: str) -> datetime:\n        """Create datetime object from str / isoformat"""\n        return datetime.fromisoformat(value)\n````\n\nThis allows us to use this new serializer:\n````python\nznjson.register(DatetimeConverter) # we need to register the new converter first\njson_string = json.dumps(dt, cls=znjson.ZnEncoder, indent=4)\njson.loads(json_string, cls=znjson.ZnDecoder)\n````\n\nand will result in\n````json\n{\n    "_type": "datetime",\n    "value": "2022-03-11T09:47:35.280331"\n}\n````\n',
    'author': 'zincwarecode',
    'author_email': 'zincwarecode@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
