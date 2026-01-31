import os
import sqlite3
import pandas as pd

os.makedirs("data/processed", exist_ok=True)

CSV_PATH = "data/raw/events.csv"
DB_PATH = "data/processed/funnel.db"

df = pd.read_csv(CSV_PATH)

# Ensure datetime stored in consistent format
df["event_time"] = pd.to_datetime(df["event_time"]).dt.strftime("%Y-%m-%d %H:%M:%S")

conn = sqlite3.connect(DB_PATH)

# Replace table each run (reproducible)
df.to_sql("events", conn, if_exists="replace", index=False)

# Basic indexes to speed up funnel queries
conn.execute("CREATE INDEX IF NOT EXISTS idx_events_user_time ON events(user_id, event_time);")
conn.execute("CREATE INDEX IF NOT EXISTS idx_events_name ON events(event_name);")
conn.commit()

# Quick sanity checks
n_rows = conn.execute("SELECT COUNT(*) FROM events;").fetchone()[0]
n_users = conn.execute("SELECT COUNT(DISTINCT user_id) FROM events;").fetchone()[0]
print(f"Loaded {n_rows} rows for {n_users} users into {DB_PATH}")

conn.close()
