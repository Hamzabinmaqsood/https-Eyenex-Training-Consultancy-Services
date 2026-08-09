from django.db import models

from core.validators import phone_validator
from courses.models import Course


class AdmissionApplication(models.Model):
    STATUS_NEW = 'new'
    STATUS_REVIEWING = 'reviewing'
    STATUS_CONTACTED = 'contacted'
    STATUS_ACCEPTED = 'accepted'
    STATUS_ENROLLED = 'enrolled'
    STATUS_REJECTED = 'rejected'
    STATUS_CLOSED = 'closed'

    STATUS_CHOICES = [
        (STATUS_NEW, 'New'),
        (STATUS_REVIEWING, 'Reviewing'),
        (STATUS_CONTACTED, 'Contacted'),
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_ENROLLED, 'Enrolled'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_CLOSED, 'Closed'),
    ]

    CONTACT_METHOD_CHOICES = [
        ('phone', 'Phone Call'),
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
    ]

    full_name = models.CharField(max_length=120)
    father_name = models.CharField(max_length=120, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, validators=[phone_validator])
    whatsapp_number = models.CharField(max_length=20, blank=True, validators=[phone_validator])
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Pakistan')

    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='applications',
    )
    course_interested = models.CharField(
        max_length=150,
        blank=True,
        help_text='Used when the course of interest is not yet in the catalogue.',
    )

    education = models.CharField(max_length=150, blank=True)
    occupation = models.CharField(max_length=150, blank=True)
    preferred_contact_method = models.CharField(
        max_length=20, choices=CONTACT_METHOD_CHOICES, default='phone'
    )
    message = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Admission Application'
        verbose_name_plural = 'Admission Applications'

    def __str__(self):
        return f'{self.full_name} - {self.course_display}'

    @property
    def course_display(self):
        return self.course.title if self.course else self.course_interested or 'General Inquiry'
