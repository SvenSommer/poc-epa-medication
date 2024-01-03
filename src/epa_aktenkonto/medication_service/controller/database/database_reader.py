import logging

from controller.database.database_connection import DatabaseConnection


class DatabaseReader(DatabaseConnection):
    def __init__(self):
        super().__init__()

    def get_resource(self, resource_type, identifier):
        if not self.is_connected():
            return None

        with self.conn.cursor() as cursor:
            return self._execute_query_all(cursor, f"SELECT data FROM {resource_type} WHERE identifier = %s", (identifier,))
    
    def find_resource_by_unique_ressource_identifier(self, resource_type, unique_ressource_identifier):
        if not self.is_connected():
            return None
        
        with self.conn.cursor() as cursor:
            return self._execute_fetch_one(cursor, f"SELECT identifier FROM {resource_type} WHERE unique_ressource_identifier = %s", (unique_ressource_identifier,))
        
    def get_resource_by_unique_ressource_identifier(self, resource_type, unique_ressource_identifier):
        if not self.is_connected():
            return None

        with self.conn.cursor() as cursor:
            ressource = self._execute_query_all(cursor, f"SELECT data FROM {resource_type} WHERE unique_ressource_identifier = %s", (unique_ressource_identifier,))

        return ressource
        
    def get_resource_by_rx_identifier(self, resource_type, rx_identifier):
        if not self.is_connected():
            return None

        with self.conn.cursor() as cursor:
            ressource = self._execute_query_all(cursor, f"SELECT data FROM {resource_type} WHERE rx_identifier = %s", (rx_identifier,))

        return ressource
    
    def get_all_resources(self, resource_type):
        if not self.is_connected():
            return None

        with self.conn.cursor() as cursor:
            return self._execute_query_all(cursor, f"SELECT data FROM {resource_type}")

    def get_rx_identifier(self):
        if not self.is_connected():
            return None

        with self.conn.cursor() as cursor:
            return self._execute_query_all(cursor, "SELECT rx_identifier FROM Medication")

    def _execute_query_all(self, cursor, query, params=None):
        try:
            cursor.execute(query, params or ())
            return cursor.fetchall() if cursor.description else None
        except Exception as e:
            logging.error(f"Failed to execute query: {e}")
            return None
        
    def _execute_fetch_one(self, cursor, query, params=None):
        try:
            cursor.execute(query, params or ())
            resource =  cursor.fetchone() 
            return resource[0] if resource else None
        except Exception as e:
            logging.error(f"Failed to execute query: {e}")
            return None
