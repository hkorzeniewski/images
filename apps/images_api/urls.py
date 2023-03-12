from django.urls import path

from apps.images_api.views import UploadImageViewSet, ListImageViewSet

urlpatterns = [
    path("upload/", UploadImageViewSet.as_view({"post": "create"}), name="upload-image"),
    path('images/<int:pk>', ListImageViewSet.as_view({"get": "list"}), name="list-images")
    ]