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
import psycopg2.extras

from .connect import PostgresConnection

connection_object = PostgresConnection()
connect = connection_object.connect
connection = connection_object.connect()
refresh = connection_object.refresh()
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor) if connection else None