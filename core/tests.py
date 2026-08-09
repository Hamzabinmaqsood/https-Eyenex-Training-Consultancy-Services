from django.test import TestCase
from django.urls import reverse

from inquiries.models import Inquiry


class StaticPageTests(TestCase):
    def test_home_returns_200(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)

    def test_about_returns_200(self):
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)

    def test_privacy_policy_returns_200(self):
        response = self.client.get(reverse('core:privacy_policy'))
        self.assertEqual(response.status_code, 200)

    def test_terms_returns_200(self):
        response = self.client.get(reverse('core:terms'))
        self.assertEqual(response.status_code, 200)

    def test_future_service_pages_return_200(self):
        for url_name in ['core:ielts', 'core:study_abroad', 'core:leadership']:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 200)


class ContactInquiryTests(TestCase):
    def test_contact_page_loads(self):
        response = self.client.get(reverse('core:contact'))
        self.assertEqual(response.status_code, 200)

    def test_valid_inquiry_can_be_submitted_and_redirects(self):
        response = self.client.post(reverse('core:contact'), {
            'full_name': 'Ayesha Khan',
            'phone': '+92 300 1234567',
            'email': 'ayesha@example.com',
            'course_interested': 'NEBOSH Preparation',
            'message': 'I would like more details.',
        })
        self.assertRedirects(response, reverse('core:contact'))
        self.assertEqual(Inquiry.objects.count(), 1)

    def test_invalid_inquiry_is_rejected(self):
        response = self.client.post(reverse('core:contact'), {
            'full_name': '',
            'phone': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Inquiry.objects.count(), 0)

    def test_duplicate_submission_within_window_is_not_double_saved(self):
        payload = {
            'full_name': 'Bilal Ahmed',
            'phone': '+92 301 1112222',
            'email': 'bilal@example.com',
            'course_interested': 'Fire Safety',
            'message': 'Interested.',
        }
        self.client.post(reverse('core:contact'), payload)
        self.client.post(reverse('core:contact'), payload)
        self.assertEqual(Inquiry.objects.count(), 1)


class SEOTests(TestCase):
    def test_robots_txt_loads(self):
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)

    def test_sitemap_xml_loads(self):
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)


class BrandingTests(TestCase):
    def test_no_old_meridian_branding_on_public_pages(self):
        public_urls = [
            reverse('core:home'),
            reverse('core:about'),
            reverse('core:contact'),
            reverse('courses:course_list'),
            reverse('gallery:gallery'),
            reverse('faqs:faq_list'),
            reverse('admissions:admissions'),
            reverse('admissions:apply'),
            reverse('core:privacy_policy'),
            reverse('core:terms'),
        ]

        for url in public_urls:
            response = self.client.get(url)
            content = response.content.decode().lower()
            self.assertNotIn('meridian', content, f'Old branding found on {url}')
