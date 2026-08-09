from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from courses.models import Course


class StaticViewSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return [
            'core:home',
            'core:about',
            'core:contact',
            'admissions:admissions',
            'admissions:apply',
            'courses:course_list',
            'gallery:gallery',
            'faqs:faq_list',
            'core:privacy_policy',
            'core:terms',
        ]

    def location(self, item):
        return reverse(item)


class CourseSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Course.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('courses:course_detail', args=[obj.slug])
