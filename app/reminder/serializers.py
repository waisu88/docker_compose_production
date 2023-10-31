from rest_framework import serializers
from .models import RemindingMessage
import datetime
import pytz
from django.contrib.auth.models import User



class RemindingMessagesSerializer(serializers.ModelSerializer):
    send_mail_at = serializers.DateTimeField()

    class Meta:
        model = RemindingMessage
        fields = "__all__"
        render_form = True


    def validate(self, data):
        send_mail_data = data['send_mail_at']
        user = data['user']
        if User.objects.get(id=user.id).email == "":
            raise serializers.ValidationError("User has to specify her/his email address first!")
        utc=pytz.UTC
        if datetime.datetime.now().replace(tzinfo=utc) > send_mail_data.replace(tzinfo=utc):
            raise serializers.ValidationError("You can't send mail before creation, unless You are time-machine owner!")
        return data
