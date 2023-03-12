from django.urls import path

from apps.images_api.views import ListImageViewSet, UploadImageViewSet

urlpatterns = [
    path(
        "upload/", UploadImageViewSet.as_view({"post": "create"}), name="upload-image"
    ),
    path("images", ListImageViewSet.as_view({"get": "list"}), name="list-images"),
]
