# 🚀 Proyecto 09 – Honeypot Inteligente con Python  
**Author:** Matías Andrés Lagos Barra  
**GitHub:** [Matiaslb14](https://github.com/Matiaslb14)

---

## 📌 Objetivo / Objective
**ES:** Implementar un honeypot en Linux que simule servicios vulnerables (SSH, HTTP, FTP), capture intentos de intrusión y los analice en tiempo real con Python.  
**EN:** Implement a honeypot in Linux that simulates vulnerable services (SSH, HTTP, FTP), captures intrusion attempts, and analyzes them in real time with Python.

---

## 📖 Descripción / Description
**ES:**  
Este proyecto crea un honeypot ligero en Python con:
- Servicios simulados (SSH, HTTP, FTP).  
- Captura de intentos de conexión y payloads.  
- Clasificación de eventos mediante **regex avanzada** y **modelo ML ligero** (opcional).  
- Almacenamiento en **SQLite** para análisis posterior.  
- **Dashboard en Flask** con métricas de IPs, países, tipos de ataque y timeline.  

**EN:**  
This project creates a lightweight honeypot in Python with:
- Simulated services (SSH, HTTP, FTP).  
- Capture of connection attempts and payloads.  
- Event classification via **advanced regex** and optional **lightweight ML model**.  
- Storage in **SQLite** for later analysis.  
- **Flask dashboard** with IP metrics, countries, attack types, and timeline.

---

## 🏗️ Arquitectura / Architecture
- Puertos reales: **22 / 80 / 21** → redirigidos con `iptables` a **2222 / 8080 / 2121**.  
- Honeypot escucha en puertos altos y guarda eventos en SQLite.  
- Dashboard expone métricas en **http://127.0.0.1:5000**.

Attacker → [22/80/21] → iptables → [2222/8080/2121] → honeypot.py → events.db → dashboard.py

---

## ⚙️ Instalación / Installation
```bash
git clone https://github.com/Matiaslb14/09-honeypot-inteligente.git
cd 09-honeypot-inteligente

# Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Inicializar DB
python db_init.py

▶️ Uso / Usage

Ejecutar el honeypot

python honeypot.py

Redirigir puertos (local y externo)

sudo iptables -t nat -A PREROUTING -p tcp --dport 22 -j REDIRECT --to-ports 2222
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8080
sudo iptables -t nat -A PREROUTING -p tcp --dport 21 -j REDIRECT --to-ports 2121

sudo iptables -t nat -A OUTPUT -p tcp --dport 22 -j REDIRECT --to-ports 2222
sudo iptables -t nat -A OUTPUT -p tcp --dport 80 -j REDIRECT --to-ports 8080
sudo iptables -t nat -A OUTPUT -p tcp --dport 21 -j REDIRECT --to-ports 2121

Generar tráfico de prueba

# HTTP
curl -A "masscan" http://127.0.0.1/ -v

# FTP
nc 127.0.0.1 21
USER anonymous
PASS test

# SSH
ssh -p 22 127.0.0.1

sqlite3 data/events.db "SELECT ts, ip, service, verdict, score FROM events ORDER BY id DESC LIMIT 10;"

Dashboard

python dashboard.py
# http://127.0.0.1:5000

📊 Dashboard

ES: Visualiza estadísticas en tiempo real (tipos de ataque, timeline, IPs).
EN: Visualize real-time stats (attack types, timeline, IPs).

📸 Ejemplo:

🛡️ Consideraciones de seguridad / Security notes

ES: Ejecutar solo en VM aislada, sin datos sensibles. Cambiar el puerto del SSH real para no bloquear acceso administrativo.

EN: Run only inside an isolated VM with no sensitive data. Change the real SSH port to avoid losing admin access.

💡 Valor en tu perfil / Value for your profile

ES: Este proyecto muestra experiencia en:

Python aplicado a ciberseguridad.

Honeypots y análisis de intrusiones.

Regex y clasificación básica con Machine Learning.

Dashboards de monitoreo con Flask.

EN: This project demonstrates skills in:

Python applied to cybersecurity.

Honeypots and intrusion analysis.

Regex and basic classification with Machine Learning.

Monitoring dashboards with Flask.

📂 Estructura / Structure
├─ honeypot.py       # Honeypot principal (SSH/HTTP/FTP)
├─ dashboard.py      # Dashboard en Flask
├─ db_init.py        # Inicialización SQLite
├─ model_train.py    # Entrenamiento ML (opcional)
├─ data/events.db    # Base de datos
├─ templates/        # HTML del dashboard
└─ static/           # Recursos frontend

🔗 Perfil

GitHub: https://github.com/Matiaslb14

LinkedIn: https://www.linkedin.com/in/matias-lagos-620223241


