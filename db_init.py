# db_init.py
import sqlite3, os

os.makedirs("data", exist_ok=True)
con = sqlite3.connect("data/events.db")
cur = con.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS events(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,
  ip TEXT NOT NULL,
  port INTEGER NOT NULL,
  service TEXT NOT NULL,
  payload TEXT,
  ua TEXT,
  verdict TEXT,
  score REAL,
  country TEXT
);
""")
cur.execute("CREATE INDEX IF NOT EXISTS idx_events_ts ON events(ts);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_events_ip ON events(ip);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_events_service ON events(service);")
con.commit()
con.close()
print("DB inicializada en data/events.db")
