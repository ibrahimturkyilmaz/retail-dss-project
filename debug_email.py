import smtplib
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load .env manually
env_vars = {}
env_path = os.path.join(os.path.dirname(__file__), 'backend', '.env')
try:
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.strip().split("=", 1)
                env_vars[k.strip()] = v.strip()
    print("✅ .env loaded.")
except FileNotFoundError:
    print("❌ .env not found!")
    sys.exit(1)

smtp_server = env_vars.get("MAIL_SERVER", "smtp.gmail.com")
smtp_port = int(env_vars.get("MAIL_PORT", 587))
sender_email = env_vars.get("MAIL_USERNAME")
password = env_vars.get("MAIL_PASSWORD")

recipient = "ibrahimtrkylmz632@gmail.com"

print(f"📧 Testing Email Sending...")
print(f"   Server: {smtp_server}:{smtp_port}")
print(f"   User: {sender_email}")
# print(f"   Pass: {'*' * len(password) if password else 'NONE'}")

if not sender_email or not password:
    print("❌ Missing credentials in .env")
    sys.exit(1)

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = recipient
msg['Subject'] = "RetailDSS Email Test"

body = "This is a test email from RetailDSS debug script. If you see this, SMTP is working."
msg.attach(MIMEText(body, 'plain'))

try:
    print("🔌 Connecting to SMTP server...")
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.set_debuglevel(1) # Enable verbose output
    print("🔒 Starting TLS...")
    server.starttls()
    print("🔑 Logging in...")
    server.login(sender_email, password)
    print("📨 Sending mail...")
    server.send_message(msg)
    server.quit()
    print("✅ Email sent successfully!")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
