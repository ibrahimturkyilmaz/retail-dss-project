
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from core.config import settings
from core.logger import logger

def get_welcome_email_html(first_name: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Hoş Geldiniz</title>
    </head>
    <body style="margin: 0; padding: 0; background-color: #f3f4f6; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
        <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
            <tr>
                <td style="padding: 40px 0; text-align: center;">
                    <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);">
                        
                        <!-- Header / Banner -->
                        <div style="background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%); padding: 40px 0; text-align: center;">
                            <div style="width: 80px; height: 80px; background-color: rgba(255, 255, 255, 0.2); border-radius: 20px; display: inline-flex; align-items: center; justify-content: center; margin-bottom: 20px; backdrop-filter: blur(10px);">
                                <span style="font-size: 40px;">🚀</span>
                            </div>
                            <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 700; letter-spacing: -0.5px;">Aramıza Hoş Geldiniz!</h1>
                        </div>

                        <!-- Content -->
                        <div style="padding: 40px 30px;">
                            <h2 style="color: #1f2937; margin-top: 0; font-size: 20px; font-weight: 600;">Merhaba {first_name},</h2>
                            <p style="color: #4b5563; font-size: 16px; line-height: 1.6; margin-bottom: 24px;">
                                RetailDSS ailesine katıldığınız için çok mutluyuz. Perakende operasyonlarınızı optimize etmeye başlamanız için her şey hazır.
                            </p>

                            <!-- Feature Grid -->
                            <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-top: 30px; margin-bottom: 30px;">
                                <tr>
                                    <td width="33%" style="padding: 10px; vertical-align: top; text-align: center;">
                                        <div style="background-color: #eff6ff; width: 60px; height: 60px; border-radius: 16px; display: inline-flex; align-items: center; justify-content: center; margin-bottom: 12px;">
                                            <span style="font-size: 28px;">📊</span>
                                        </div>
                                        <h3 style="margin: 0; font-size: 14px; color: #1f2937; font-weight: 600;">Gelişmiş Analizler</h3>
                                    </td>
                                    <td width="33%" style="padding: 10px; vertical-align: top; text-align: center;">
                                        <div style="background-color: #f0fdf4; width: 60px; height: 60px; border-radius: 16px; display: inline-flex; align-items: center; justify-content: center; margin-bottom: 12px;">
                                            <span style="font-size: 28px;">📍</span>
                                        </div>
                                        <h3 style="margin: 0; font-size: 14px; color: #1f2937; font-weight: 600;">Mağaza Simülasyonu</h3>
                                    </td>
                                    <td width="33%" style="padding: 10px; vertical-align: top; text-align: center;">
                                        <div style="background-color: #fff7ed; width: 60px; height: 60px; border-radius: 16px; display: inline-flex; align-items: center; justify-content: center; margin-bottom: 12px;">
                                            <span style="font-size: 28px;">📦</span>
                                        </div>
                                        <h3 style="margin: 0; font-size: 14px; color: #1f2937; font-weight: 600;">Stok Takibi</h3>
                                    </td>
                                </tr>
                            </table>

                            <p style="color: #4b5563; font-size: 16px; line-height: 1.6;">
                                Hesabınız aktifleştirildi. Panelinize giderek hemen analizlere başlayabilirsiniz.
                            </p>

                            <!-- CTA Button -->
                            <div style="text-align: center; margin-top: 30px;">
                                <a href="{settings.FRONTEND_URL}" style="display: inline-block; background-color: #4f46e5; color: #ffffff; text-decoration: none; padding: 14px 32px; border-radius: 12px; font-weight: 600; font-size: 16px; box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.4);">
                                    Platformu Keşfet
                                </a>
                            </div>
                        </div>

                        <!-- Footer -->
                        <div style="background-color: #f9fafb; padding: 20px; text-align: center; border-top: 1px solid #e5e7eb;">
                            <p style="margin: 0; color: #9ca3af; font-size: 12px;">
                                &copy; 2026 RetailDSS. Tüm hakları saklıdır.<br>
                                Bu e-posta otomatik olarak gönderilmiştir.
                            </p>
                        </div>
                    </div>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

def send_welcome_email(to_email: str, first_name: str):
    """
    Sends a welcome email to the new user.
    """
    if not settings.MAIL_USERNAME or not settings.MAIL_PASSWORD:
        logger.warning("Mail credentials missing. Skipping welcome email.")
        return

    subject = "RetailDSS'e Hoş Geldiniz! 🚀"
    html_content = get_welcome_email_html(first_name)

    msg = MIMEMultipart('alternative')
    msg['From'] = settings.MAIL_USERNAME
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # Attach HTML version
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))

    try:
        server = smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT)
        server.starttls()
        server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        logger.info(f"Welcome email sent to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send welcome email to {to_email}: {e}")

def send_welcome_email_customer(to_email: str, name: str):
    """
    Sends a welcome email to the new mobile customer.
    """
    if not settings.MAIL_USERNAME or not settings.MAIL_PASSWORD:
        logger.warning("Mail credentials missing. Skipping welcome email.")
        return

    subject = "StyleStore Ailesine Hoş Geldiniz! 🎉"
    
    # Use the nice HTML template from customers.py or a better one
    first_letter = (name[0] if name else "C").upper()
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Hoş Geldiniz</title>
    </head>
    <body style="margin: 0; padding: 0; background-color: #0f172a; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
        <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
            <tr>
                <td style="padding: 40px 0; text-align: center;">
                    <div style="max-width: 600px; margin: 0 auto; background-color: #1e293b; border-radius: 24px; overflow: hidden; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);">
                        
                        <!-- Header / Banner -->
                        <div style="background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%); padding: 50px 0; text-align: center;">
                            <div style="width: 80px; height: 80px; background-color: rgba(255, 255, 255, 0.2); border-radius: 20px; display: inline-flex; align-items: center; justify-content: center; margin-bottom: 20px; backdrop-filter: blur(10px);">
                                <span style="font-size: 40px; color: #fff; font-weight: bold;">{first_letter}</span>
                            </div>
                            <h1 style="color: #ffffff; margin: 0; font-size: 32px; font-weight: 800; letter-spacing: -0.5px;">Merhaba {name}!</h1>
                            <p style="color: rgba(255,255,255,0.9); margin-top: 10px; font-size: 16px;">StyleStore'a Hoş Geldin</p>
                        </div>

                        <!-- Content -->
                        <div style="padding: 40px 30px;">
                            
                            <!-- Welcome Badge -->
                            <div style="background: linear-gradient(to right, #312e81, #1e1b4b); border-radius: 16px; padding: 20px; border: 1px solid #4338ca; display: flex; align-items: center; margin-bottom: 30px;">
                                <div style="font-size: 32px; margin-right: 20px;">🎁</div>
                                <div>
                                    <h3 style="color: #818cf8; margin: 0; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">Hoş Geldin Hediyesi</h3>
                                    <p style="color: #ffffff; margin: 5px 0 0 0; font-size: 20px; font-weight: bold;">100 Sadakat Puanı</p>
                                </div>
                            </div>

                            <p style="color: #94a3b8; font-size: 16px; line-height: 1.6; margin-bottom: 30px;">
                                Mobil uygulamamız üzerinden yapacağınız alışverişlerde puan kazanabilir, size özel kampanyalardan yararlanabilirsiniz.
                            </p>

                            <!-- CTA Button -->
                            <div style="text-align: center; margin-top: 10px;">
                                <a href="#" style="display: inline-block; background-color: #6366f1; color: #ffffff; text-decoration: none; padding: 16px 48px; border-radius: 12px; font-weight: 700; font-size: 16px; box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);">
                                    Alışverişe Başla
                                </a>
                            </div>
                        </div>

                        <!-- Footer -->
                        <div style="background-color: #0f172a; padding: 24px; text-align: center; border-top: 1px solid #334155;">
                            <p style="margin: 0; color: #64748b; font-size: 12px;">
                                &copy; 2026 RetailDSS StyleStore.<br>
                                Bu e-posta otomatik olarak gönderilmiştir.
                            </p>
                        </div>
                    </div>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

    msg = MIMEMultipart('alternative')
    msg['From'] = f"StyleStore <{settings.MAIL_USERNAME}>"
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))

    try:
        server = smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT)
        server.starttls()
        server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        logger.info(f"Customer welcome email sent to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send customer welcome email to {to_email}: {e}")
