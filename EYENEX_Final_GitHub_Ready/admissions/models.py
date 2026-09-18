from django.db import models

from core.storage import PrivateMediaStorage
from core.validators import phone_validator, validate_image_size
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


class CourseAppointment(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_REVIEWING = 'reviewing'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_COMPLETED = 'completed'
    STATUS_DECLINED = 'declined'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_REVIEWING, 'Reviewing'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_DECLINED, 'Declined'),
    ]

    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name='appointments',
    )
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20, validators=[phone_validator])
    whatsapp_number = models.CharField(max_length=20, blank=True, validators=[phone_validator])
    city = models.CharField(max_length=100)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    message = models.TextField(blank=True)

    appointment_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='Snapshot of the appointment fee at the time the student submitted the request.',
    )
    payment_screenshot = models.ImageField(
        storage=PrivateMediaStorage(),
        upload_to='appointments/payment_receipts/%Y/%m/',
        blank=True,
        null=True,
        validators=[validate_image_size],
    )
    financial_aid_requested = models.BooleanField(default=False)
    financial_aid_reason = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Course Appointment'
        verbose_name_plural = 'Course Appointments'

    def __str__(self):
        return f'{self.full_name} - {self.course.title}'

    @property
    def appointment_fee_display(self):
        return f'PKR {self.appointment_fee:,.0f}'
