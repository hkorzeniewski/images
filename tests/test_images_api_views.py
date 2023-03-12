import os
import tempfile
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import (InMemoryUploadedFile,
                                            SimpleUploadedFile)
from django.shortcuts import render
from django.test import TestCase
from django.urls import ResolverMatch, resolve
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.tiers.models import AccountTier
from apps.users.models import User
from tests.test_setup import BaseTestCase

# Create your tests here.


class TestUploadImage(BaseTestCase):
    def setUp(self) -> None:
        self.client = APIClient(enforce_csrf_checks=True)
        self.url = "http://127.0.0.1:8000/upload/"
        self.image = Image.new("RGB", size=(100, 100), color=(155, 0, 0))
        super().setUp()

    def test_upload_with_image_basic_tier(self):
        tmp_image = BytesIO()
        self.image.save(tmp_image, "png")
        image_file = SimpleUploadedFile(
            "test.png", tmp_image.getvalue(), content_type="image/png"
        )

        upload_data = {
            "uploaded_image": image_file,
            "uploading_user": self.basic_user.id,
        }
        self.response = self.client.post(self.url, data=upload_data)
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_upload_without_image(self):
        upload_data = {"uploaded_image": "", "uploading_user": self.basic_user.id}
        self.response = self.client.post(self.url, upload_data)
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)


class TestListImage(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient(enforce_csrf_checks=True)
        self.url = "http://127.0.0.1:8000/images"

    def test_list_images(self):
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_list_images_user(self):
        user_url = self.url + "?username=basicuser"
        self.response = self.client.get(user_url)
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
