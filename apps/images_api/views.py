from django.shortcuts import render

from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from apps.images_api.models import UploadedImage
from apps.images_api.serializers import UploadImageSerializer, LinkSerializer
from apps.users.models import User

from apps.images_api.services import ThumbnailService
# Create your views here.

class UploadImageViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = UploadedImage.objects.all()
    serializer_class = UploadImageSerializer
    
    def create(self, request, *arg, **kwargs):
        upload_image = self.request.FILES['uploaded_image']
        upload_user = User.objects.get(id=self.request.data['uploading_user'])
        uploaded_image = UploadedImage.objects.create(uploaded_image=upload_image, uploading_user=upload_user)

        if upload_user.account_tier.tier_name == 'BASIC':
            thumbnail_200px = ThumbnailService.make_thumbnail(image_id=uploaded_image.id, size=200)
            serializer = LinkSerializer(data={
                "link_to_200px_thumbnail": thumbnail_200px.thumbnail.path
            })
        elif upload_user.account_tier.tier_name == 'PREMIUM':
            thumbnail_200px = ThumbnailService.make_thumbnail(image_id=uploaded_image.id, size=200)
            thumbnail_400px = ThumbnailService.make_thumbnail(image_id=uploaded_image.id, size=400)

            serializer = LinkSerializer(data={
                "link_to_200px_thumbnail": thumbnail_200px.thumbnail.path,
                "link_to_400px_thumbnail": thumbnail_400px.thumbnail.path,
                "link_to_original_image": uploaded_image.uploaded_image.path
            })
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ListImageViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UploadImageSerializer

    def get_queryset(self):
        user = User.objects.get(id=self.kwargs['pk'])
        return UploadedImage.objects.filter(uploading_user=user)