from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r'^\+?[0-9\s\-()]{7,20}$',
    message='Enter a valid phone number (digits, spaces, +, -, or () only).',
)

MAX_IMAGE_UPLOAD_SIZE_MB = 5


def validate_image_size(image):
    max_bytes = MAX_IMAGE_UPLOAD_SIZE_MB * 1024 * 1024

    if image.size > max_bytes:
        raise ValidationError(f'Image file size must not exceed {MAX_IMAGE_UPLOAD_SIZE_MB}MB.')
