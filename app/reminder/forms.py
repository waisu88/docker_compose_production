from django import forms

class MessageForm(forms.Form):
    message = forms.CharField(max_length=255, required=True)
    send_mail_at = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))