import time
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework.test import APIClient
from rest_framework import status
from .models import Image, Thumbnail, ExpiringLink
from .permissions import CreateExpiringLinkPermission
from .models import ThumbnailSize, AccountTier, GrantedTier
import datetime
from django.urls import reverse

class ImagesApiTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="testuser1", password="very-strong-password")
        self.user2 = User.objects.create_user(username="testuser2", password="very-strong-password")
        self.user3 = User.objects.create_user(username="testuser3", password="very-strong-password")
        self.client = APIClient()
        self.client.login(username='testuser1', password='very-strong-password')
        self.permission = CreateExpiringLinkPermission()
        thumbnail_200px = ThumbnailSize.objects.create(id=1, name="200px", width=200, height=200)
        thumbnail_400px = ThumbnailSize.objects.create(id=2, name="400px", width=400, height=400)
        enterprise_tier = AccountTier.objects.create(id=1, name="Enterprise", link_to_original=True, generate_expiring_links=True)
        enterprise_tier.thumbnail_sizes.add(thumbnail_200px, thumbnail_400px)
        
        # premium_tier = AccountTier.objects.create(id=2, name="Premium", thumbnail_sizes=[thumbnail_200px, thumbnail_400px], link_to_original=True, generate_expiring_links=False)
        # basic_tier = AccountTier.objects.create(id=3, name="Enterprise", thumbnail_sizes=[thumbnail_200px], link_to_original=False, generate_expiring_links=False)
        user1_granted_tiers = GrantedTier.objects.create(id=1, user=self.user1)
        user1_granted_tiers.granted_tiers.add(enterprise_tier)
        # GrantedTier.objects.create(id=2, user=self.user2, granted_tiers=[premium_tier])
        # GrantedTier.objects.create(id=3, user=self.user3, granted_tiers=[basic_tier])
        
        # set-up for testing detail-image
        image_1 = Image.objects.create(id=1, image="image.png", uploaded_by=self.user1, created_at=datetime.datetime.now())
        Image.objects.create(id=2, image="image.jpg", uploaded_by=self.user2, created_at=datetime.datetime.now())
        Thumbnail.objects.create(id=1, created_by=self.user1, base_image=image_1, 
                                 thumbnail_image="th_img.png", thumbnail_size="200px", 
                                 created_at=datetime.datetime.now())
        Thumbnail.objects.create(id=2, created_by=self.user1, base_image=image_1, 
                                 thumbnail_image="th_img.png", thumbnail_size="400px", 
                                 created_at=datetime.datetime.now())
        

    def test_images_list_authenticated(self):
        response = self.client.get(reverse("images"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_images_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("images"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_image_detail_authenticated(self):
    #     response = self.client.get(reverse("image-detail", kwargs={"pk": 1}))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_image_detail_un_authenticated(self):
    #     self.client.force_authenticate(user=None)
    #     response = self.client.get(reverse("image-detail", kwargs={"pk": 1}))
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # def test_expiring_link_authenticated(self):
    #     response = self.client.get(reverse("expiring-links", kwargs={"pk": 1}))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_expiring_link_no_permission(self):
    #     exp_link_obj = ExpiringLinkGrantedPrivileges.objects.get(account_tier__tier_name="Enterprise")
    #     exp_link_obj.expiring_link = False
    #     exp_link_obj.save()
    #     response = self.client.get(reverse("expiring-links", kwargs={"pk": 1}))
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_expiring_link_un_authenticated(self):
    #     self.client.force_authenticate(user=None)
    #     response = self.client.get(reverse("expiring-links", kwargs={"pk": 1}))
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_create_image(self):
    #     object = Image.objects.get(id=1)
    #     self.assertIsInstance(object, Image)

    # def test_create_image_bad_extension_bmp(self):
    #     Image.objects.create(id=4, image="img.bmp", uploaded_by=self.user, created_at=datetime.datetime.now())
    #     object = Image.objects.get(id=4)
    #     self.assertRaises(ValidationError, object.full_clean)
    
    # def test_create_image_bad_extension_pdf(self):
    #     Image.objects.create(id=5, image="img.pdf", uploaded_by=self.user, created_at=datetime.datetime.now())
    #     object = Image.objects.get(id=5)
    #     self.assertRaises(ValidationError, object.full_clean)

    # def test_create_image_bad_extension_tiff(self):
    #     Image.objects.create(id=6, image="img.tiff", uploaded_by=self.user, created_at=datetime.datetime.now())
    #     object = Image.objects.get(id=6)
    #     self.assertRaises(ValidationError, object.full_clean)

    # def test_create_image_bad_extension_svg(self):
    #     Image.objects.create(id=7, image="img.svg", uploaded_by=self.user, created_at=datetime.datetime.now())
    #     object = Image.objects.get(id=7)
    #     self.assertRaises(ValidationError, object.full_clean)

    # def test_create_thumbnail(self):
    #     object = Thumbnail.objects.get(id=1)
    #     self.assertIsInstance(object, Thumbnail)

    # def test_create_expiring_link(self):
    #     ExpiringLink.objects.create(base_image=Image.objects.get(id=1), image="exp_im.png", 
    #                                 seconds=30, created_by=self.user)
    #     object = ExpiringLink.objects.last()
    #     self.assertIsInstance(object, ExpiringLink)

    # def test_create_expiring_link_less_seconds(self):
    #     ExpiringLink.objects.create(base_image=Image.objects.get(id=1), image="exp_im.png", 
    #                                 seconds=20, created_by=self.user)
    #     object = ExpiringLink.objects.last()
    #     self.assertRaises(ValidationError, object.full_clean)

    # def test_create_expiring_link_more_seconds(self):
    #     ExpiringLink.objects.create(base_image=Image.objects.get(id=1), image="exp_im.png", 
    #                                 seconds=30001, created_by=self.user)
    #     object = ExpiringLink.objects.last()
    #     self.assertRaises(ValidationError, object.full_clean)
    


    # def setUp(self):
    #     self.client = APIClient()
    #     self.user = User.objects.create_user(username='testuser', password='testpassword')
    #     self.other_user = User.objects.create_user(username='otheruser', password='otherpassword')
    #     self.image = Image.objects.create(image="image.png", name="test-image", uploaded_by=self.user)

    # # def create_image(self, name="TestImage"):
    # #     return Image.objects.create(image="image.png", name=name, uploaded_by=self.user)

    # # def create_expiring_link(self, image):
    # #     return ExpiringLink.objects.create(base_image=self.image, seconds_to_expire=60)

    # def test_unauthenticated_user_cannot_create_image(self):
    #     self.client.force_authenticate(user=None)
    #     response = self.client.post('/images/', {'name': 'NewImage', 'image': 'image.png'})
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_create_image(self):
    #     self.client.force_authenticate(user=self.user)
    #     response = self.client.post('/images/', {'name': 'NewImage'})
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Image.objects.count(), 1)
    #     # self.assertEqual(Thumbnail.objects.count(), 1)  # Assuming thumbnail creation is triggered by the signal.

    # def test_delete_image(self):
    #     self.client.force_authenticate(user=self.user)
    #     image = self.create_image()
    #     response = self.client.delete(f'/images/{image.slug}/')
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(Image.objects.count(), 0)
    #     self.assertEqual(Thumbnail.objects.count(), 0)

    # def test_user_cannot_delete_other_user_image(self):
    #     self.client.force_authenticate(user=self.other_user)
    #     image = self.create_image()
    #     response = self.client.delete(f'/images/{image.slug}/')
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_nonexistent_image_deletion_returns_not_found(self):
    #     self.client.force_authenticate(user=self.user)
    #     response = self.client.delete('/images/nonexistent-slug/')
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_unauthenticated_user_cannot_access_protected_endpoints(self):
    #     response = self.client.get('/images/')
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_invalid_method_returns_method_not_allowed(self):
    #     self.client.force_authenticate(user=self.user)
    #     response = self.client.put('/images/')
    #     self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # def test_invalid_input_when_creating_image_returns_bad_request(self):
    #     self.client.force_authenticate(user=self.user)
    #     response = self.client.post('/images/', {'invalid_field': 'Invalid Value'})
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_missing_required_field_when_creating_image_returns_bad_request(self):
    #     self.client.force_authenticate(user=self.user)
    #     response = self.client.post('/images/', {'name': ''})
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_authenticated_user_can_create_image_with_valid_data(self):
    #     self.client.force_authenticate(user=self.user)
    #     response = self.client.post('/images/', {'name': 'Valid Image'})
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_authenticated_user_cannot_create_image_with_duplicate_name(self):
    #     self.client.force_authenticate(user=self.user)
    #     Image.objects.create(name='Existing Image', uploaded_by=self.user)
    #     response = self.client.post('/images/', {'name': 'Existing Image'})
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_cache_is_invalidated_after_image_deletion(self):
    #     self.client.force_authenticate(user=self.user)
    #     image = self.create_image()
    #     response = self.client.get(f'/images/{image.slug}/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # Delete the image and check if the cache is invalidated
    #     response = self.client.delete(f'/images/{image.slug}/')
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    #     response = self.client.get(f'/images/{image.slug}/')
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_signal_handler_deletes_thumbnail_image_file(self):
    #     self.client.force_authenticate(user=self.user)
    #     image = self.create_image()
    #     thumbnail = Thumbnail.objects.create(base_image=image, created_by=self.user, thumbnail_image='path/to/thumbnail.jpg', thumbnail_size='100x100')

    #     response = self.client.get(f'/thumbnails/{thumbnail.id}/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # Delete the thumbnail and check if the associated image file is deleted
    #     thumbnail.delete()
    #     response = self.client.get(f'/thumbnails/{thumbnail.id}/')
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_expiring_link_deleted_after_specified_duration(self):
    #     self.client.force_authenticate(user=self.user)
    #     image = self.create_image()
    #     expiring_link = self.create_expiring_link(image)

    #     # Check if the expiring link exists initially
    #     response = self.client.get(f'/expiring/{expiring_link.id}/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # Wait for the specified duration, then check if the expiring link is deleted
    #     time.sleep(61)  # Simulate passage of time
    #     response = self.client.get(f'/expiring/{expiring_link.id}/')
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_signal_handler_deletes_thumbnail_image_file_concurrently(self):
    #     self.client.force_authenticate(user=self.user)
    #     image = self.create_image()
    #     thumbnail = Thumbnail.objects.create(base_image=image, created_by=self.user, thumbnail_image='path/to/thumbnail.jpg', thumbnail_size='100x100')

    #     def delete_thumbnail():
    #         thumbnail.delete()

    #     # Simulate concurrent deletion of the thumbnail using multiple threads
    #     threads = [threading.Thread(target=delete_thumbnail) for _ in range(5)]
    #     for thread in threads:
    #         thread.start()

    #     for thread in threads:
    #         thread.join()

    #     # Check if the associated image file is deleted
    #     response = self.client.get(f'/thumbnails/{thumbnail.id}/')
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_expiring_link_deleted_after_specified_duration_concurrently(self):
    #     self.client.force_authenticate(user=self.user)
    #     image = self.create_image()
    #     expiring_link = self.create_expiring_link(image)

    #     # Check if the expiring link exists initially
    #     response = self.client.get(f'/expiring/{expiring_link.id}/')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

  