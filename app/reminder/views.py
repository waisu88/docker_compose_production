from rest_framework import generics
from .serializers import RemindingMessagesSerializer
from .models import RemindingMessage
from .tasks import send_reminding_email
from rest_framework.response import Response
import os
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.views import APIView
from django.http import response
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import status
from django.contrib.auth.models import User
from .forms import MessageForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View

# Create your views here.
class RemindingMessagesListAPIView(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    queryset = RemindingMessage.objects.all()
    serializer_class = RemindingMessagesSerializer
    template_name = 'reminding_messages.html'
    # def get(self, request):
    #     messages = RemindingMessage.objects.all()
    #     return Response({'messages': messages}, template_name='reminding_messages.html')

class RemindingMessagesListCreateAPIView(generics.ListCreateAPIView, View):
    queryset = RemindingMessage.objects.all()
    serializer_class = RemindingMessagesSerializer
    form = MessageForm()

    def get(self, request):
        # form = MessageForm()
        return render(request, 'reminding_messages.html', {'form': self.form, 'messages': self.get_queryset()})

    def post(self, request):
        
        if request.data:
            # API request, use serializer
            data = request.data.copy()
            data['user'] = request.user.id
            print(data['user'])
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                message_id = serializer.data["id"]
                send_mail_at = serializer.data['send_mail_at']
                send_reminding_email.apply_async(args=[message_id], kwargs=None, eta=send_mail_at)
                return render(request, 'reminding_messages.html', {'form': self.form, 'messages': self.get_queryset()})
                # return Response({'success': True}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # HTML form request
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.cleaned_data['message']
                send_mail_at = form.cleaned_data['send_mail_at']
                user = request.user
                message_obj = RemindingMessage(message=message, send_mail_at=send_mail_at, user=user)
                message_obj.save()
                return HttpResponseRedirect(reverse('reminding-messages-list'))
            return render(request, 'reminding_messages.html', {'form': form, 'user': request.user})
    
class RemindingMessageDetailAPIView(generics.RetrieveAPIView):
    queryset = RemindingMessage.objects.all()
    serializer_class = RemindingMessagesSerializer
    lookup_field = 'pk'
# class RemindingMessagesListCreateAPIView(APIView):
#     queryset = RemindingMessage.objects.all()
#     serializer_class = RemindingMessagesSerializer
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'reminding_messages.html'


#     def get(self, request, format=None):
#         queryset = RemindingMessage.objects.all()
#         serializer = RemindingMessagesSerializer()
#         return Response({'queryset': queryset, 'serializer': serializer})


#     def post(self, request, format=None):
#         serializer = RemindingMessagesSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'serializer': serializer}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

































# class RemindingMessagesListCreateAPIView(generics.ListCreateAPIView):
#     queryset = RemindingMessage.objects.all()
#     serializer_class = RemindingMessagesSerializer
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'reminding_messages.html'
# class RemindingMessagesListCreateAPIView(APIView):
#     queryset = RemindingMessage.objects.all()
#     serializer_class = RemindingMessagesSerializer
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'reminding_messages.html'


#     def get(self, request, format=None):
#         queryset = RemindingMessage.objects.all()
#         serializer = RemindingMessagesSerializer()
#         return Response({'queryset': queryset, 'serializer': serializer})


#     def post(self, request, format=None):
#         serializer = RemindingMessagesSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'serializer': serializer}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def perform_create(self, reminding_messages_serializer):
    #     if reminding_messages_serializer.is_valid():
    #         reminding_messages_serializer.save()
    #         message_id = reminding_messages_serializer.data["id"]
    #         reminding_message = RemindingMessage.objects.get(id=message_id)
    #         user_email = reminding_message.user.email
    #         send_mail_at = reminding_message.send_mail_at
    #         message = reminding_message.message
    #         created_at = reminding_message.created_at

    #         smtp_server = os.environ.get("EMAIL_HOST")
    #         sender_email = os.environ.get("EMAIL_HOST_USER")
    #         password = os.environ.get("EMAIL_HOST_PASSWORD")
    #         email_port = os.environ.get("EMAIL_PORT")
    #         params = [message_id, user_email, message, created_at]
    #         server_variables = [smtp_server, sender_email, password, email_port]
          
    #         
    #     return Response(reminding_messages_serializer.data, template_name=self.template_name)
   