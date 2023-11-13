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
    # get neccessary variables from kwargs
    message_id = kwargs['message_id']
    smtp_server = kwargs['smtp_server']
    sender_email = kwargs['sender_email']
    password = kwargs['password']
    email_port = kwargs['email_port']
    # get instance of the message
    reminding_message = RemindingMessage.objects.get(id=message_id)
    user_email = reminding_message.user.email
    message = reminding_message.message
    created_at = reminding_message.created_at
    # to avoid encoding issues
    msg = MIMEMultipart("alternative")
    mime_message = MIMEText(message, "plain")
    msg.attach(mime_message)
    # read local datetime
    local_created_at = created_at.astimezone(timezone.get_current_timezone())
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
    # clear unnecessary message
    RemindingMessage.objects.get(id=message_id).delete()