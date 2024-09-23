from contextlib import contextmanager

from decouple import config
from mysql.connector import Error, connect
from shared.error_handler import CustomError


class Database:
    def __init__(
        self,
        host,
        port,
        user,
        password,
        database,
        collation="utf8mb4_general_ci",
    ):
        self.config = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database,
            "collation": collation,
        }

    @contextmanager
    def _get_connection(self):
        try:
            connection = connect(**self.config)
            yield connection
        except Error as e:
            print(f"Connection error: {e}")
            yield None
        finally:
            if connection:
                connection.close()

    def commit(self, query, params=None):
        with self._get_connection() as connection:
            if connection is None:
                return False
            try:
                cursor = connection.cursor()
                cursor.execute(query, params)
                connection.commit()
                return cursor.lastrowid
            except Error as e:
                connection.rollback()
                raise CustomError(f"{e}", 500)

    def select(self, query, params=None, format=True):
        with self._get_connection() as connection:
            if connection is None:
                return False
            try:
                cursor = connection.cursor()
                cursor.execute(query, params)
                records = cursor.fetchall()
                col_names = [desc[0] for desc in cursor.description]
                cursor.close()

                if format:
                    return [dict(zip(col_names, record)) for record in records]
                else:
                    return (col_names, records)
            except Error as e:
                raise CustomError(f"{e}", 500)


db = Database(
    host=config("DB_HOST"),
    port=config("DB_PORT"),
    user=config("DB_USER"),
    password=config("DB_PASSWORD"),
    database=config("DB_NAME"),
)
