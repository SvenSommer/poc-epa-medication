#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import psycopg2
import logging

from functools import wraps
from datetime import datetime

import settings


class Singleton(object):

    def __init__(self, cls):
        self._cls = cls

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)


@Singleton
class Database(object):

    def __init__(self):
        self.db_name = settings.DB_NAME
        self.db_user = settings.DB_USER
        self.db_password = settings.DB_PASSWORD
        self.db_host = settings.DB_HOST
        self.db_port = settings.DB_PORT
        self.__conn = None

    @property
    def connection(self):
        return self.__conn
    
    def start(self):
        if not self.connect():
            return False
        self.create_tables()
        return True

    def connect(self):
        try:
            self.__conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port
            )
            return True
        except Exception as e:
            logging.error(f"Database Connection Failed: {e}")
            return False
        
    def is_connected(self):
        if not self.connection:
            logging.error("Database connection is not established")
            return False
        return True

    def close(self):
        if self.connection:
            self.connection.close()

    def create_tables(self):
        if not self.is_connected():
            return None

        with self.connection.cursor() as cursor:
            self._drop_existing_tables(cursor)
            self._create_new_tables(cursor)

            self.connection.commit()
            logging.info("Tables created successfully")

    def _drop_existing_tables(self, cursor):
        drop_commands = ["DROP TABLE IF EXISTS Resources CASCADE"]
        for command in drop_commands:
            cursor.execute(command)

    def _create_new_tables(self, cursor):
        create_commands = [
            """
            CREATE TABLE IF NOT EXISTS Resources (
                ID VARCHAR PRIMARY KEY,
                RES_TYPE VARCHAR,
                HASH_SHA256 VARCHAR,
                RES_UPDATED TIMESTAMP,
                DATA JSONB
            )
            """
        ]
        for command in create_commands:
            cursor.execute(command)

    def _commit_changes(self):
        try:
            self.connection.commit()
            return True
        except Exception as e:
            logging.error(f"Failed to commit changes: {e}")
            raise e
        

def with_connection(method):
    @wraps(method)
    def _with_connection(self, *args, **kwargs):
        database = Database.Instance()
        if not database.is_connected():
            logging.error("Databse is not connected")
            raise Exception("Dabase connection exception")
        try:
            result = method(self, database.connection, *args, **kwargs)
        except:
            database.connection.rollback()
            logging.error("SQL failed")
            raise
        else:
            try:
                database.connection.commit()
            except Exception as e:
                logging.error(f"Failed to commit changes: {e}")
                raise e

        return result
    return _with_connection