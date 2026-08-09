from django.test import TestCase
from django.urls import reverse

from .models import Course, CourseCategory


class CourseModelTests(TestCase):
    def test_duplicate_titles_get_unique_slugs(self):
        first = Course.objects.create(
            title='Safety Officer Training',
            short_description='Intro course',
            description='Details',
        )
        second = Course.objects.create(
            title='Safety Officer Training',
            short_description='Intro course',
            description='Details',
        )
        self.assertNotEqual(first.slug, second.slug)


class CourseViewTests(TestCase):
    def setUp(self):
        self.category = CourseCategory.objects.create(name='Safety')
        self.active_course = Course.objects.create(
            title='NEBOSH Preparation',
            short_description='Exam preparation course',
            description='Full details about NEBOSH preparation.',
            category=self.category,
            is_active=True,
        )
        self.inactive_course = Course.objects.create(
            title='Draft Course',
            short_description='Not ready yet',
            description='Draft description',
            is_active=False,
        )

    def test_course_list_loads(self):
        response = self.client.get(reverse('courses:course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'NEBOSH Preparation')

    def test_active_course_detail_loads(self):
        response = self.client.get(
            reverse('courses:course_detail', args=[self.active_course.slug])
        )
        self.assertEqual(response.status_code, 200)

    def test_inactive_course_not_publicly_accessible(self):
        response = self.client.get(
            reverse('courses:course_detail', args=[self.inactive_course.slug])
        )
        self.assertEqual(response.status_code, 404)

    def test_course_search_matches_title(self):
        response = self.client.get(reverse('courses:course_list'), {'q': 'NEBOSH'})
        self.assertContains(response, 'NEBOSH Preparation')

    def test_course_search_excludes_non_matching(self):
        response = self.client.get(reverse('courses:course_list'), {'q': 'zzz-no-match'})
        self.assertNotContains(response, 'NEBOSH Preparation')

    def test_category_filter_works(self):
        response = self.client.get(
            reverse('courses:course_list'), {'category': self.category.slug}
        )
        self.assertContains(response, 'NEBOSH Preparation')
