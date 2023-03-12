from django.core.exceptions import ValidationError

from apps.images_api.constants import MAX_FILESIZE


def validate_file_size(value):
    filesize = value.size
    if filesize > MAX_FILESIZE:
        raise ValidationError("You cannot upload file more than 25Mb")
    else:
        return value
