import psycopg2


class PostgresConnection:
    def __init__(self, db_url):
        self.db_url = db_url
        self.conn = None

    def __enter__(self):
        self.conn = psycopg2.connect(self.db_url)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
