# 🐍 Intelligent Honeypot with Python  
### (Honeypot Inteligente en Python)
---

## 🧠 Overview / Descripción

**EN:**  
A lightweight intelligent honeypot built in Python that simulates vulnerable services (SSH, HTTP, FTP), captures intrusion attempts, classifies events in real time, and provides a visual dashboard powered by Flask. Designed for cybersecurity learning, threat monitoring, and behavior analysis.

**ES:**  
Un honeypot liviano e inteligente desarrollado en Python que simula servicios vulnerables (SSH, HTTP, FTP), captura intentos de intrusión, clasifica eventos en tiempo real y entrega un dashboard visual con Flask. Diseñado para aprendizaje en ciberseguridad, monitoreo de amenazas y análisis de comportamiento.

---

## 📋 Description / Descripción Detallada

**EN:**  
This project implements a multi-service honeypot that listens on redirected ports and logs attacker interactions. It supports:

- Simulated SSH, HTTP and FTP services  
- Real-time event processing (regex + optional ML model)  
- SQLite storage for long-term analysis  
- A Flask-based dashboard showing IPs, countries, attack types and timeline  
- Port redirection via **iptables**, allowing safe execution on non-privileged ports

The goal is to provide a simple, extensible and realistic threat-simulation environment for labs and training.

**ES:**  
Este proyecto implementa un honeypot multiservicio que escucha en puertos redirigidos y registra las interacciones de atacantes. Soporta:

- Servicios SSH, HTTP y FTP simulados  
- Procesamiento de eventos en tiempo real (regex + modelo ML opcional)  
- Almacenamiento en SQLite para análisis posterior  
- Dashboard en Flask con IPs, países, tipos de ataque y línea de tiempo  
- Redirección de puertos mediante **iptables**, permitiendo ejecutarlo sin privilegios

El objetivo es ofrecer un entorno sencillo, extensible y realista para laboratorios y entrenamiento.

---

## 🏗️ Architecture / Arquitectura

**EN:**  
Real ports (22/80/21) are redirected to high ports (2222/8080/2121).  
The honeypot listens on these ports, logs events to SQLite, and exposes a dashboard on port 5000.

**Flow:**  
Attacker → [22/80/21] → iptables → [2222/8080/2121] → honeypot.py → events.db → dashboard.py

**ES:**  
Los puertos reales (22/80/21) se redirigen a puertos altos (2222/8080/2121).  
El honeypot escucha en esos puertos, registra eventos en SQLite y expone un dashboard en el puerto 5000.

**Flujo:**  
Atacante → [22/80/21] → iptables → [2222/8080/2121] → honeypot.py → events.db → dashboard.py

---

## ⚙️ Installation / Instalación

git clone https://github.com/Matiaslb14/09-honeypot-inteligente.git
cd 09-honeypot-inteligente

Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

Install dependencies
pip install -r requirements.txt

Initialize database
python db_init.py

▶️ Usage / Ejecución

EN — Run the honeypot

python honeypot.py

ES — Ejecutar el honeypot

python honeypot.py

🔄 EN — Redirect real ports (external + local)

sudo iptables -t nat -A PREROUTING -p tcp --dport 22 -j REDIRECT --to-ports 2222

sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8080

sudo iptables -t nat -A PREROUTING -p tcp --dport 21 -j REDIRECT --to-ports 2121

sudo iptables -t nat -A OUTPUT -p tcp --dport 22 -j REDIRECT --to-ports 2222

sudo iptables -t nat -A OUTPUT -p tcp --dport 80 -j REDIRECT --to-ports 8080

sudo iptables -t nat -A OUTPUT -p tcp --dport 21 -j REDIRECT --to-ports 2121

🔄 ES — Redirigir puertos reales (externo + local)

sudo iptables -t nat -A PREROUTING -p tcp --dport 22 -j REDIRECT --to-ports 2222

sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8080

sudo iptables -t nat -A PREROUTING -p tcp --dport 21 -j REDIRECT --to-ports 2121

sudo iptables -t nat -A OUTPUT -p tcp --dport 22 -j REDIRECT --to-ports 2222

sudo iptables -t nat -A OUTPUT -p tcp --dport 80 -j REDIRECT --to-ports 8080

sudo iptables -t nat -A OUTPUT -p tcp --dport 21 -j REDIRECT --to-ports 2121

🧪 EN — Generate test traffic

HTTP
curl -A "masscan" http://127.0.0.1/ -v

FTP
nc 127.0.0.1 21
USER anonymous
PASS test

SSH
ssh -p 22 127.0.0.1

🧪 ES — Generar tráfico de prueba

HTTP
curl -A "masscan" http://127.0.0.1/ -v

FTP
nc 127.0.0.1 21
USER anonymous
PASS test

SSH
ssh -p 22 127.0.0.1

📄 Check events / Ver eventos

sqlite3 data/events.db "SELECT ts, ip, service, verdict, score FROM events ORDER BY id DESC LIMIT 10;"

🖥️ Dashboard

python dashboard.py
http://127.0.0.1:5000

## 📸 Screenshots / Capturas

### 🔍 Dashboard Overview / Vista General del Dashboard
<p align="center">
  <img src="./images/dashboard_overview.png" width="800">
</p>

### 🧪 SQLite Events View / Vista de Eventos en SQLite
<p align="center">
  <img src="./images/events_terminal_view.png" width="800">
</p>

### 🚀 Flask Server Running / Servidor Flask en Ejecución
<p align="center">
  <img src="./images/flask_server_running.png" width="800">
</p>

🛡️ Security Notes / Notas de Seguridad

**EN:**

Run only inside an isolated VM.

Avoid running on production systems.

Change real SSH port to avoid locking yourself out.

**ES:**

Ejecutar solo dentro de una VM aislada.

No usar en sistemas de producción.

Cambiar el puerto SSH real para evitar pérdida de acceso.

📂 Project Structure / Estructura

├─ honeypot.py       # Main honeypot (SSH/HTTP/FTP)
├─ dashboard.py      # Flask dashboard
├─ db_init.py        # SQLite initialization
├─ model_train.py    # Optional ML training
├─ data/events.db    # Database
├─ templates/        # Dashboard HTML
└─ static/           # Frontend resources

👨‍💻 Developed by / Desarrollado por

Matías Andrés Lagos Barra — Cloud Security & DevSecOps Engineer
