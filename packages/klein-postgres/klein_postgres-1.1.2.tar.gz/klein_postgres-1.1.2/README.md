# Klein Postgres

Simple module to enable postgres database connections with details specified in yaml based config file.

## Example

config.yaml

``` yaml
postgres:
    username: postgres_username
    password: postgres_password
    database: database_name
    host: 127.0.0.1
    port: 5432
    readonly: True  # Default to True, set to False if write operation is required
    autocommit: True  # Default to be the same as readonly. If set to false, you are expected to commit after the queries manually.
```

python

``` python
from klein_postgres.connect import connect

connection = connect()  # or
connection = connect('postgres')  # same as in the config. You may specify multiple postgres db in the config
```
In the above example the `postgres` parameter matches the key in the config that the database details should be read from.
If you wanted multiple db connections then you would specify multiple db connection sections in the config:

**N.B. if you do not have working connection details under the `postgres` config key you will encounter a runtime failure.**

```yaml
firstdb:
    username: firstdb_username
    password: firstdb_password
    database: firstdb_name
seconddb:
    username: seconddb_username
    password: seconddb_password
    database: seconddb_name
```

## Development


Utilises python 3.7

### Ubuntu

```
sudo apt install python3.7
```

## Virtualenv

```
virtualenv -p python3.7 venv
source venv/bin/activate
echo -e "[global]\nindex = https://nexus.mdcatapult.io/repository/pypi-all/pypi\nindex-url = https://nexus.mdcatapult.io/repository/pypi-all/simple" > venv/pip.conf
pip install -r requirements.txt
```

### Testing
```bash
docker-compose up
python -m pytest
```
For test coverage you can run:
```bash
docker-compose up
python -m pytest --cov-report term --cov src/ tests/
```

### Anything else?
Why Klein? It's probably one of [these](https://en.wikipedia.org/wiki/Klein_bottle). Possibly a statement on the tangled web of support libraries.

## License
This project is licensed under the terms of the Apache 2 license, which can be found in the repository as `LICENSE.txt`