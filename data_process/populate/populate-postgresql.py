import os
from dotenv import load_dotenv
from tqdm import tqdm
from utilities import PostgresConnection


def execute_sql_file(cursor, filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        sql = f.read()
        cursor.execute(sql)


if __name__ == "__main__":
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL not found in .env file")
    ddl_path = os.path.join(os.path.dirname(__file__), "../process/sql_outputs/ddl.sql")
    dml_path = os.path.join(os.path.dirname(__file__), "../process/sql_outputs/dml.sql")
    sql_files = [ddl_path, dml_path]
    descriptions = ["Creating schemas", "Inserting data"]

    with PostgresConnection(db_url) as conn:
        with conn.cursor() as cur:
            for sql_file, desc in zip(sql_files, descriptions):
                with open(sql_file, "r", encoding="utf-8") as f:
                    sql_statements = f.read().split(";")
                    sql_statements = [
                        stmt.strip() for stmt in sql_statements if stmt.strip()
                    ]
                    for stmt in tqdm(sql_statements, desc=desc):
                        cur.execute(stmt)
                print(f"{desc} done.")
            # remove every instances in Lap
            # cur.execute(
            #     """
            #     DROP TABLE IF EXISTS screens CASCADE;
            #     DROP TABLE IF EXISTS gpus CASCADE;
            #     DROP TABLE IF EXISTS storages CASCADE;
            #     DROP TABLE IF EXISTS rams CASCADE;
            #     DROP TABLE IF EXISTS cpus CASCADE;
            #     DROP TABLE IF EXISTS conditions CASCADE;
            #     DROP TABLE IF EXISTS keyboards CASCADE;
            #     DROP TABLE IF EXISTS cameras CASCADE;
            #     DROP TABLE IF EXISTS batteries CASCADE;
            #     DROP TABLE IF EXISTS matterials CASCADE;
            #     DROP TABLE IF EXISTS operating_systems CASCADE;
            #     DROP TABLE IF EXISTS ports CASCADE;
            #     DROP TABLE IF EXISTS physicals CASCADE;
            #     DROP TABLE IF EXISTS warranties CASCADE;
            #     DROP TABLE IF EXISTS wireless CASCADE;
            #     DROP TABLE IF EXISTS laptops CASCADE;
            # """
            # )
        conn.commit()
    # print("Database schema and data deleted successfully.")
    print("Database schema and data imported successfully.")
    # print("Database schema successfully.")
