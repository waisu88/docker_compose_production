from celery import shared_task
import smtplib
import ssl
import os
# from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .models import RemindingMessage
from datetime import timedelta
from django.utils import timezone

@shared_task(bind=True)
def send_reminding_email(*args, **kwargs):
    message_id = args[1]

    reminding_message = RemindingMessage.objects.get(id=message_id)
    user_email = reminding_message.user.email
    message = reminding_message.message
    created_at = reminding_message.created_at
    
    local_created_at = created_at.astimezone(timezone.get_current_timezone())

    smtp_server = os.environ.get("EMAIL_HOST")
    sender_email = os.environ.get("EMAIL_HOST_USER")
    password = os.environ.get("EMAIL_HOST_PASSWORD")
    email_port = os.environ.get("EMAIL_PORT")

    msg = MIMEMultipart("alternative")
    mime_message = MIMEText(message, "plain")
    msg.attach(mime_message)
    msg["Subject"] = f"Przypominajka z {local_created_at:%H:%M dnia %A %d.%m.%Yy}"
    # Create the SSLContext object
    context = ssl.create_default_context()
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