import os
import psycopg2
import logging

class DatabaseConnection:
    def __init__(self):
        self.db_name = os.getenv('DB_NAME', 'fhir')
        self.db_user = os.getenv('DB_USER', 'fhir')
        self.db_password = os.getenv('DB_PASSWORD', 'fhir')
        self.db_host = os.getenv('DB_HOST', 'localhost')
        self.db_port = os.getenv('DB_PORT', '5432')
        self.conn = None

        self.conn = None
        self.connect()

    def connect(self):
        try:
            self.conn = psycopg2.connect(
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
        if not self.conn:
            logging.error("Database connection is not established")
            return False
        return True

    def close(self):
        if self.conn:
            self.conn.close()