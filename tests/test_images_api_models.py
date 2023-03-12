import os
import tempfile
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import (InMemoryUploadedFile,
                                            SimpleUploadedFile)
from django.db import models
from django.test import TestCase
from PIL import Image

from apps.images_api.constants import MAX_FILESIZE
from apps.images_api.models import Thumbnail, UploadedImage
from tests.test_setup import BaseTestCase


class UploadImageModelTest(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        image = Image.new("RGB", size=(100, 100), color=(155, 0, 0))
        buffer_original = BytesIO()
        image.save(fp=buffer_original, format="PNG")
        pillow_image = ContentFile(buffer_original.getvalue())
        uploaded = UploadedImage.objects.create(uploading_user=self.basic_user)
        uploaded.uploaded_image.save(
            f"test.png",
            InMemoryUploadedFile(
                pillow_image,  # file
                None,  # field_name
                f"test.png",  # file name
                "image/png",  # content_type
                pillow_image.tell,  # size
                None,
            ),
        )
        uploaded.save()

    def test_uploaded_image_label(self):
        uploaded_image = UploadedImage.objects.get(id=1)
        field_label = uploaded_image._meta.get_field("uploaded_image").name
        self.assertEqual(field_label, "uploaded_image")

    def test_uploaded_image_too_big(self):
        uploaded_image = UploadedImage.objects.get(id=1)
        self.assertFalse(uploaded_image.uploaded_image.size > MAX_FILESIZE)

    def test_original_image_path(self):
        uploaded_image = UploadedImage.objects.get(id=1)
        path = uploaded_image.uploaded_image.name
        self.assertIn("original", path)


class ThumbnailModelTest(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.basic_thumbnail_size = 200
        self.premium_thumbnail_size = 400
        image = Image.new("RGB", size=(100, 100), color=(155, 0, 0))
        buffer_original = BytesIO()
        image.save(fp=buffer_original, format="PNG")
        pillow_image = ContentFile(buffer_original.getvalue())
        uploaded = UploadedImage.objects.create(uploading_user=self.basic_user)
        uploaded.uploaded_image.save(
            f"test.png",
            InMemoryUploadedFile(
                pillow_image,  # file
                None,  # field_name
                f"test.png",  # file name
                "image/png",  # content_type
                pillow_image.tell,  # size
                None,
            ),
        )
        uploaded.save()
        basic_thumb = BytesIO()
        upload_image_instance = UploadedImage.objects.get(id=1)
        image = upload_image_instance.uploaded_image
        img: Image.Image = Image.open(image.path)

        img.thumbnail((self.basic_thumbnail_size, self.basic_thumbnail_size))
        img.save(basic_thumb, format="PNG")
        thumbnail = InMemoryUploadedFile(
            basic_thumb, None, f"thumb.png", "image/png", basic_thumb.tell, None
        )

        self.thumbnail_created = Thumbnail.objects.create(
            thumbnail=thumbnail,
            thumbnail_size=200,
            original_image=upload_image_instance,
        )

    def test_thumbnails_image_path(self):
        thumbnail_image = Thumbnail.objects.get(id=1)
        path = thumbnail_image.thumbnail.name
        self.assertIn("thumbnails", path)
