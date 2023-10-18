import asyncpg
import os

class DBHandler:
    def __init__(self, logger):
        self.conn = None
        self.cursor = None
        self.logger  = logger

    async def connect(self):
        try:
            self.logger.info(f"Attempting to connect to {os.getenv('HOST')}")
            self.conn = await asyncpg.connect(
                host=os.getenv('HOST'),
                port=os.getenv('PORT'),
                database='thingsboard',
                user=os.getenv('DB_USER'),
                password=os.getenv('PASSWORD')
            )
            self.logger.info("Database connection successfull")
            return
        except Exception as e:
            self.logger.error(f"Error connecting to the database: {e}")

    async def execute_query(self, query):
        try:
            rows = await self.conn.fetch(query)
            return rows
        except Exception as e:
            self.logger.error(f"Error executing query: {e}")

    def close_connection(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            self.logger.error(f"Error closing connection: {e}")

    def get_connection(self):
        return self.conn