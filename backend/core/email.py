import resend
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
    Sends a welcome email to the new backoffice user via Resend HTTP API.
    """
    if not settings.RESEND_API_KEY:
        logger.warning("RESEND_API_KEY missing. Skipping welcome email.")
        return

    resend.api_key = settings.RESEND_API_KEY
    subject = "RetailDSS'e Hoş Geldiniz! 🚀"
    html_content = get_welcome_email_html(first_name)

    # Note: Using default resend sender if no custom domain is configured.
    # Otherwise replace with your verified domain email (e.g. info@yourdomain.com)
    sender = "RetailDSS <onboarding@resend.dev>" 

    try:
        r = resend.Emails.send({
            "from": sender,
            "to": to_email,
            "subject": subject,
            "html": html_content
        })
        logger.info(f"Welcome email sent to {to_email} via Resend. Response: {r}")
    except Exception as e:
        logger.error(f"Failed to send welcome email to {to_email} via Resend: {e}")

def send_welcome_email_customer(to_email: str, name: str):
    """
    Sends a welcome email to the new mobile customer via Resend HTTP API.
    """
    if not settings.RESEND_API_KEY:
        logger.warning("RESEND_API_KEY missing. Skipping welcome email.")
        return

    resend.api_key = settings.RESEND_API_KEY
    subject = "StyleStore Ailesine Hoş Geldiniz! 🎉"
    
    # Use the nice HTML template from customers.py or a better one
    first_letter = (name[0] if name else "C").upper()
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>StyleStore'a Hoş Geldiniz</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            body {{
                margin: 0;
                padding: 0;
                background-color: #f7f9fc;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                color: #1e293b;
                -webkit-font-smoothing: antialiased;
            }}
            .wrapper {{
                width: 100%;
                background-color: #f7f9fc;
                padding: 40px 0;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                border-radius: 24px;
                overflow: hidden;
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
            }}
            .header {{
                background: linear-gradient(135deg, #1e1b4b 0%, #4338ca 100%);
                padding: 60px 40px;
                text-align: center;
                position: relative;
                overflow: hidden;
            }}
            .header::after {{
                content: '';
                position: absolute;
                top: 0;
                right: 0;
                bottom: 0;
                left: 0;
                background: radial-gradient(circle at 80% 20%, rgba(255,255,255,0.1) 0%, transparent 50%);
                pointer-events: none;
            }}
            .avatar {{
                width: 88px;
                height: 88px;
                background: linear-gradient(135deg, #818cf8 0%, #4f46e5 100%);
                border-radius: 50%;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 24px;
                box-shadow: 0 0 0 8px rgba(255, 255, 255, 0.1);
                color: #ffffff;
                font-size: 36px;
                font-weight: 700;
                line-height: 88px;
            }}
            .title {{
                color: #ffffff;
                margin: 0;
                font-size: 32px;
                font-weight: 700;
                letter-spacing: -0.02em;
                line-height: 1.2;
            }}
            .subtitle {{
                color: #c7d2fe;
                margin: 12px 0 0 0;
                font-size: 18px;
                font-weight: 400;
            }}
            .content {{
                padding: 48px 40px;
            }}
            .greeting {{
                font-size: 24px;
                font-weight: 600;
                color: #0f172a;
                margin-top: 0;
                margin-bottom: 16px;
            }}
            .message {{
                font-size: 16px;
                line-height: 1.6;
                color: #475569;
                margin-bottom: 32px;
            }}
            .reward-card {{
                background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
                border: 1px solid #e2e8f0;
                border-radius: 20px;
                padding: 24px;
                display: flex;
                align-items: center;
                margin-bottom: 40px;
                position: relative;
                overflow: hidden;
            }}
            .reward-card::before {{
                content: '';
                position: absolute;
                left: 0;
                top: 0;
                bottom: 0;
                width: 4px;
                background: linear-gradient(to bottom, #4f46e5, #ec4899);
            }}
            .reward-icon {{
                font-size: 40px;
                margin-right: 24px;
                line-height: 1;
            }}
            .reward-content {{
                flex: 1;
            }}
            .reward-label {{
                color: #64748b;
                font-size: 13px;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                font-weight: 600;
                margin-bottom: 4px;
            }}
            .reward-value {{
                color: #0f172a;
                font-size: 24px;
                font-weight: 700;
                margin: 0;
            }}
            .cta-container {{
                text-align: center;
            }}
            .btn {{
                display: inline-block;
                background-color: #0f172a;
                color: #ffffff !important;
                text-decoration: none;
                padding: 16px 40px;
                border-radius: 9999px;
                font-weight: 600;
                font-size: 16px;
                transition: transform 0.2s, box-shadow 0.2s;
                box-shadow: 0 4px 14px 0 rgba(15, 23, 42, 0.2);
            }}
            .footer {{
                background-color: #f8fafc;
                padding: 32px 40px;
                text-align: center;
                border-top: 1px solid #e2e8f0;
            }}
            .social-links {{
                margin-bottom: 24px;
            }}
            .social-links a {{
                color: #64748b;
                text-decoration: none;
                margin: 0 12px;
                font-weight: 500;
                font-size: 14px;
            }}
            .footer p {{
                margin: 0;
                color: #94a3b8;
                font-size: 13px;
                line-height: 1.5;
            }}
        </style>
    </head>
    <body>
        <div class="wrapper">
            <div class="container">
                
                <!-- Header -->
                <div class="header">
                    <div class="avatar">{first_letter}</div>
                    <h1 class="title">Aramıza Hoş Geldin!</h1>
                    <p class="subtitle">StyleStore ailesine katıldığın için mutluyuz.</p>
                </div>

                <!-- Content -->
                <div class="content">
                    <h2 class="greeting">Merhaba {name},</h2>
                    <p class="message">
                        Alışveriş deneyimini yeniden tanımlaman için özel olarak tasarlanmış StyleStore mobil uygulamasına giriş yaptın. Artık favori ürünlerini keşfedebilir, sana özel fırsatlardan yararlanabilirsin.
                    </p>
                    
                    <!-- Reward Card -->
                    <div class="reward-card">
                        <div class="reward-icon">🎁</div>
                        <div class="reward-content">
                            <div class="reward-label">Hoş Geldin Hediyen</div>
                            <h3 class="reward-value">100 Sadakat Puanı</h3>
                        </div>
                    </div>

                    <p class="message" style="margin-bottom: 40px;">
                        Puanların hemen hesabına tanımlandı. İlk alışverişinde <b>kasa aşamasında</b> bu puanları indirim olarak kullanabilirsin!
                    </p>

                    <!-- CTA Button -->
                    <div class="cta-container">
                        <a href="#" class="btn">Uygulamaya Dön</a>
                    </div>
                </div>

                <!-- Footer -->
                <div class="footer">
                    <div class="social-links">
                        <a href="#">Instagram</a>
                        <a href="#">Twitter</a>
                        <a href="#">Yardım Merkezi</a>
                    </div>
                    <p>
                        &copy; 2026 StyleStore.<br>
                        Bu e-posta otomatik olarak gönderilmiştir. Lütfen yanıtlamayınız.
                    </p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    sender = "StyleStore <onboarding@resend.dev>" 

    try:
        logger.info(f"Attempting to send customer welcome email to {to_email} via Resend")
        r = resend.Emails.send({
            "from": sender,
            "to": to_email,
            "subject": subject,
            "html": html_content
        })
        logger.info(f"✅ Customer welcome email sent to {to_email}. Response: {r}")
    except Exception as e:
        logger.error(f"❌ Failed to send customer welcome email to {to_email} via Resend: {e}")

