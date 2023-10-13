import sqlite3

conn = sqlite3.connect("database/database.db")

cursor = conn.cursor()
sql_script_paths = [
    "database\\scripts\\HighCarb.sql",
    "database\\scripts\\LowCarb.sql",
    "database\\scripts\\ModerateCarb.sql",
    "database\\scripts\\StandardCalories.sql",
]

for sql_script_path in sql_script_paths:
    with open(sql_script_path, "r") as file:
        sql_script = file.read()
    cursor.executescript(sql_script)

conn.close()
