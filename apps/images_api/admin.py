from django.contrib import admin

from apps.images_api.models import UploadedImage, Thumbnail

# Register your models here.

admin.site.register(UploadedImage)
admin.site.register(Thumbnail)