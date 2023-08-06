# gremlin-dsl

A small example Gremlin DSL for the toy Modern database.

## About

There aren't many complete examples of building a **domain specific language (DSL)** using the Gremlin Python driver.
This is a small example Python package that implements a DSL for the Modern toy database, served using the Gremlin Server.

## Usage Notes

The first necessary step is to install the Gremlin server:

```bash
$ curl -o gremlin-server.zip https://dlcdn.apache.org/tinkerpop/3.6.0/apache-tinkerpop-gremlin-server-3.6.0-bin.zip
$ unzip gremlin-server.zip
$ rm -rf gremlin-server.zip
```

The link for the latest release of the Gremlin Server can be found [here](https://tinkerpop.apache.org/).

Next, start the server with the Modern config:

```bash
$ cd apache-tinkerpop-gremlin-server-3.6.0/
$ bin/gremlin-server.sh conf/gremlin-server-modern.yaml
```

Docs on using the Gremlin Server can be found [here](https://tinkerpop.apache.org/docs/current/reference/#gremlin-server).

The package can then be installed from PyPi:

```bash
$ pip install gremlin-dsl
```

With the server running, you can use to the DSL to write queries against the Modern database:

```python
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.anonymous_traversal import traversal

from gremlin_dsl.core_dsl import get_db_endpoint
from gremlin_dsl.core_dsl import SocialTraversalSource

def main():
    endpoint = get_db_endpoint()
    connection = DriverRemoteConnection(endpoint, "g")

    social = traversal(SocialTraversalSource).with_remote(endpoint)

    print(social.persons("marko").knows("josh"))

    connection.close()

if __name__ == "__main__":
  main()
```
