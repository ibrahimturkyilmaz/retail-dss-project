import os
# from reportlab.lib.pagesizes import A4
# from reportlab.pdfgen import canvas
# from reportlab.lib.units import mm
# import qrcode
from services.email_service import send_z_report_email # Re-using email logic
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from core.config import settings
import logging

logger = logging.getLogger(__name__)

def generate_receipt_pdf(sale_data: dict, filename: str):
    """
    ReportLab ile PDF Fiş oluşturur.
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import mm
        import qrcode
    except ImportError:
        logger.error("ReportLab or QRCode module not found. Skipping PDF generation.")
        return None

    c = canvas.Canvas(filename, pagesize=(80*mm, 200*mm)) # 80mm Termal Fiş Boyutu
    
    y = 190 * mm
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(40*mm, y, settings.PROJECT_NAME)
    y -= 5*mm
    c.setFont("Helvetica", 8)
    c.drawCentredString(40*mm, y, "Saha Operasyon Fisi")
    y -= 5*mm
    c.drawString(5*mm, y, "-"*40)
    y -= 5*mm
    
    # Bilgiler
    c.drawString(5*mm, y, f"Fiş No: {sale_data.get('receipt_no')}")
    y -= 4*mm
    c.drawString(5*mm, y, f"Tarih: {sale_data.get('created_at')}")
    y -= 4*mm
    c.drawString(5*mm, y, f"Cihaz: {sale_data.get('pos_device_id')}")
    y -= 5*mm
    c.drawString(5*mm, y, "-"*40)
    y -= 5*mm
    
    # Kalemler
    c.setFont("Helvetica-Bold", 8)
    c.drawString(5*mm, y, "Urun")
    c.drawString(50*mm, y, "Fiyat")
    y -= 4*mm
    c.setFont("Helvetica", 8)
    
    for item in sale_data.get('items', []):
        name = item.get('product_sku') # Isim yoksa SKU bas
        price = item.get('unit_price')
        qty = item.get('quantity')
        line = f"{qty}x {name}"
        c.drawString(5*mm, y, line)
        c.drawRightString(75*mm, y, f"{price * qty:.2f} TL")
        y -= 4*mm
        
    y -= 2*mm
    c.drawString(5*mm, y, "-"*40)
    y -= 5*mm
    c.setFont("Helvetica-Bold", 10)
    c.drawString(5*mm, y, "TOPLAM:")
    c.drawRightString(75*mm, y, f"{sale_data.get('total_amount'):.2f} TL")
    
    # QR Code
    qr = qrcode.make(sale_data.get('receipt_no'))
    qr_filename = f"temp_qr_{sale_data.get('receipt_no')}.png"
    qr.save(qr_filename)
    
    y -= 40*mm
    c.drawImage(qr_filename, 20*mm, y, width=40*mm, height=40*mm)
    
    # Cleanup QR
    os.remove(qr_filename)
    
    c.save()
    return filename

def send_receipt_email(to_email: str, pdf_path: str, sale_data: dict):
    """
    PDF fişi mail atar.
    """
    smtp_server = settings.MAIL_SERVER
    smtp_port = settings.MAIL_PORT
    sender_email = settings.MAIL_USERNAME
    password = settings.MAIL_PASSWORD
    
    if not sender_email or not password:
         logger.warning("SMTP Missing. Skipping Receipt Email.")
         return False

    msg = MIMEMultipart()
    msg['Subject'] = f"Satis Fisi: {sale_data.get('receipt_no')}"
    msg['From'] = sender_email
    msg['To'] = to_email

    body = "Alisverisiniz icin tesekkur ederiz. Fisi ektedir."
    msg.attach(MIMEText(body, 'plain'))

    with open(pdf_path, "rb") as f:
        attach = MIMEApplication(f.read(),_subtype="pdf")
        attach.add_header('Content-Disposition','attachment',filename=os.path.basename(pdf_path))
        msg.attach(attach)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
        return True
    except Exception as e:
        logger.error(f"Mail send failed: {e}")
        return False

def process_receipt_delivery(email: str, sale_data: dict, filename: str):
    """
    Background Task Wrapper: Generate PDF -> Send Email -> Delete PDF
    """
    try:
        pdf_path = generate_receipt_pdf(sale_data, filename)
        if email:
            send_receipt_email(email, pdf_path, sale_data)
        
        # Cleanup
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
            
    except Exception as e:
        logger.error(f"Receipt delivery failed: {e}")

