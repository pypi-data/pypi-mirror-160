# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gremlin_dsl']

package_data = \
{'': ['*']}

install_requires = \
['gremlinpython>=3.6.0,<4.0.0']

setup_kwargs = {
    'name': 'gremlin-dsl',
    'version': '0.3.0',
    'description': 'A small example DSL using gremlinpython',
    'long_description': '# gremlin-dsl\n\nA small example Gremlin DSL for the toy Modern database.\n\n## About\n\nThere aren\'t many complete examples of building a **domain specific language (DSL)** using the Gremlin Python driver.\nThis is a small example Python package that implements a DSL for the Modern toy database, served using the Gremlin Server.\n\n## Usage Notes\n\nThe first necessary step is to install the Gremlin server:\n\n```bash\n$ curl -o gremlin-server.zip https://dlcdn.apache.org/tinkerpop/3.6.0/apache-tinkerpop-gremlin-server-3.6.0-bin.zip\n$ unzip gremlin-server.zip\n$ rm -rf gremlin-server.zip\n```\n\nThe link for the latest release of the Gremlin Server can be found [here](https://tinkerpop.apache.org/).\n\nNext, start the server with the Modern config:\n\n```bash\n$ cd apache-tinkerpop-gremlin-server-3.6.0/\n$ bin/gremlin-server.sh conf/gremlin-server-modern.yaml\n```\n\nDocs on using the Gremlin Server can be found [here](https://tinkerpop.apache.org/docs/current/reference/#gremlin-server).\n\nThe package can then be installed from PyPi:\n\n```bash\n$ pip install gremlin-dsl\n```\n\nWith the server running, you can use to the DSL to write queries against the Modern database:\n\n```python\nfrom gremlin_python.driver.driver_remote_connection import DriverRemoteConnection\nfrom gremlin_python.process.anonymous_traversal import traversal\n\nfrom gremlin_dsl.core_dsl import get_db_endpoint\nfrom gremlin_dsl.core_dsl import SocialTraversalSource\n\ndef main():\n    endpoint = get_db_endpoint()\n    connection = DriverRemoteConnection(endpoint, "g")\n\n    social = traversal(SocialTraversalSource).with_remote(endpoint)\n\n    print(social.persons("marko").knows("josh"))\n\n    connection.close()\n\nif __name__ == "__main__":\n  main()\n```\n',
    'author': 'Elliot Hershberg',
    'author_email': 'eahershberg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
