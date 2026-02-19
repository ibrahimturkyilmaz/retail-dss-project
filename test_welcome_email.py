
import sys
import os

# Add backend to sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

# Load .env manually because pydantic might not find it in backend/ from root
env_path = os.path.join(os.getcwd(), 'backend', '.env')
if os.path.exists(env_path):
    print(f"Loading .env from {env_path}")
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.strip().split("=", 1)
                os.environ[k.strip()] = v.strip()

from core.email import send_welcome_email
from core.config import settings

print(f"Testing Welcome Email...")
print(f"SMTP Server: {settings.MAIL_SERVER}")
print(f"SMTP Port: {settings.MAIL_PORT}")
print(f"SMTP User: {settings.MAIL_USERNAME}")

try:
    send_welcome_email("ibrahimtrkylmz632@gmail.com", "Test User")
    print("✅ send_welcome_email called successfully. Check your inbox.")
except Exception as e:
    print(f"❌ Error: {e}")
