import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from core.config import settings
import logging

logger = logging.getLogger(__name__)

def send_z_report_email(to_email: str, subject: str, body_html: str):
    """
    SMTP sunucusu üzerinden Z-Raporu gönderir.
    Ayarlar .env dosyasından veya Config'den gelir.
    """
    smtp_server = settings.MAIL_SERVER or "smtp.gmail.com"
    smtp_port = int(settings.MAIL_PORT or 587)
    sender_email = settings.MAIL_USERNAME
    password = settings.MAIL_PASSWORD
    
    if not sender_email or not password:
        logger.warning("SMTP ayarları eksik! Mail gönderilemedi (Loglara yazılıyor).")
        logger.info(f"--- MOCK EMAIL TO {to_email} ---\n{subject}\n{body_html}\n---------------------------")
        return False

    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = to_email

        # HTML Body
        part = MIMEText(body_html, "html")
        message.attach(part)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, to_email, message.as_string())
            
        logger.info(f"Z-Report email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False

def send_marketing_email(to_email: str, subject: str, context: dict, coupon_code: str):
    """
    Sends a personalized marketing email with QR code.
    """
    try:
        import qrcode
        import io
        import base64
        
        # Generate QR Code for Coupon
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(coupon_code)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to Base64 for inline HTML
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                    <h2 style="color: #d32f2f;">{subject}</h2>
                    <p style="font-size: 16px;">{context.get('message', 'Sürpriz!')}</p>
                    
                    <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <p><strong>Hava Durumu:</strong> {context.get('weather', 'Bilinmiyor')} ({context.get('temp', 20)}°C)</p>
                        <p><strong>Sana Özel Önerimiz:</strong> {context.get('product', 'Sürpriz Ürün')}</p>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <p style="font-size: 18px; font-weight: bold;">KUPON KODUNUZ:</p>
                        <div style="background-color: #e0f7fa; padding: 10px; font-size: 24px; font-weight: bold; letter-spacing: 2px; color: #006064; display: inline-block;">
                            {coupon_code}
                        </div>
                        <p style="color: #d32f2f; font-size: 12px; margin-top: 5px;">*Sadece önümüzdeki 2 saat geçerlidir!</p>
                        <br/>
                        <img src="data:image/png;base64,{img_str}" alt="Kupon QR" width="150" />
                    </div>
                    
                    <p style="font-size: 14px; color: #777;">
                        Mevcut Puanınız: <strong>{context.get('points', 0)}</strong>. İsterseniz bu ürünü puanlarınızla da alabilirsiniz!
                    </p>
                </div>
            </body>
        </html>
        """
        
        return send_z_report_email(to_email, subject, html_content)
        
    except Exception as e:
        logger.error(f"Marketing email failed: {e}")
        return False
