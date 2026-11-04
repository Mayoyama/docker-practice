from flask import Flask
import psycopg
import os


app = Flask(__name__)


@app.route("/health")
def get_health() -> tuple[dict[str, str], int]:
    return {"status": "ok"}, 200

pg_user = os.environ.get("POSTGRES_USER")
pg_pw = os.environ.get("POSTGRES_PASSWORD")
db_name = os.environ.get("POSTGRES_DB")
db_host = os.environ.get("DB_HOST")

with psycopg.connext(db_host, db_name, pg_user, pg_pw) as conn:
    query = conn.execute("")
    res = query.fetchone()
