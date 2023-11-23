import threading
import time
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework.test import APIClient
from rest_framework import status
from .models import Image, Thumbnail, ExpiringLink

class YourAppTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        self.image = Image.objects.create(image="image.png", name="test-image", uploaded_by=self.user)

    # def create_image(self, name="TestImage"):
    #     return Image.objects.create(image="image.png", name=name, uploaded_by=self.user)

    # def create_expiring_link(self, image):
    #     return ExpiringLink.objects.create(base_image=self.image, seconds_to_expire=60)

    def test_unauthenticated_user_cannot_create_image(self):
        self.client.force_authenticate(user=None)
        response = self.client.post('/images/', {'name': 'NewImage', 'image': 'image.png'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_image(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/images/', {'name': 'NewImage'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Image.objects.count(), 1)
        # self.assertEqual(Thumbnail.objects.count(), 1)  # Assuming thumbnail creation is triggered by the signal.

    def test_delete_image(self):
        self.client.force_authenticate(user=self.user)
        image = self.create_image()
        response = self.client.delete(f'/images/{image.slug}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Image.objects.count(), 0)
        self.assertEqual(Thumbnail.objects.count(), 0)

    def test_user_cannot_delete_other_user_image(self):
        self.client.force_authenticate(user=self.other_user)
        image = self.create_image()
        response = self.client.delete(f'/images/{image.slug}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_nonexistent_image_deletion_returns_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete('/images/nonexistent-slug/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_user_cannot_access_protected_endpoints(self):
        response = self.client.get('/images/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_method_returns_method_not_allowed(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put('/images/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_invalid_input_when_creating_image_returns_bad_request(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/images/', {'invalid_field': 'Invalid Value'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_required_field_when_creating_image_returns_bad_request(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/images/', {'name': ''})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authenticated_user_can_create_image_with_valid_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/images/', {'name': 'Valid Image'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authenticated_user_cannot_create_image_with_duplicate_name(self):
        self.client.force_authenticate(user=self.user)
        Image.objects.create(name='Existing Image', uploaded_by=self.user)
        response = self.client.post('/images/', {'name': 'Existing Image'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cache_is_invalidated_after_image_deletion(self):
        self.client.force_authenticate(user=self.user)
        image = self.create_image()
        response = self.client.get(f'/images/{image.slug}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Delete the image and check if the cache is invalidated
        response = self.client.delete(f'/images/{image.slug}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f'/images/{image.slug}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_signal_handler_deletes_thumbnail_image_file(self):
        self.client.force_authenticate(user=self.user)
        image = self.create_image()
        thumbnail = Thumbnail.objects.create(base_image=image, created_by=self.user, thumbnail_image='path/to/thumbnail.jpg', thumbnail_size='100x100')

        response = self.client.get(f'/thumbnails/{thumbnail.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Delete the thumbnail and check if the associated image file is deleted
        thumbnail.delete()
        response = self.client.get(f'/thumbnails/{thumbnail.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_expiring_link_deleted_after_specified_duration(self):
        self.client.force_authenticate(user=self.user)
        image = self.create_image()
        expiring_link = self.create_expiring_link(image)

        # Check if the expiring link exists initially
        response = self.client.get(f'/expiring/{expiring_link.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Wait for the specified duration, then check if the expiring link is deleted
        time.sleep(61)  # Simulate passage of time
        response = self.client.get(f'/expiring/{expiring_link.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_signal_handler_deletes_thumbnail_image_file_concurrently(self):
        self.client.force_authenticate(user=self.user)
        image = self.create_image()
        thumbnail = Thumbnail.objects.create(base_image=image, created_by=self.user, thumbnail_image='path/to/thumbnail.jpg', thumbnail_size='100x100')

        def delete_thumbnail():
            thumbnail.delete()

        # Simulate concurrent deletion of the thumbnail using multiple threads
        threads = [threading.Thread(target=delete_thumbnail) for _ in range(5)]
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # Check if the associated image file is deleted
        response = self.client.get(f'/thumbnails/{thumbnail.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_expiring_link_deleted_after_specified_duration_concurrently(self):
        self.client.force_authenticate(user=self.user)
        image = self.create_image()
        expiring_link = self.create_expiring_link(image)

        # Check if the expiring link exists initially
        response = self.client.get(f'/expiring/{expiring_link.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        def wait_and_check():
            time.sleep(62)  # Simulate passage of time
            response = self.client.get(f'/expiring/{expiring_link.id}/')
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Simulate concurrent waiting and checking for the expiring link
        threads = [threading.Thread(target=wait_and_check) for _ in range(5)]
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()