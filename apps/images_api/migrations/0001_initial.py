# Generated by Django 4.1.7 on 2023-03-12 22:27

import apps.images_api.models
import apps.images_api.validator
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Thumbnail",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "thumbnail",
                    models.ImageField(upload_to=apps.images_api.models.thumbnail_path),
                ),
                ("thumbnail_size", models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="UploadedImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("uuid", models.UUIDField(default=uuid.uuid4, unique=True)),
                (
                    "uploaded_image",
                    models.ImageField(
                        upload_to=apps.images_api.models.file_upload_path,
                        validators=[apps.images_api.validator.validate_file_size],
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
