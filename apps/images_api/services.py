from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image

from apps.images_api.models import Thumbnail, UploadedImage


class ThumbnailService:
    @classmethod
    def make_thumbnail(cls, image_id, size):
        basic_thumb = BytesIO()
        upload_image_instance = UploadedImage.objects.get(id=image_id)
        image = upload_image_instance.uploaded_image
        img: Image.Image = Image.open(image.path)

        img.thumbnail((size, size))
        img.save(basic_thumb, format='PNG')
        thumbnail = InMemoryUploadedFile(
            basic_thumb,
            None,
            f"thumb.png",
            "image/png",
            basic_thumb.tell,
            None
        )

        thumbnail_created = Thumbnail.objects.create(thumbnail=thumbnail, thumbnail_size=size, original_image=upload_image_instance)
        return thumbnail_created