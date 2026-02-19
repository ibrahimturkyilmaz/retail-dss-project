import sys
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Add parent directory to path to import backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Explicitly load backend .env
backend_env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(backend_env_path)

from core.config import settings

def test_email():
    print("--- SMTP Test Script ---")
    print(f"Server: {settings.MAIL_SERVER}")
    print(f"Port: {settings.MAIL_PORT}")
    print(f"Username: {settings.MAIL_USERNAME}")
    # Don't print password obviously
    print(f"Password provided: {'Yes' if settings.MAIL_PASSWORD else 'No'}")
    
    sender = settings.MAIL_USERNAME
    receiver = settings.MAIL_USERNAME # Send to self for testing
    
    msg = MIMEText("This is a test email from RetailDSS Debug script.")
    msg['Subject'] = 'RetailDSS SMTP Test'
    msg['From'] = sender
    msg['To'] = receiver

    try:
        print("Connecting to server...")
        server = smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT)
        server.set_debuglevel(1) # Enable debug output
        
        print("Starting TLS...")
        server.starttls()
        
        print("Logging in...")
        server.login(sender, settings.MAIL_PASSWORD)
        
        print(f"Sending email to {receiver}...")
        server.send_message(msg)
        
        print("Quitting...")
        server.quit()
        print("✅ Email sent successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_email()
