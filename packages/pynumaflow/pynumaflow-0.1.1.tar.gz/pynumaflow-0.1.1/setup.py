# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynumaflow',
 'pynumaflow.function',
 'pynumaflow.sink',
 'pynumaflow.tests',
 'pynumaflow.tests.function',
 'pynumaflow.tests.sink']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'msgpack>=1.0.3,<2.0.0']

setup_kwargs = {
    'name': 'pynumaflow',
    'version': '0.1.1',
    'description': 'Provides the interfaces of writing Python User Defined Functions and Sinks for NumaFlow.',
    'long_description': '# Python SDK for Numaflow\n\nThis SDK provides the interface for writing [UDFs](https://numaproj.github.io/numaflow/user-defined-functions/) \nand [UDSinks](https://numaproj.github.io/numaflow/sinks/user-defined-sinks/) in Python.\n\n## Implement a User Defined Function (UDF)\n\n```python\nfrom pynumaflow.function import Message, Messages, HTTPHandler\nimport random\n\n\ndef my_handler(key: bytes, value: bytes, _) -> Messages:\n    messages = Messages()\n    if random.randint(0, 10) % 2 == 0:\n        messages.append(Message.to_all(value))\n    else:\n        messages.append(Message.to_drop())\n    return messages\n\n\nif __name__ == "__main__":\n    handler = HTTPHandler(my_handler)\n    handler.start()\n```\n\n### Sample Image\n\nA sample UDF [Dockerfile](examples/function/udfproj/Dockerfile) is provided \nunder [examples](examples/function/udfproj).\n\n\n## Implement a User Defined Sink (UDSink)\n\n```python\nfrom typing import List\nfrom pynumaflow.sink import Message, Responses, Response, HTTPSinkHandler\n\n\ndef udsink_handler(messages: List[Message], __) -> Responses:\n    responses = Responses()\n    for msg in messages:\n        responses.append(Response.as_success(msg.id))\n    return responses\n\n\nif __name__ == "__main__":\n    handler = HTTPSinkHandler(udsink_handler)\n    handler.start()\n```\n\n### Sample Image\n\nA sample UDSink [Dockerfile](examples/sink/simplesink/Dockerfile) is provided \nunder [examples](examples/sink/simplesink).\n',
    'author': 'NumaFlow Developers',
    'author_email': None,
    'maintainer': 'Avik Basu',
    'maintainer_email': 'avikbasu93@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
