import json
import psycopg2
import logging
import os
import uuid


from controller.database.database_connection import DatabaseConnection

class DatabaseWriter(DatabaseConnection):
    def __init__(self):
        super().__init__()
        if self.conn:
            self.create_tables()

    def create_tables(self):
        if not self.is_connected():
            return None

        with self.conn.cursor() as cursor:
            self._drop_existing_tables(cursor)
            self._create_new_tables(cursor)

            self.conn.commit()
            logging.info("Tables created successfully")


    def _drop_existing_tables(self, cursor):
        drop_commands = [
                    "DROP TABLE IF EXISTS MedicationRequest CASCADE",
                    "DROP TABLE IF EXISTS Medication CASCADE",
                    "DROP TABLE IF EXISTS Organization CASCADE",
                    "DROP TABLE IF EXISTS Practitioner CASCADE",
                    "DROP TABLE IF EXISTS MedicationDispense CASCADE",
                ]

        for command in drop_commands:
            cursor.execute(command)

    def _create_new_tables(self, cursor):
        create_commands = [
                    """
                    CREATE TABLE IF NOT EXISTS MedicationRequest (
                        identifier VARCHAR PRIMARY KEY,
                        unique_ressource_identifier VARCHAR,
                        rx_identifier VARCHAR,
                        data JSONB
                    )
                    """,
                     """
                    CREATE TABLE IF NOT EXISTS MedicationDispense (
                        identifier VARCHAR PRIMARY KEY,
                        unique_ressource_identifier VARCHAR,
                        rx_identifier VARCHAR,
                        data JSONB
                    )
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS Medication (
                        identifier VARCHAR PRIMARY KEY,
                        unique_ressource_identifier VARCHAR,
                        rx_identifier VARCHAR,
                        data JSONB
                    )
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS Organization (
                        identifier VARCHAR PRIMARY KEY,
                        unique_ressource_identifier VARCHAR,
                        data JSONB
                    )
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS Practitioner (
                        identifier VARCHAR PRIMARY KEY,
                        unique_ressource_identifier VARCHAR,
                        data JSONB
                    )
                    """
                ]

        for command in create_commands:
            cursor.execute(command)
        
   

    def create_or_update_resource(self, resource_type, resource_data, unique_ressource_identifier, rx_identifier=None):
        if not self.is_connected():
            return None

        resource_data_json = json.dumps(resource_data)
        resource_identifier = self._commit_create_or_update_resource(resource_type, unique_ressource_identifier, resource_data_json, rx_identifier)

        if not resource_identifier:
            logging.error("Failed to create or update resource")
            return False

        return self._commit_changes()

    def _commit_create_or_update_resource(self, resource_type, unique_ressource_identifier, resource_data_json, rx_identifier):
        with self.conn.cursor() as cursor:
            resource_identifier = self.find_resource_by_unique_ressource_identifier(cursor, resource_type, unique_ressource_identifier)
            
            if resource_identifier:
                self._update_resource(cursor, resource_type, resource_data_json, resource_identifier)
            else:
                resource_identifier = str(uuid.uuid4())
                self._insert_resource(cursor, resource_type, unique_ressource_identifier, rx_identifier, resource_data_json, resource_identifier)

            return resource_identifier

    def find_resource_by_unique_ressource_identifier(self, cursor, resource_type, unique_ressource_identifier):
        cursor.execute(f"SELECT identifier FROM {resource_type} WHERE unique_ressource_identifier = %s", (unique_ressource_identifier,))
        resource = cursor.fetchone()
        return resource[0] if resource else None

    def _update_resource(self, cursor, resource_type, resource_data_json, resource_identifier):
        cursor.execute(f"UPDATE {resource_type} SET data = %s WHERE identifier = %s", (resource_data_json, resource_identifier))
        logging.info(f"Updated {resource_type} with identifier {resource_identifier}")

    def _insert_resource(self, cursor, resource_type, unique_ressource_identifier, rx_identifier, resource_data_json, resource_identifier):
        if rx_identifier:
            cursor.execute(f"INSERT INTO {resource_type} (identifier, unique_ressource_identifier, rx_identifier, data) VALUES (%s, %s, %s, %s)", 
                           (resource_identifier, unique_ressource_identifier, rx_identifier, resource_data_json))
            logging.info(f"Created {resource_type} with identifier {resource_identifier} and unique_ressource_identifier {unique_ressource_identifier} and rx_identifier {rx_identifier}")
        else:   
            cursor.execute(f"INSERT INTO {resource_type} (identifier, unique_ressource_identifier, data) VALUES (%s, %s, %s)", 
                           (resource_identifier, unique_ressource_identifier, resource_data_json))
            logging.info(f"Created {resource_type} with identifier {resource_identifier} and unique_ressource_identifier {unique_ressource_identifier}")

    def _commit_changes(self):
        try:
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"Failed to commit changes: {e}")
            return False
