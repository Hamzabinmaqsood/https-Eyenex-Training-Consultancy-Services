from django.contrib import admin

from .models import AdmissionApplication


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
