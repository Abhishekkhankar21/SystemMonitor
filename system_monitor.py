# Main Python script

import psutil
import smtplib
from email.mime.text import MIMEText
import schedule
import time

# Thresholds
CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 80
DISK_THRESHOLD = 90

# Email config
EMAIL_FROM = "your_email@example.com"
EMAIL_TO = "admin@example.com"
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
EMAIL_USER = "your_email@example.com"
EMAIL_PASS = "your_password"

def check_system_health():
    alerts = []

    if psutil.cpu_percent(interval=1) > CPU_THRESHOLD:
        alerts.append("⚠️ High CPU usage detected.")

    if psutil.virtual_memory().percent > MEMORY_THRESHOLD:
        alerts.append("⚠️ High memory usage detected.")

    if psutil.disk_usage('/').percent > DISK_THRESHOLD:
        alerts.append("⚠️ Low disk space.")

    if alerts:
        send_email_alert("\n".join(alerts))

def send_email_alert(message):
    msg = MIMEText(message)
    msg['Subject'] = '🚨 System Health Alert'
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

schedule.every(10).minutes.do(check_system_health)

print("🔍 System health monitor started...")
while True:
    schedule.run_pending()
    time.sleep(1)