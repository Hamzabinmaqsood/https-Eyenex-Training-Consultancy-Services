from django.contrib import admin
from .models import CourseCategory, Course


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'duration',
        'fee',
        'level',
        'is_featured',
        'is_active',
        'display_order',
    )
    list_filter = ('category', 'level', 'is_featured', 'is_active')
    search_fields = ('title', 'short_description', 'description')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_featured', 'is_active', 'display_order')
    autocomplete_fields = ('category',)
    ordering = ('display_order', 'title')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'title', 'slug', 'short_description', 'description'),
        }),
        ('Course Information', {
            'fields': ('duration', 'fee', 'level', 'image'),
        }),
        ('Publishing', {
            'fields': ('is_featured', 'is_active', 'display_order'),
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
