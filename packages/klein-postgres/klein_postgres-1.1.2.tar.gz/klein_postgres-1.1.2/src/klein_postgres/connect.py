#  Copyright 2022 Medicines Discovery Catapult
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# -*- coding: utf-8 -*-
import argparse
import logging
from typing import Dict

import psycopg2
from psycopg2.extras import LoggingConnection
from klein_config import get_config

parser = argparse.ArgumentParser()
parser.add_argument("--debug", help="enable debug", action="store_true")


def params(config_path: str = 'postgres', **kwargs) -> Dict:
    """
    generate a dict of connection based on those provided by klein_config
    :param config_path: the path to the postgres config in the config
    :param kwargs: expanded keyword arguments to build a connection with
    :return dict
    """
    config = get_config()
    p = {}

    if config.has(f'{config_path}.username'):
        p["user"] = config.get(f'{config_path}.username')

    if config.has(f'{config_path}.password'):
        p["password"] = config.get(f'{config_path}.password')

    if config.has(f'{config_path}.database'):
        p["database"] = config.get(f'{config_path}.database')

    if config.has(f'{config_path}.host'):
        p["host"] = config.get(f'{config_path}.host', "127.0.0.1")

    if config.has(f'{config_path}.port'):
        p["port"] = config.get(f'{config_path}.port', "5432")

    p["readonly"] = bool(config.get(f'{config_path}.readonly', True))
    p["autocommit"] = bool(config.get(f'{config_path}.autocommit', p["readonly"]))

    p.update(kwargs)
    return p


class PostgresConnection:

    def __init__(self):
        self.connections = {}
        args, _ = parser.parse_known_args()
        self.debug = args

    def refresh(self, config_path: str = 'postgres', **kwargs):
        """
        refresh the connection
        :param config_path: the path to the postgres config in the config
        :param **kwargs: parameters to refresh the connection with (optional)
        :return psycopg.connection
        """
        if config_path in self.connections:
            self.connections[config_path].close()
        return self.connect(config_path, **kwargs)

    def connect(self, config_path: str = 'postgres', **kwargs):
        """
        connect to database
        :param config_path: the path to the postgres config in the config
        :param **kwargs: parameters to refresh the connection with (optional)
        :return psycopg.connection
        """

        p = params(config_path, **kwargs)

        if not p:
            return None

        readonly = p.pop('readonly', True)
        autocommit = p.pop('autocommit', readonly)

        if self.debug:
            logging.basicConfig(level=logging.DEBUG)
            logger = logging.getLogger(__name__)
            p["connection_factory"] = LoggingConnection
            conn = psycopg2.connect(**p)
            conn.initialize(logger)
        else:
            conn = psycopg2.connect(**p)

        conn.set_session(readonly=readonly,
                         autocommit=autocommit)

        return conn


