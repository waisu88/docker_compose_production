from celery import shared_task
import smtplib
import ssl
# from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .models import RemindingMessage
from datetime import timedelta

@shared_task(bind=True)
def send_reminding_email(*args, **kwargs):
    message_id, user_email, message, created_at = args[1]
    
    msg = MIMEMultipart("alternative")
    mime_message = MIMEText(message, "plain")
    msg.attach(mime_message)
    msg["Subject"] = f"Reminding message from {(created_at + timedelta(hours=2)):%H:%M in %A %d.%m.%Yy}"
    # Create the SSLContext object
    context = ssl.create_default_context()
    smtp_server, sender_email, password, email_port = args[2]
    # Use smtplib.SMTP() class
    with smtplib.SMTP(smtp_server, email_port) as server:
        #  Put the connection into TLS mode
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(
            sender_email,
            user_email,
            msg.as_string()
        )
        server.quit()

    RemindingMessage.objects.get(id=message_id).delete()



