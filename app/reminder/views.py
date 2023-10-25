from rest_framework import generics
from .serializers import RemindingMessagesSerializer
from .models import RemindingMessage
from .tasks import send_reminding_email
import smtplib
import ssl
from django.contrib.auth.models import User
import os

# Create your views here.
class RemindingMessagesListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = RemindingMessagesSerializer
    queryset = RemindingMessage.objects.all()

    def perform_create(self, reminding_messages_serializer):
        if reminding_messages_serializer.is_valid():
            reminding_messages_serializer.save()
            message_id = reminding_messages_serializer.data["id"]
            reminding_message = RemindingMessage.objects.get(id=message_id)
            user_email = reminding_message.user.email
            send_mail_at = reminding_message.send_mail_at
            message = reminding_message.message
            created_at = reminding_message.created_at

            smtp_server = os.environ.get("EMAIL_HOST")
            sender_email = os.environ.get("EMAIL_HOST_USER")
            password = os.environ.get("EMAIL_HOST_PASSWORD")
            email_port = os.environ.get("EMAIL_PORT")
            params = [message_id, user_email, message, created_at]
            server_variables = [smtp_server, sender_email, password, email_port]
            print(params)
            print(server_variables)
          
            send_reminding_email.apply_async(args=[params, server_variables], kwargs=None, eta=send_mail_at)
            