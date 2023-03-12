from django.shortcuts import render
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from apps.images_api.models import UploadedImage
from apps.images_api.serializers import LinkSerializer, UploadImageSerializer
from apps.images_api.services import ThumbnailService
from apps.users.models import User

# Create your views here.


class UploadImageViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = UploadedImage.objects.all()
    serializer_class = UploadImageSerializer

    def create(self, request, *arg, **kwargs):
        upload_image = self.request.data["uploaded_image"]
        if upload_image:
            upload_user = User.objects.get(id=self.request.data["uploading_user"])
            uploaded_image = UploadedImage.objects.create(
                uploaded_image=upload_image, uploading_user=upload_user
            )

            if upload_user.account_tier.tier_name == "BASIC":
                thumbnail_200px = ThumbnailService.make_thumbnail(
                    image_id=uploaded_image.id, size=200
                )
                serializer = LinkSerializer(
                    data={"link_to_200px_thumbnail": thumbnail_200px.thumbnail.path}
                )
            elif upload_user.account_tier.tier_name == "PREMIUM":
                thumbnail_200px = ThumbnailService.make_thumbnail(
                    image_id=uploaded_image.id, size=200
                )
                thumbnail_400px = ThumbnailService.make_thumbnail(
                    image_id=uploaded_image.id, size=400
                )

                serializer = LinkSerializer(
                    data={
                        "link_to_200px_thumbnail": thumbnail_200px.thumbnail.path,
                        "link_to_400px_thumbnail": thumbnail_400px.thumbnail.path,
                        "link_to_original_image": uploaded_image.uploaded_image.path,
                    }
                )
            elif upload_user.account_tier.tier_name == "ENTERPRISE":
                thumbnail_200px = ThumbnailService.make_thumbnail(
                    image_id=uploaded_image.id, size=200
                )
                thumbnail_400px = ThumbnailService.make_thumbnail(
                    image_id=uploaded_image.id, size=400
                )
                ability_to_fetch_expiring_link = True
                serializer = LinkSerializer(
                    data={
                        "link_to_200px_thumbnail": thumbnail_200px.thumbnail.path,
                        "link_to_400px_thumbnail": thumbnail_400px.thumbnail.path,
                        "link_to_original_image": uploaded_image.uploaded_image.path,
                        "ability_to_fetch_expiring_link": ability_to_fetch_expiring_link,
                    }
                )
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response("Upload image...", status=status.HTTP_400_BAD_REQUEST)


class ListImageViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UploadImageSerializer

    def get_queryset(self):
        queryset = UploadedImage.objects.all()

        username = self.request.query_params.get("username")
        if username is not None:
            queryset = queryset.filter(uploading_user__username=username)
        return queryset
