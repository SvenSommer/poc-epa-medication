#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import psycopg2
import logging

from datetime import datetime

from controller.database import with_connection


class FHIRDataBase(object):

    def __init__(self, res_type):
        self.res_type = res_type

    @with_connection
    def get_all(self, connection):
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT DATA, RES_TYPE FROM resources', ())
            results = cursor.fetchall()
        return results

    @with_connection
    def count(self, connection):
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(ID) from resources WHERE RES_TYPE = %s", (self.res_type,))
            result = cursor.fetchone()
        return result[0] if result else 0

    @with_connection
    def get_instance(self, connection, id):
        with connection.cursor() as cursor:
            instance = self._get_instance(cursor=cursor, id=id)
        return instance

    @with_connection
    def create(self, connection, id, updated, data_json, data_hash):
        with connection.cursor() as cursor:
            self._insert_resource(cursor=cursor, id=id, updated=updated, data_json=data_json, data_hash=data_hash)
        return True
    
    @with_connection
    def search(self, connection, offset, count):
        with connection.cursor() as cursor:
            data = self._search(cursor=cursor, offset=offset, count=count)
        return data
    
    def _search(self, cursor, offset, count):
        cursor.execute(f'SELECT DATA, RES_TYPE FROM resources WHERE RES_TYPE = %s LIMIT %s OFFSET %s', (self.res_type, count, offset))
        results = cursor.fetchall()
        return results

    def _get_instance(self, cursor, id):
        cursor.execute(f"SELECT DATA FROM resources WHERE RES_TYPE = %s AND ID = %s", (self.res_type, id))
        instance = cursor.fetchone()
        return instance[0] if instance else None

    def _insert_resource(self, cursor, id, updated, data_json, data_hash):
        cursor.execute('INSERT INTO resources (ID, RES_TYPE, RES_UPDATED, HASH_SHA256, DATA) VALUES (%s, %s, %s, %s, %s)', (id, self.res_type, updated, data_hash, data_json))
