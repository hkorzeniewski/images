from rest_framework import mixins, serializers, status, viewsets

from rest_framework import serializers

from apps.images_api.models import UploadedImage, Thumbnail

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class DynamicFieldsSerializer(serializers.Serializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class ThumbnailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Thumbnail
        fields = ("thumbnail", )

class UploadImageSerializer(serializers.ModelSerializer):
 
    thumbnails = ThumbnailSerializer(read_only=True, many=True)

    class Meta:
        model = UploadedImage
        fields = ("uploaded_image", "uploading_user", "thumbnails")

class LinkSerializer(DynamicFieldsSerializer):
    link_to_original_image = serializers.CharField(max_length=256, required=False)
    link_to_200px_thumbnail = serializers.CharField(max_length=256, required=False)
    link_to_400px_thumbnail = serializers.CharField(max_length=256, required=False)
    link_to_default_thumbnail = serializers.CharField(max_length=256, required=False)

    class Meta:
        
        fields = "__all__"

    


   
    