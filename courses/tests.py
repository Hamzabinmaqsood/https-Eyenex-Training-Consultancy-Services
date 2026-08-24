from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Course, CourseCategory


class CourseModelTests(TestCase):
    def test_category_can_be_created_and_returns_its_name(self):
        category = CourseCategory.objects.create(name='Occupational Health & Safety')

        self.assertEqual(str(category), 'Occupational Health & Safety')
        self.assertEqual(category.slug, 'occupational-health-safety')

    def test_duplicate_category_names_are_rejected_and_similar_slugs_are_unique(self):
        first = CourseCategory.objects.create(name='Fire & Safety')
        second = CourseCategory.objects.create(name='Fire Safety')

        self.assertEqual(first.slug, 'fire-safety')
        self.assertEqual(second.slug, 'fire-safety-2')
        with self.assertRaises(ValidationError):
            CourseCategory(name='Fire & Safety').full_clean()

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

    def test_generated_slug_and_collision_suffix_respect_field_length(self):
        long_title = 'Safety Training ' * 30
        first = Course.objects.create(
            title=long_title,
            short_description='Intro course',
            description='Details',
        )
        second = Course.objects.create(
            title=long_title,
            short_description='Intro course',
            description='Details',
        )

        self.assertLessEqual(len(first.slug), 220)
        self.assertLessEqual(len(second.slug), 220)
        self.assertTrue(second.slug.endswith('-2'))

    def test_course_fields_flags_choices_and_string_representation(self):
        category = CourseCategory.objects.create(name='Industrial Safety')
        course = Course.objects.create(
            category=category,
            title='Advanced Industrial Safety',
            short_description='Practical industrial safety training.',
            description='Full details.',
            fee=Decimal('12500.00'),
            level=Course.Level.ADVANCED,
            is_featured=True,
            is_active=True,
            display_order=2,
        )

        self.assertEqual(course.category, category)
        self.assertEqual(str(course), course.title)
        self.assertEqual(course.level, Course.Level.ADVANCED)
        self.assertEqual(course.get_level_display(), 'Advanced')
        self.assertTrue(course.is_featured)
        self.assertTrue(course.is_active)

    def test_negative_fee_is_rejected(self):
        course = Course(
            title='Invalid Fee Course',
            short_description='Summary.',
            description='Details.',
            fee=Decimal('-1.00'),
        )

        with self.assertRaises(ValidationError):
            course.full_clean()

    def test_negative_display_order_is_rejected(self):
        course = Course(
            title='Invalid Order Course',
            short_description='Summary.',
            description='Details.',
            display_order=-1,
        )

        with self.assertRaises(ValidationError):
            course.full_clean()


class CourseAdminTests(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username='course-admin',
            email='admin@example.com',
            password='test-password',
        )
        self.client.force_login(self.admin_user)

    def test_admin_lists_and_add_forms_manage_categories_and_courses(self):
        index_response = self.client.get(reverse('admin:index'))
        self.assertContains(index_response, 'Course Categories')
        self.assertContains(index_response, 'Courses')

        category_response = self.client.post(reverse('admin:courses_coursecategory_add'), {
            'name': 'Workplace Safety',
            'slug': 'workplace-safety',
            'description': 'Safety course category.',
            '_save': 'Save',
        })
        self.assertEqual(category_response.status_code, 302)
        category = CourseCategory.objects.get(slug='workplace-safety')

        course_response = self.client.post(reverse('admin:courses_course_add'), {
            'category': category.pk,
            'title': 'Workplace Safety Essentials',
            'slug': 'workplace-safety-essentials',
            'short_description': 'A concise course introduction.',
            'description': 'Complete course details.',
            'duration': '3 Days',
            'fee': '15000.00',
            'level': Course.Level.BEGINNER,
            'is_featured': 'on',
            'is_active': 'on',
            'display_order': '1',
            '_save': 'Save',
        })
        self.assertEqual(course_response.status_code, 302)
        course = Course.objects.get(slug='workplace-safety-essentials')
        self.assertEqual(course.category, category)
        self.assertEqual(course.fee, Decimal('15000.00'))

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
