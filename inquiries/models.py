from django.db import models

from core.validators import phone_validator
from courses.models import Course


class Inquiry(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('enrolled', 'Enrolled'),
        ('closed', 'Closed'),
    ]

    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30, validators=[phone_validator])
    email = models.EmailField(blank=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='inquiries',
    )
    course_interested = models.CharField(
        max_length=150,
        blank=True,
        help_text='Used when the course of interest is not in the catalogue.',
    )
    message = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Inquiries"

    def __str__(self):
        return f"{self.full_name} - {self.phone}"

    @property
    def course_display(self):
        return self.course.title if self.course else self.course_interested or 'General Inquiry'
