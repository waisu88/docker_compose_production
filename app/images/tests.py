import json
from .models import Image
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from authorization.serializers import LoginSerializer
import datetime



# class RegistationTestCase(APITestCase):

#     def test_registration(self):

#         data = {"username": "testcase", "email": "test@localhost.app", 
#                 "password1": "some-strong-password", "password2": "some-strong-password"}
#         response = self.client.post()
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginAPIViewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="davinci", password="very-strong-password")
        self.client.login(username='davinci', password='very-strong-password')
        # set-up for testing detail-image
        Image.objects.create(id=1, image="image.png", uploaded_by=self.user, created_at=datetime.datetime.now())
        Image.objects.create(id=2, image="image.jpg", uploaded_by=self.user, created_at=datetime.datetime.now())

    # def api_authentication(self):
    #     self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_images_list_authenticated(self):
        response = self.client.get(reverse("list-create-image"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_images_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("list-create-image"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_images_detail_authenticated(self):
        response = self.client.get(reverse("image-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_images_detail_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("image-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_image(self):
        object = Image.objects.get(id=1)
        self.assertIsInstance(object, Image)


class ImageAPIViewTestCase(APITestCase):

    images_urls = reverse("list-create-image")

    def setUp(self):
        pass

