from django.contrib import admin
from .models import Inquiry


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'course_display', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'phone', 'email', 'course__title', 'course_interested')
    list_editable = ('status',)
    autocomplete_fields = ('course',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
