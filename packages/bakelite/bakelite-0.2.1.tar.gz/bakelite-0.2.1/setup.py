# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bakelite',
 'bakelite.generator',
 'bakelite.proto',
 'bakelite.tests',
 'bakelite.tests.proto']

package_data = \
{'': ['*'],
 'bakelite.generator': ['runtimes/cpptiny/*', 'templates/*'],
 'bakelite.tests': ['generator/*']}

install_requires = \
['bitstring>=3.1.7,<4.0.0',
 'click>=8.0.3,<9.0.0',
 'dataclasses-json>=0.5.2,<0.6.0',
 'jinja2>=3,<4',
 'lark>=0.12.0,<0.13.0']

entry_points = \
{'console_scripts': ['bakelite = bakelite.generator.cli:main']}

setup_kwargs = {
    'name': 'bakelite',
    'version': '0.2.1',
    'description': 'A utility that makes it simple to communicate with your firmware.',
    'long_description': "# Bakelite\n\n[![Tests](https://github.com/brendan0powers/bakelite/actions/workflows/test.yaml/badge.svg)](https://github.com/brendan0powers/bakelite/actions/workflows/test.yaml)\n[![Lint](https://github.com/brendan0powers/bakelite/actions/workflows/lint.yaml/badge.svg)](https://github.com/brendan0powers/bakelite/actions/workflows/lint.yaml)\n[![Documentation Status](https://readthedocs.org/projects/bakelite/badge/?version=latest)](https://bakelite.readthedocs.io/en/latest/?badge=latest)\n\n\n[Documentation](https://bakelite.readthedocs.io/en/latest/) | \n[Protocol Spec](https://bakelite.readthedocs.io/en/latest/protocol/) |\n[Arduino Example](https://github.com/brendan0powers/bakelite/tree/master/examples/arduino)\n\n<hr/>\n\nBakelite is a utility that makes it simple to communicate with your firmware.\nBakelite uses a code generator to automate the tedious process of hand-building your own protocol.\nIt includes features like framing, error detection, and a lightweight C++ implementation suitable for small microcontrollers.\n\n\n\n## Features\n* Compact, easy to understand data serialization format\n* Simple message passing\n* Built in framing and error detection\n* Easy to integrate with Serial, USB, TCP, I2C, etc...\n* Use only the parts you need\n* Code generators for:\n    * C++ (header only, no STL or memory allocation)\n    * Python\n\nA more formal overview of the protocol can be found\n[here](./docs/protocol.md), and examples can be found [here](./examples).\n\n## Status\nThis project is in early development. The C++ implementation is currently WIP.\nThe API and data format are not stable, and will change without notice.\n\n## How Does it Work?\n![Overview](docs/img/overview.svg)\nYou start by creating a protocol definition file that describes the messages and fields you'd like to send. It also includes information about the protocol itself, like what kind of framing to use and the maximum message length.\n\nHere's an example:\n```proto\nstruct TestMessage {\n  message: string[128]\n}\n\nstruct Ack {\n  code: uint8\n}\n\nprotocol {\n  maxLength = 256\n  framing = COBS\n  crc = CRC8\n\n  messageIds {\n    TestMessage = 1\n    Ack = 2\n  }\n}\n```\n\nNow that you've created the definition file, we can generate some code:\n```bash\nbakelite gen -l python -i my_proto.bakelite -o my_proto.py\n```\n\nAnd then use it to send a message over a serial port:\n```python3\nfrom proto import Protocol, TestMessage, Ack\nimport serial\n\n# Open a serial port and send an Ack message\nwith serial.Serial(':COM1', 9600) as port:\n  proto = Protocol(stream=port)\n  proto.send(Ack(code=123))\n```\n\nMessage serialization, framing, and error detection are all taken care of.\nIf you need something more customized, you can use any of the components independently.\nDrop-in your own CRC algorithm, use the framer with your own message format, or just use the serializer on its own.\n\nFor a more complete example, have a look at the [Python/Arduino Example](./examples/arduino).",
    'author': 'Brendan Powers',
    'author_email': 'brendan0powers@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/bakelite',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
