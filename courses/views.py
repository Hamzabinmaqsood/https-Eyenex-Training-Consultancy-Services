from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Course, CourseCategory


def course_list(request):
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()

    courses = Course.objects.filter(is_active=True).select_related('category')

    if query:
        courses = courses.filter(
            Q(title__icontains=query)
            | Q(short_description__icontains=query)
            | Q(description__icontains=query)
            | Q(category__name__icontains=query)
        ).distinct()

    if category_slug:
        courses = courses.filter(category__slug=category_slug)

    context = {
        'courses': courses,
        'categories': CourseCategory.objects.all(),
        'query': query,
        'selected_category': category_slug,
    }

    return render(request, 'courses/course_list.html', context)


def course_detail(request, slug):
    course = get_object_or_404(
        Course.objects.select_related('category'), slug=slug, is_active=True
    )

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'related_courses': course.related_courses(),
    })
