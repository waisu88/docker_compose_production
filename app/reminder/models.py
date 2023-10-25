from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class RemindingMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=500, default="Just reminding sth")
    created_at = models.DateTimeField(auto_now_add=True)
    send_mail_at = models.DateTimeField()

    def __str__(self):
        return self.message