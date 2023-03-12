from django.contrib import admin

from apps.images_api.models import Thumbnail, UploadedImage

# Register your models here.

admin.site.register(UploadedImage)
admin.site.register(Thumbnail)
