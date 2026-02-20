import resend
from core.config import settings
from core.logger import logger
import qrcode
import io
import base64

def send_marketing_email(to_email: str, subject: str, context: dict, coupon_code: str):
    """
    Sends a personalized premium marketing email with a coupon and QR code via Resend.
    """
    if not settings.RESEND_API_KEY:
        logger.warning("RESEND_API_KEY missing. Skipping marketing email.")
        return False

    resend.api_key = settings.RESEND_API_KEY

    try:
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
        <!DOCTYPE html>
        <html lang="tr">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{subject}</title>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
                body {{
                    margin: 0;
                    padding: 0;
                    background-color: #f0f2f5;
                    font-family: 'Outfit', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                    color: #1e293b;
                }}
                .wrapper {{
                    width: 100%;
                    padding: 40px 0;
                    background-color: #f0f2f5;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    border-radius: 32px;
                    overflow: hidden;
                    box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.1);
                }}
                .hero {{
                    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
                    padding: 60px 40px;
                    text-align: center;
                    color: #ffffff;
                }}
                .hero h1 {{
                    font-size: 32px;
                    font-weight: 700;
                    margin: 0;
                    letter-spacing: -0.03em;
                }}
                .content {{
                    padding: 40px;
                }}
                .message {{
                    font-size: 18px;
                    line-height: 1.6;
                    color: #475569;
                    margin-bottom: 30px;
                }}
                .context-box {{
                    background-color: #f8fafc;
                    border-radius: 20px;
                    padding: 24px;
                    margin-bottom: 32px;
                    border: 1px solid #e2e8f0;
                }}
                .context-item {{
                    display: flex;
                    align-items: center;
                    margin-bottom: 12px;
                }}
                .context-item:last-child {{ margin-bottom: 0; }}
                .context-icon {{ font-size: 20px; margin-right: 12px; }}
                .context-text {{ font-size: 15px; color: #64748b; font-weight: 500; }}
                
                .coupon-card {{
                    background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
                    border: 2px dashed #cbd5e1;
                    border-radius: 24px;
                    padding: 40px 20px;
                    text-align: center;
                    margin: 40px 0;
                    position: relative;
                }}
                .coupon-label {{
                    font-size: 13px;
                    font-weight: 700;
                    color: #6366f1;
                    text-transform: uppercase;
                    letter-spacing: 0.1em;
                    margin-bottom: 8px;
                }}
                .coupon-code {{
                    font-size: 36px;
                    font-weight: 800;
                    color: #1e293b;
                    letter-spacing: 4px;
                    margin-bottom: 24px;
                }}
                .qr-code {{
                    width: 160px;
                    height: 160px;
                    margin: 0 auto;
                    padding: 12px;
                    background: #ffffff;
                    border-radius: 16px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
                }}
                .validity {{
                    font-size: 12px;
                    color: #ef4444;
                    font-weight: 600;
                    margin-top: 16px;
                }}
                .footer {{
                    padding: 32px;
                    text-align: center;
                    background-color: #f8fafc;
                    color: #94a3b8;
                    font-size: 13px;
                }}
            </style>
        </head>
        <body>
            <div class="wrapper">
                <div class="container">
                    <div class="hero">
                        <h1>{subject}</h1>
                    </div>
                    <div class="content">
                        <p class="message">
                            Merhaba <strong>{context.get('customer_name', 'Değerli Müşterimiz')}</strong>,<br><br>
                            {context.get('message', 'Sana özel bir sürprizimiz var!')}
                        </p>

                        <div class="context-box">
                            <div class="context-item">
                                <span class="context-icon">📍</span>
                                <span class="context-text">{context.get('store_name')} Mağazamızdasın</span>
                            </div>
                            <div class="context-item">
                                <span class="context-icon">🌦️</span>
                                <span class="context-text">{context.get('weather_condition')}, {context.get('temperature')}°C</span>
                            </div>
                            <div class="context-item">
                                <span class="context-icon">✨</span>
                                <span class="context-text">Sana Özel Önerimiz: <strong>{context.get('product_recommendation')}</strong></span>
                            </div>
                        </div>

                        <div class="coupon-card">
                            <div class="coupon-label">Kupon Kodunuz</div>
                            <div class="coupon-code">{coupon_code}</div>
                            <div class="qr-code">
                                <img src="data:image/png;base64,{img_str}" alt="Kupon QR" width="136" height="136" />
                            </div>
                            <p class="validity">⚠️ Bu kupon sadece 2 saat boyunca geçerlidir!</p>
                        </div>
                    </div>
                    <div class="footer">
                        <p>&copy; 2026 StyleStore RetailDSS. Tüm hakları saklıdır.</p>
                        <p>Mevcut Puanınız: <strong>{context.get('points', 0)}</strong></p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

        sender = "StyleStore <marketing@resend.dev>" 
        
        r = resend.Emails.send({
            "from": sender,
            "to": to_email,
            "subject": subject,
            "html": html_content
        })
        logger.info(f"Marketing email sent to {to_email} via Resend. Response: {r}")
        return True

    except Exception as e:
        logger.error(f"Failed to send marketing email to {to_email} via Resend: {e}")
        return False

def send_z_report_email(to_email: str, subject: str, body_html: str):
    """
    SMTP sunucusu üzerinden Z-Raporu gönderir (Resend ile refaktör edildi).
    """
    if not settings.RESEND_API_KEY:
        logger.warning("RESEND_API_KEY missing. Skipping Z-Report email.")
        return False

    resend.api_key = settings.RESEND_API_KEY
    sender = "StyleStore Reports <reports@resend.dev>" 

    try:
        r = resend.Emails.send({
            "from": sender,
            "to": to_email,
            "subject": subject,
            "html": body_html
        })
        logger.info(f"Z-Report email sent to {to_email} via Resend. Response: {r}")
        return True
    except Exception as e:
        logger.error(f"Error sending report email: {e}")
        return False
