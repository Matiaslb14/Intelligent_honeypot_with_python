import asyncio, sqlite3, datetime, re, os
from typing import Tuple, Optional

DB_PATH = "data/events.db"

# ---------- Clasificador (Reglas + ML opcional) ----------

def _regex_rules(service: str, payload: str, ua: Optional[str]) -> Tuple[str, float]:
    text = (payload or "") + " " + (ua or "")
    text_low = text.lower()
    score = 0.0
    verdict = "probe"

    http_iocs = [
        r"/wp-admin", r"/xmlrpc\.php", r"/phpmyadmin", r"\.\./\.\./", r"/etc/passwd",
        r"select\s+.*\s+from", r"union\s+select", r"cmd=", r"eval\(", r"base64,?"
    ]
    ftp_iocs = [r"^USER\s+anonymous", r"^USER\s+ftp", r"^\s*PASS\s*", r"\bSITE\s+EXEC\b"]
    ssh_iocs = [r"ssh-2\.0", r"putty", r"libssh", r"paramiko"]

    if service == "http":
        if any(re.search(p, text_low) for p in http_iocs):
            verdict, score = "web-exploit", 0.9
        elif "user-agent:" in text_low and ("masscan" in text_low or "nmap" in text_low or "nessus" in text_low):
            verdict, score = "web-scan", 0.7
        else:
            verdict, score = "web-probe", 0.5

    elif service == "ftp":
        if any(re.search(p, text_low, flags=re.MULTILINE) for p in ftp_iocs):
            verdict, score = "ftp-bruteforce/anon", 0.8
        else:
            verdict, score = "ftp-probe", 0.5

    elif service == "ssh":
        if any(re.search(p, text_low) for p in ssh_iocs):
            verdict, score = "ssh-scan", 0.7
        else:
            verdict, score = "ssh-probe", 0.5

    return verdict, score

# ML opcional: si existe model.pkl se intenta usar
_model = None
def _try_load_model():
    global _model
    try:
        import joblib
        if os.path.exists("model.pkl"):
            _model = joblib.load("model.pkl")
    except Exception:
        _model = None

def _ml_features(service: str, payload: str, ua: Optional[str]):
    # Features muy simples a modo demo
    txt = (payload or "") + " " + (ua or "")
    return [
        len(txt),
        sum(c.isdigit() for c in txt),
        txt.count('/'),
        1 if "admin" in txt.lower() else 0,
        {"http":0, "ftp":1, "ssh":2}.get(service, 3)
    ]

def classify(service: str, payload: str, ua: Optional[str]) -> Tuple[str,float]:
    # Intentar ML si hay modelo; sino, regex
    if _model is None:
        _try_load_model()
    if _model is not None:
        try:
            import numpy as np
            X = np.array([_ml_features(service, payload, ua)])
            y_prob = _model.predict_proba(X)[0]
            labels = _model.classes_.tolist()
            idx = int(y_prob.argmax())
            return labels[idx], float(y_prob[idx])
        except Exception:
            pass
    return _regex_rules(service, payload, ua)

# ---------- DB helpers ----------

def insert_event(ip: str, port: int, service: str, payload: str, ua: Optional[str], country: Optional[str], verdict: str, score: float):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO events(ts,ip,port,service,payload,ua,verdict,score,country) VALUES (?,?,?,?,?,?,?,?,?)",
        (datetime.datetime.utcnow().isoformat(), ip, port, service, payload, ua, verdict, score, country)
    )
    con.commit()
    con.close()

# GeoIP opcional (si instalas geoip2 y el DB de MaxMind en ./GeoLite2-Country.mmdb)
_geo_reader = None
def ip_country(ip: str) -> Optional[str]:
    global _geo_reader
    if _geo_reader is None:
        try:
            import geoip2.database
            if os.path.exists("GeoLite2-Country.mmdb"):
                _geo_reader = geoip2.database.Reader("GeoLite2-Country.mmdb")
        except Exception:
            _geo_reader = False
    if not _geo_reader:
        return None
    try:
        r = _geo_reader.country(ip)
        return r.country.iso_code
    except Exception:
        return None

# ---------- Servidores ----------

async def handle_http(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    ip, port = writer.get_extra_info('peername')[:2]
    service = "http"
    try:
        data = await asyncio.wait_for(reader.readuntil(b"\r\n\r\n"), timeout=3.0)
    except Exception:
        data = await reader.read(1024)

    raw = data.decode(errors="ignore")
    # Parse request line y UA
    req_line = raw.split("\r\n",1)[0]
    headers = raw.split("\r\n\r\n",1)[0]
    ua = None
    for line in headers.split("\r\n")[1:]:
        if line.lower().startswith("user-agent:"):
            ua = line.split(":",1)[1].strip()
            break

    verdict, score = classify(service, payload=req_line + "\n" + headers, ua=ua)
    country = ip_country(ip)
    insert_event(ip, 80, service, req_line, ua, country, verdict, score)

    resp = (
        "HTTP/1.1 200 OK\r\n"
        "Server: Apache/2.4.41 (Ubuntu)\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        "Connection: close\r\n\r\n"
        "<html><body>OK</body></html>"
    )
    writer.write(resp.encode())
    await writer.drain()
    writer.close()
    await writer.wait_closed()

async def handle_ssh(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    ip, port = writer.get_extra_info('peername')[:2]
    service = "ssh"
    try:
        client_banner = await asyncio.wait_for(reader.readline(), timeout=3.0)
    except Exception:
        client_banner = b""
    # Banner “creíble”
    server_banner = b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.9\r\n"
    writer.write(server_banner)
    await writer.drain()

    payload = (client_banner or b"").decode(errors="ignore").strip()
    verdict, score = classify(service, payload=payload, ua=None)
    country = ip_country(ip)
    insert_event(ip, 22, service, payload, None, country, verdict, score)

    # Espera breve para que el cliente lea el banner
    await asyncio.sleep(0.4)
    try:
        writer.write_eof()  # puede fallar en algunos SO; es opcional
    except Exception:
        pass
    writer.close()
    try:
        await writer.wait_closed()
    except Exception:
        pass


async def handle_ftp(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    ip, port = writer.get_extra_info('peername')[:2]
    service = "ftp"
    writer.write(b"220 (vsFTPd 3.0.3)\r\n")
    await writer.drain()
    transcript = []
    for _ in range(4):  # unas pocas interacciones
        try:
            line = await asyncio.wait_for(reader.readline(), timeout=5.0)
        except Exception:
            break
        if not line:
            break
        s = line.decode(errors="ignore").strip()
        transcript.append(s)
        if s.upper().startswith("USER"):
            writer.write(b"331 Please specify the password.\r\n")
        elif s.upper().startswith("PASS"):
            writer.write(b"530 Login incorrect.\r\n")
            await writer.drain()
            break
        else:
            writer.write(b"500 Unknown command.\r\n")
        await writer.drain()
    payload = "\n".join(transcript)
    verdict, score = classify(service, payload=payload, ua=None)
    country = ip_country(ip)
    insert_event(ip, 21, service, payload, None, country, verdict, score)
    writer.close()
    await writer.wait_closed()

async def main():
    os.makedirs("data", exist_ok=True)
    # Escuchamos en puertos altos; iptables redirige los bajos
    srv_http = await asyncio.start_server(handle_http, host="0.0.0.0", port=8080)
    srv_ssh  = await asyncio.start_server(handle_ssh,  host="0.0.0.0", port=2222)
    srv_ftp  = await asyncio.start_server(handle_ftp,  host="0.0.0.0", port=2121)

    addrs = ", ".join(str(s.getsockname()) for s in srv_http.sockets)
    print(f"Honeypot HTTP en: {addrs}")
    print("Honeypot SSH en : 0.0.0.0:2222 (redirigido desde 22)")
    print("Honeypot FTP en : 0.0.0.0:2121 (redirigido desde 21)")

    async with srv_http, srv_ssh, srv_ftp:
        await asyncio.gather(
            srv_http.serve_forever(),
            srv_ssh.serve_forever(),
            srv_ftp.serve_forever()
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
