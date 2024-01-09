#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from psycopg2 import sql
import logging

from datetime import datetime

from controller.database import with_connection


class FHIRDataBase(object):

    def __init__(self, res_type):
        self.res_type = res_type

    @with_connection
    def get_all(self, connection):
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT data, res_type FROM resources', ())
            results = cursor.fetchall()
        return results

    @with_connection
    def count(self, connection):
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(id) from resources WHERE res_type = %s", (self.res_type,))
            result = cursor.fetchone()
        return result[0] if result else 0

    @with_connection
    def get_instance(self, connection, id):
        with connection.cursor() as cursor:
            instance = self._get_instance(cursor=cursor, id=id)
        return instance

    @with_connection
    def create(self, connection, id, updated, data_json, data_hash, searchparams=None):
        with connection.cursor() as cursor:
            self._insert_resource(cursor=cursor, id=id, updated=updated, data_json=data_json, data_hash=data_hash)
            if isinstance(searchparams, list):
                for param in searchparams:
                    self._insert_searchparam(cursor=cursor, id=id, name=param.name, hash_value=param.hash_value, value=param.value)
        return True
    
    @with_connection
    def search(self, connection, offset, count, searchparams=None):
        with connection.cursor() as cursor:
            data = self._search(cursor=cursor, offset=offset, count=count, searchparams=searchparams)
            count = self._search(cursor=cursor, searchparams=searchparams, only_count=True)
        return count, data

    def _get_instance(self, cursor, id):
        cursor.execute(f"SELECT data FROM resources WHERE res_type = %s AND id = %s", (self.res_type, id))
        instance = cursor.fetchone()
        return instance[0] if instance else None

    def _insert_resource(self, cursor, id, updated, data_json, data_hash):
        cursor.execute('INSERT INTO resources (id, res_type, res_updated, hash_sha256, data) VALUES (%s, %s, %s, %s, %s)', (id, self.res_type, updated, data_hash, data_json))

    def _insert_searchparam(self, cursor, id, name, hash_value, value):
        cursor.execute('INSERT INTO resourcesearch (resource_id, name, res_type, hash_value, value) VALUES (%s,  %s, %s, %s, %s)', (id, name, self.res_type, hash_value, value))

    def _search(self, cursor, offset=None, count=None, searchparams=None, only_count=False):
        query_params = []
        if only_count:
            query = sql.SQL('SELECT COUNT(RES.id) FROM resources RES WHERE RES.res_type = %s ')
        else:
            query = sql.SQL('SELECT RES.data, RES.res_type FROM resources RES WHERE RES.res_type = %s ')
        query_params.append(self.res_type)

        if searchparams and isinstance(searchparams, list):
            last_index = len(searchparams) - 1
            index = 0
            for param in searchparams:
                if index == 0:
                    query += sql.SQL('AND RES.id in (SELECT SEARCH.resource_id FROM resourcesearch SEARCH WHERE SEARCH.name = %s AND SEARCH.hash_value = %s ')
                else:
                    query += sql.SQL('AND SEARCH.name = %s AND SEARCH.hash_value = %s ')
                if last_index == index:
                    query += sql.SQL(') ')
                query_params.append(param.name)
                query_params.append(param.hash_value)
                index += 1
        
        if count is not None:
            query += sql.SQL('LIMIT %s ')
            query_params.append(count)
        if offset is not None:
            query += sql.SQL('OFFSET %s ')
            query_params.append(offset)   

        cursor.execute(query, query_params)
        
        if only_count:
            result = cursor.fetchone()
            return result[0] if result else 0
        else:
            results = cursor.fetchall()
            return results
