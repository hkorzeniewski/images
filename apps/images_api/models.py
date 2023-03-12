from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from PIL import Image

from apps.commons.models import TimeStampAbstractModel, UUIDAbstractModel
from apps.images_api.validator import validate_file_size
from apps.users.models import User

# Create your models here.


def file_upload_path(instance, filename) -> str:
    return f"original/{instance.uuid}/{filename}"


def thumbnail_path(instance, filename) -> str:
    return f"thumbnails/{instance.thumbnail_size}/{filename}"


class UploadedImage(TimeStampAbstractModel, UUIDAbstractModel):
    uploaded_image = models.ImageField(
        upload_to=file_upload_path, validators=[validate_file_size]
    )
    uploading_user = models.ForeignKey(User, on_delete=models.CASCADE)


class Thumbnail(models.Model):
    thumbnail = models.ImageField(upload_to=thumbnail_path)
    thumbnail_size = models.IntegerField(null=True)
    original_image = models.ForeignKey(UploadedImage, on_delete=models.CASCADE)
