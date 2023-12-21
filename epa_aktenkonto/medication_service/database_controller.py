import json
import psycopg2
import logging
import os
import uuid


class Database:
    def __init__(self):
        self.db_name = os.getenv('DB_NAME', 'fhir')
        self.db_user = os.getenv('DB_USER', 'fhir')
        self.db_password = os.getenv('DB_PASSWORD', 'fhir')
        self.db_host = os.getenv('DB_HOST', 'localhost')
        self.db_port = os.getenv('DB_PORT', '5432')
        self.conn = None
        if self.connect():
            self.create_tables()


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
            print(f"Database Connection Failed: {e}")
            return False
        
    def create_tables(self):
        if self.conn:
            cursor = self.conn.cursor()
            try:
                drop_commands = [
                    "DROP TABLE IF EXISTS MedicationRequest CASCADE",
                    "DROP TABLE IF EXISTS Medication CASCADE",
                    "DROP TABLE IF EXISTS Organization CASCADE",
                    "DROP TABLE IF EXISTS Practitioner CASCADE",
                    "DROP TABLE IF EXISTS MedicationDispense CASCADE",
                    # Add more tables here if necessary
                ]

                create_commands = [
                    """
                    CREATE TABLE IF NOT EXISTS MedicationRequest (
                        identifier VARCHAR PRIMARY KEY,
                        rx_identifier VARCHAR,
                        data JSONB
                    )
                    """,
                     """
                    CREATE TABLE IF NOT EXISTS MedicationDispense (
                        identifier VARCHAR PRIMARY KEY,
                        rx_identifier VARCHAR,
                        data JSONB
                    )
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS Medication (
                        identifier VARCHAR PRIMARY KEY,
                        rx_identifier VARCHAR,
                        data JSONB
                    )
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS Organization (
                        identifier VARCHAR PRIMARY KEY,
                        data JSONB
                    )
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS Practitioner (
                        identifier VARCHAR PRIMARY KEY,
                        data JSONB
                    )
                    """
                ]

                # Drop existing tables
                for command in drop_commands:
                    cursor.execute(command)

                # Create new tables
                for command in create_commands:
                    cursor.execute(command)
                self.conn.commit()
                logging.info("Tables created successfully")
            except Exception as e:
                logging.error(f"Error creating tables: {e}")
            finally:
                cursor.close()
        else:
            logging.error("Database connection is not established")

    def create_resource(self, resource_type, resource_data, rx_identifier=None):
        if self.conn:
            cursor = self.conn.cursor()
            try:
                # Serialize the entire resource_data dictionary to JSON
                resource_data_json = json.dumps(resource_data)

                # Assuming the unique identifier is under the 'id' key in resource_data
                # generate the a new random resource identifier
                resource_identifier = str(uuid.uuid4())

                if rx_identifier:
                    cursor.execute(f"INSERT INTO {resource_type} (identifier, rx_identifier, data) VALUES (%s, %s, %s)", (resource_identifier, rx_identifier, resource_data_json))
                    logging.info(f"Created {resource_type} with identifier {resource_identifier} and rx_identifier {rx_identifier}")
                else:
                    cursor.execute(f"INSERT INTO {resource_type} (identifier, data) VALUES (%s, %s)", (resource_identifier, resource_data_json))
                    logging.info(f"Created {resource_type} with identifier {resource_identifier}")              

                self.conn.commit()
                return True
            except Exception as e:
                logging.error(f"Failed to create or update resource: {e}")
                return False
            finally:
                cursor.close()
        else:
            logging.error("Database connection is not established")
            return False

    def get_resource(self, resource_type, identifier):
        if self.conn:
            cursor = self.conn.cursor()
            try:
                # Retrieve the resource based on its type and identifier
                cursor.execute(f"SELECT data FROM {resource_type} WHERE identifier = %s", (identifier,))
                resource = cursor.fetchone()
                return resource
            except Exception as e:
                logging.error(f"Failed to retrieve resource: {e}")
                return None
            finally:
                cursor.close()
        else:
            logging.error("Database connection is not established")
            return None
        
    def get_all_resources(self, resource_type):
        if self.conn:
            cursor = self.conn.cursor()
            try:
                # Retrieve all resources based on its type
                cursor.execute(f"SELECT data FROM {resource_type}")
                resources = cursor.fetchall()
                return resources
            except Exception as e:
                logging.error(f"Failed to retrieve resources: {e}")
                return None
            finally:
                cursor.close()
        else:
            logging.error("Database connection is not established")
            return None
        
    def get_rx_identifier(self):
        if self.conn:
            cursor = self.conn.cursor()
            try:
                # Retrieve all resources based on its type
                cursor.execute(f"SELECT rx_identifier FROM Medication")
                resources = cursor.fetchall()
                return resources
            except Exception as e:
                logging.error(f"Failed to retrieve resources: {e}")
                return None
            finally:
                cursor.close()
        else:
            logging.error("Database connection is not established")
            return None

    def close(self):
        if self.conn:
            self.conn.close()