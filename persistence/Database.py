import mysql.connector
from mysql.connector import Error, errorcode
from typing import Optional, Union, List, Dict, Any
import logging


class Database:
    """
    A class to handle MySQL database connections and operations.

    Features:
    - Connection pooling
    - Error handling
    - CRUD operations
    - Transaction support
    - Logging
    - Type hints

    Requirements:
    - mysql-connector-python package
    - Python 3.6+
    """

    def __init__(self, host: str, database: str, user: str, password: str,
                 port: int = 3306, pool_name: str = "mypool", pool_size: int = 5):
        """
        Initialize the MySQL database connection.

        Args:
            host: Database host address
            database: Database name
            user: Database username
            password: Database password
            port: Database port (default: 3306)
            pool_name: Connection pool name (default: "mypool")
            pool_size: Connection pool size (default: 5)
        """
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.pool_name = pool_name
        self.pool_size = pool_size
        self.connection = None

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def connect(self) -> bool:
        """
        Establish a connection to the MySQL database with connection pooling.

        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port,
                pool_name=self.pool_name,
                pool_size=self.pool_size,
                autocommit=False
            )
            self.logger.info(f"Successfully connected to database: {self.database}")
            return True
        except Error as e:
            self.logger.error(f"Error connecting to MySQL database: {e}")
            return False

    def disconnect(self) -> None:
        """Close the database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.logger.info("Database connection closed")

    def execute_query(self, query: str, params: Optional[tuple] = None,
                      multi: bool = False) -> Optional[int]:
        """
        Execute a SQL query (INSERT, UPDATE, DELETE).

        Args:
            query: SQL query string
            params: Parameters for the query (default: None)
            multi: Execute multiple statements (default: False)

        Returns:
            Optional[int]: Number of affected rows or None if error
        """
        cursor = None
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()

            cursor = self.connection.cursor()
            cursor.execute(query, params, multi=multi)
            self.connection.commit()
            affected_rows = cursor.rowcount
            self.logger.debug(f"Query executed successfully. Affected rows: {affected_rows}")
            return affected_rows
        except Error as e:
            self.logger.error(f"Error executing query: {query}. Error: {e}")
            if self.connection:
                self.connection.rollback()
            return None
        finally:
            if cursor:
                cursor.close()

    def execute_read_query(self, query: str, params: Optional[tuple] = None,
                           fetch_all: bool = True) -> Optional[Union[List[Dict[str, Any]], Dict[str, Any]]]:
        """
        Execute a read query (SELECT).

        Args:
            query: SQL query string
            params: Parameters for the query (default: None)
            fetch_all: Fetch all results if True, else fetch one (default: True)

        Returns:
            Optional[Union[List[Dict], Dict]]: Query results as list of dictionaries
            or single dictionary, None if error
        """
        cursor = None
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()

            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)

            if fetch_all:
                result = cursor.fetchall()
            else:
                result = cursor.fetchone()

            self.logger.debug(f"Read query executed successfully. Rows returned: {len(result) if result else 0}")
            return result
        except Error as e:
            self.logger.error(f"Error executing read query: {query}. Error: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def insert_record(self, table: str, data: Dict[str, Any]) -> Optional[int]:
        """
        Insert a single record into a table.

        Args:
            table: Table name
            data: Dictionary of column-value pairs

        Returns:
            Optional[int]: ID of the inserted record or None if error
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        try:
            cursor = None
            if not self.connection or not self.connection.is_connected():
                self.connect()

            cursor = self.connection.cursor()
            cursor.execute(query, tuple(data.values()))
            self.connection.commit()
            last_id = cursor.lastrowid
            self.logger.info(f"Record inserted into {table}. ID: {last_id}")
            return last_id
        except Error as e:
            self.logger.error(f"Error inserting record into {table}. Error: {e}")
            if self.connection:
                self.connection.rollback()
            return None
        finally:
            if cursor:
                cursor.close()

    def update_record(self, table: str, data: Dict[str, Any], condition: str,
                      condition_params: Optional[tuple] = None) -> Optional[int]:
        """
        Update records in a table.

        Args:
            table: Table name
            data: Dictionary of column-value pairs to update
            condition: WHERE condition string
            condition_params: Parameters for the condition (default: None)

        Returns:
            Optional[int]: Number of affected rows or None if error
        """
        set_clause = ', '.join([f"{key}=%s" for key in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        params = tuple(data.values())

        if condition_params:
            params += condition_params

        return self.execute_query(query, params)

    def delete_record(self, table: str, condition: str,
                      condition_params: Optional[tuple] = None) -> Optional[int]:
        """
        Delete records from a table.

        Args:
            table: Table name
            condition: WHERE condition string
            condition_params: Parameters for the condition (default: None)

        Returns:
            Optional[int]: Number of affected rows or None if error
        """
        query = f"DELETE FROM {table} WHERE {condition}"
        return self.execute_query(query, condition_params)

    def table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists in the database.

        Args:
            table_name: Name of the table to check

        Returns:
            bool: True if table exists, False otherwise
        """
        query = """
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_schema = %s AND table_name = %s
        """
        params = (self.database, table_name)

        result = self.execute_read_query(query, params, fetch_all=False)
        return result and result['COUNT(*)'] > 0

    def start_transaction(self) -> bool:
        """
        Start a database transaction.

        Returns:
            bool: True if transaction started successfully, False otherwise
        """
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()

            self.connection.start_transaction()
            self.logger.info("Transaction started")
            return True
        except Error as e:
            self.logger.error(f"Error starting transaction: {e}")
            return False

    def commit_transaction(self) -> bool:
        """
        Commit the current transaction.

        Returns:
            bool: True if committed successfully, False otherwise
        """
        try:
            if self.connection and self.connection.is_connected():
                self.connection.commit()
                self.logger.info("Transaction committed")
                return True
            return False
        except Error as e:
            self.logger.error(f"Error committing transaction: {e}")
            return False

    def rollback_transaction(self) -> bool:
        """
        Roll back the current transaction.

        Returns:
            bool: True if rolled back successfully, False otherwise
        """
        try:
            if self.connection and self.connection.is_connected():
                self.connection.rollback()
                self.logger.info("Transaction rolled back")
                return True
            return False
        except Error as e:
            self.logger.error(f"Error rolling back transaction: {e}")
            return False

    def __enter__(self):
        """Context manager entry point."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point."""
        self.disconnect()
