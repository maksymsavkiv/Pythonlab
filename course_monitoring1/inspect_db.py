import sqlite3
from pathlib import Path

with sqlite3.connect(Path(__file__).resolve().parent / "db.sqlite3") as conn:
    for name, sql in conn.execute("SELECT name, sql FROM sqlite_master WHERE type='table' ORDER BY name"):
        print(name)
        print(sql)
        print()
