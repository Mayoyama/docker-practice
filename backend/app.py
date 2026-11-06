from flask import Flask
import psycopg
import sys
import os


app = Flask(__name__)


try:
    PG_USER = os.environ["POSTGRES_USER"]
    PG_PW = os.environ["POSTGRES_PASSWORD"]
    DB_NAME = os.environ["POSTGRES_DB"]
    DB_HOST = os.environ["DB_HOST"]

except KeyError as e:
    sys.exit(f"Missing environmental variable: {e}")


VISIT_TABLE = "visits"
VISIT_COL = "count"


with psycopg.connect(
    host=DB_HOST,
    dbname=DB_NAME,
    user=PG_USER,
    password=PG_PW
) as conn:
    conn.execute(f"CREATE TABLE IF NOT EXISTS {VISIT_TABLE} (id INTEGER "
                 f"PRIMARY KEY, {VISIT_COL} INTEGER NOT NULL)")

    conn.execute(f"INSERT INTO {VISIT_TABLE} (id, {VISIT_COL}) VALUES "
                 "(1, 0) ON CONFLICT (id) DO NOTHING")


@app.route("/health")
def get_health() -> tuple[dict[str, str], int]:
    return {"status": "ok"}, 200


@app.route("/visits")
def get_visit_count() -> tuple[dict[str, int | str], int]:
    with psycopg.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=PG_USER,
        password=PG_PW
    ) as conn:
        val = conn.execute(f"UPDATE {VISIT_TABLE} SET {VISIT_COL} = "
                    f"{VISIT_COL} +1 WHERE id = 1 RETURNING {VISIT_COL}")
        res = val.fetchone()

        if res:
            return ({"visit_count": res[0]}, 200)

    return {"error": "visit counter row not found"}, 500

