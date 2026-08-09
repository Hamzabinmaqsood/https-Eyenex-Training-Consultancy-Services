from django.test import TestCase
from django.urls import reverse

from .models import FAQ


class FAQPageTests(TestCase):
    def setUp(self):
        self.active_faq = FAQ.objects.create(
            question='Visible question', answer='Visible answer', is_active=True
        )
        self.inactive_faq = FAQ.objects.create(
            question='Hidden question', answer='Hidden answer', is_active=False
        )

    def test_faq_page_loads(self):
        response = self.client.get(reverse('faqs:faq_list'))
        self.assertEqual(response.status_code, 200)

    def test_active_faq_is_shown(self):
        response = self.client.get(reverse('faqs:faq_list'))
        self.assertContains(response, 'Visible question')

    def test_inactive_faq_is_hidden(self):
        response = self.client.get(reverse('faqs:faq_list'))
        self.assertNotContains(response, 'Hidden question')
