from django.db import models
from django.utils.text import slugify

from core.validators import validate_image_size


def unique_slugify(instance, value, slug_field_name='slug'):
    """Generate a unique slug for `instance` by appending -2, -3, ... on collision."""
    model = instance.__class__
    base_slug = slugify(value) or model.__name__.lower()
    slug = base_slug
    counter = 2

    while model.objects.filter(**{slug_field_name: slug}).exclude(pk=instance.pk).exists():
        slug = f'{base_slug}-{counter}'
        counter += 1

    return slug


class CourseCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Course Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    category = models.ForeignKey(
        CourseCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses'
    )
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.CharField(max_length=100, blank=True)
    fee = models.CharField(max_length=100, blank=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    image = models.ImageField(
        upload_to='courses/', blank=True, null=True, validators=[validate_image_size]
    )
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def related_courses(self):
        if not self.category_id:
            return Course.objects.none()

        return Course.objects.filter(
            category_id=self.category_id, is_active=True
        ).exclude(pk=self.pk)[:3]
