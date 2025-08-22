# 🚀 Project Intelligent Honeypot with Python  
**Author:** Matías Andrés Lagos Barra  
**GitHub:** [Matiaslb14](https://github.com/Matiaslb14)  

## 📌 Objective  
Implement a honeypot in Linux that simulates vulnerable services (SSH, HTTP, FTP), captures intrusion attempts, and analyzes them in real time with Python.  

## 📖 Description  
This project creates a lightweight honeypot in Python with:  
- Simulated services (SSH, HTTP, FTP).  
- Capture of connection attempts and payloads.  
- Event classification via advanced regex and optional lightweight ML model.  
- Storage in SQLite for later analysis.  
- Flask dashboard with IP metrics, countries, attack types, and timeline.  

## 🏗️ Architecture  
- Real ports: 22 / 80 / 21 → redirected with **iptables** to 2222 / 8080 / 2121.  
- Honeypot listens on higher ports and stores events in SQLite.  
- Dashboard available at `http://127.0.0.1:5000`.  

**Flow:**  
Attacker → [22/80/21] → iptables → [2222/8080/2121] → honeypot.py → events.db → dashboard.py  

## ⚙️ Installation  

```bash
git clone https://github.com/Matiaslb14/09-honeypot-inteligente.git
cd 09-honeypot-inteligente

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize DB
python db_init.py

▶️ Usage
Run the honeypot

python honeypot.py

Redirect ports (local and external)

sudo iptables -t nat -A PREROUTING -p tcp --dport 22 -j REDIRECT --to-ports 2222
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8080
sudo iptables -t nat -A PREROUTING -p tcp --dport 21 -j REDIRECT --to-ports 2121

sudo iptables -t nat -A OUTPUT -p tcp --dport 22 -j REDIRECT --to-ports 2222
sudo iptables -t nat -A OUTPUT -p tcp --dport 80 -j REDIRECT --to-ports 8080
sudo iptables -t nat -A OUTPUT -p tcp --dport 21 -j REDIRECT --to-ports 2121

Generate test traffic

# HTTP
curl -A "masscan" http://127.0.0.1/ -v

# FTP
nc 127.0.0.1 21
USER anonymous
PASS test

# SSH
ssh -p 22 127.0.0.1
Check events

sqlite3 data/events.db "SELECT ts, ip, service, verdict, score FROM events ORDER BY id DESC LIMIT 10;"

Dashboard
python dashboard.py
# http://127.0.0.1:5000

📊 Dashboard
Visualize real-time stats (attack types, timeline, IPs).

📸 Example
(Include screenshots here)

🛡️ Security Notes
Run only inside an isolated VM with no sensitive data.

Change the real SSH port to avoid losing admin access.

💡 Value for Your Profile
This project demonstrates skills in:

Python applied to cybersecurity.

Honeypots and intrusion analysis.

Regex and basic classification with Machine Learning.

Monitoring dashboards with Flask.

📂 Structure
bash
Copiar
Editar
├─ honeypot.py       # Main honeypot (SSH/HTTP/FTP)
├─ dashboard.py      # Flask dashboard
├─ db_init.py        # SQLite initialization
├─ model_train.py    # ML training (optional)
├─ data/events.db    # Database
├─ templates/        # Dashboard HTML
└─ static/           # Frontend resources

🔗 Profiles
GitHub: Matiaslb14
LinkedIn: matias-lagos-620223241
