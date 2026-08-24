from decimal import Decimal

from django.core.validators import MaxLengthValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify

from core.validators import validate_image_size


def unique_slugify(instance, value, slug_field_name='slug'):
    """Generate a unique slug for `instance` by appending -2, -3, ... on collision."""
    model = instance.__class__
    slug_field = instance._meta.get_field(slug_field_name)
    max_length = slug_field.max_length
    base_slug = (slugify(value) or model.__name__.lower())[:max_length].rstrip('-')
    slug = base_slug
    counter = 2

    while model.objects.filter(**{slug_field_name: slug}).exclude(pk=instance.pk).exists():
        suffix = f'-{counter}'
        slug = f'{base_slug[:max_length - len(suffix)].rstrip("-")}{suffix}'
        counter += 1

    return slug


class CourseCategory(models.Model):
    name = models.CharField('name', max_length=150, unique=True)
    slug = models.SlugField('slug', max_length=170, unique=True, blank=True)
    description = models.TextField('description', blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Course Category'
        verbose_name_plural = 'Course Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Course(models.Model):
    class Level(models.TextChoices):
        BEGINNER = 'beginner', 'Beginner'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        ADVANCED = 'advanced', 'Advanced'

    category = models.ForeignKey(
        CourseCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses'
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    short_description = models.TextField(
        validators=[MaxLengthValidator(500)],
        help_text='A concise summary for course cards and previews (maximum 500 characters).',
    )
    description = models.TextField()
    duration = models.CharField(max_length=100, blank=True)
    fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00'))],
    )
    level = models.CharField(
        max_length=20,
        choices=Level.choices,
        default=Level.BEGINNER,
    )
    image = models.ImageField(
        upload_to='courses/', blank=True, null=True, validators=[validate_image_size]
    )
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'title']

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
