from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.validators import validate_image_size


class Testimonial(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=150, blank=True)
    message = models.TextField()
    image = models.ImageField(
        upload_to='testimonials/', blank=True, null=True, validators=[validate_image_size]
    )

    rating = models.PositiveSmallIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return self.name
