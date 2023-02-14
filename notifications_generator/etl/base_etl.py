import backoff
import psycopg2
from core.config import settings
from etl.extract import Extract
from etl.load import Load
from etl.transform import Transform


class Etl:
    @backoff.on_exception(
        backoff.expo,
        (psycopg2.OperationalError,),
        max_time=1000,
        max_tries=10,
    )
    async def __aenter__(self):
        self.pg_conn = psycopg2.connect(
            host=settings.postgres.host,
            port=settings.postgres.port,
            database=settings.postgres.dbname,
            user=settings.postgres.user,
            password=settings.postgres.password,
        )
        self.extract = Extract(self.pg_conn)
        self.transform = Transform()
        self.load = Load(
            base_url=f"http://{settings.fastapi.host}:{settings.fastapi.port}"
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.pg_conn.close()
