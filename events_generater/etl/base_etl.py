import psycopg2
from core.config import settings
from etl.extract import Extract
from etl.transform import Transform


class Etl:
    def __enter__(self):
        self.pg_conn = psycopg2.connect(
            host=settings.postgres.host,
            port=settings.postgres.port,
            database=settings.postgres.dbname,
            user=settings.postgres.user,
            password=settings.postgres.password,
        )
        self.extract = Extract(self.pg_conn)
        self.transform = Transform()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pg_conn.close()
