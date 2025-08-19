from flask import Flask, jsonify, render_template
import sqlite3, datetime

DB_PATH = "data/events.db"
app = Flask(__name__, template_folder="templates", static_folder="static")

def q(sql, params=()):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(sql, params)
    rows = cur.fetchall()
    con.close()
    return rows

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/stats")
def api_stats():
    since = (datetime.datetime.utcnow() - datetime.timedelta(hours=24)).isoformat()
    rows = q("SELECT verdict, COUNT(*) FROM events WHERE ts>=? GROUP BY verdict ORDER BY COUNT(*) DESC", (since,))
    labels = [r[0] for r in rows]
    counts = [r[1] for r in rows]
    return jsonify({"labels": labels, "counts": counts})

@app.route("/api/timeseries")
def api_timeseries():
    since_dt = datetime.datetime.utcnow() - datetime.timedelta(hours=24)
    since = since_dt.isoformat()
    rows = q("""
    SELECT substr(ts,1,13) AS hour, COUNT(*) 
    FROM events 
    WHERE ts>=?
    GROUP BY substr(ts,1,13)
    ORDER BY hour ASC
    """, (since,))
    labels = []
    counts = []
    # Relleno horas vacías
    by_hour = {r[0]: r[1] for r in rows}
    for i in range(25):
        h = (since_dt + datetime.timedelta(hours=i)).strftime("%Y-%m-%dT%H")
        labels.append(h)
        counts.append(by_hour.get(h, 0))
    return jsonify({"labels": labels, "counts": counts})

@app.route("/api/top_ips")
def api_top_ips():
    since = (datetime.datetime.utcnow() - datetime.timedelta(hours=24)).isoformat()
    rows = q("""
    SELECT ip, COALESCE(country,''), COUNT(*) AS cnt
    FROM events WHERE ts>=?
    GROUP BY ip, country
    ORDER BY cnt DESC
    LIMIT 10
    """, (since,))
    return jsonify([{"ip": r[0], "country": r[1] or None, "cnt": r[2]} for r in rows])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
