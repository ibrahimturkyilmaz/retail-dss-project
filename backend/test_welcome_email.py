"""Quick test to send the new premium email template"""
import sys, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '.')

from dotenv import load_dotenv
load_dotenv()

from core.config import Settings
settings = Settings()

# Import the actual function
from routers.customers import _send_welcome_email

print(f"Sending welcome email to: {settings.MAIL_USERNAME}")
_send_welcome_email(settings.MAIL_USERNAME, "Ibrahim", "Turkyilmaz")
print("Done! Check your inbox.")
