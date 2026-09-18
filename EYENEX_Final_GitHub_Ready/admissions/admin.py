from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import AdmissionApplication, CourseAppointment


@admin.register(AdmissionApplication)
class AdmissionApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'phone',
        'course_display',
        'city',
        'status',
        'created_at',
    )
    list_filter = ('status', 'preferred_contact_method', 'country', 'created_at')
    search_fields = (
        'full_name',
        'father_name',
        'email',
        'phone',
        'whatsapp_number',
        'city',
        'course__title',
        'course_interested',
    )
    list_editable = ('status',)
    autocomplete_fields = ('course',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    fieldsets = (
        ('Applicant', {
            'fields': ('full_name', 'father_name', 'email', 'phone', 'whatsapp_number', 'preferred_contact_method')
        }),
        ('Location', {
            'fields': ('city', 'country')
        }),
        ('Course & Background', {
            'fields': ('course', 'course_interested', 'education', 'occupation', 'message')
        }),
        ('Status', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )


@admin.register(CourseAppointment)
class CourseAppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'course',
        'phone',
        'preferred_date',
        'preferred_time',
        'appointment_fee',
        'financial_aid_requested',
        'status',
        'created_at',
    )
    list_filter = ('status', 'financial_aid_requested', 'course', 'preferred_date', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'whatsapp_number', 'city', 'course__title')
    list_editable = ('status',)
    autocomplete_fields = ('course',)
    readonly_fields = ('appointment_fee', 'payment_screenshot_preview', 'created_at', 'updated_at')
    ordering = ('-created_at',)

    @admin.display(description='Payment screenshot')
    def payment_screenshot_preview(self, obj):
        if not obj or not obj.pk or not obj.payment_screenshot:
            return 'No screenshot uploaded'
        url = reverse('admissions:payment_receipt', args=[obj.pk])
        return format_html('<a href="{}" target="_blank" rel="noopener">View payment screenshot</a>', url)

    fieldsets = (
        ('Student', {
            'fields': ('full_name', 'email', 'phone', 'whatsapp_number', 'city')
        }),
        ('Appointment', {
            'fields': ('course', 'preferred_date', 'preferred_time', 'message', 'appointment_fee')
        }),
        ('Payment / Financial Aid', {
            'fields': ('payment_screenshot_preview', 'financial_aid_requested', 'financial_aid_reason')
        }),
        ('Status', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )
