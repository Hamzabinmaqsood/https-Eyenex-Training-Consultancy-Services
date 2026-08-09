from django.test import TestCase
from django.urls import reverse

from .models import AdmissionApplication


class AdmissionsPageTests(TestCase):
    def test_admissions_page_loads(self):
        response = self.client.get(reverse('admissions:admissions'))
        self.assertEqual(response.status_code, 200)

    def test_apply_page_loads(self):
        response = self.client.get(reverse('admissions:apply'))
        self.assertEqual(response.status_code, 200)


class AdmissionApplicationSubmissionTests(TestCase):
    def valid_payload(self):
        return {
            'full_name': 'Sara Malik',
            'father_name': 'Malik Ahmed',
            'email': 'sara@example.com',
            'phone': '+92 300 1234567',
            'whatsapp_number': '+92 300 1234567',
            'city': 'Lahore',
            'country': 'Pakistan',
            'course': '',
            'course_interested': 'HSE Training',
            'education': 'Bachelors',
            'occupation': 'Engineer',
            'preferred_contact_method': 'whatsapp',
            'message': 'Please contact me.',
        }

    def test_valid_application_saves_and_redirects(self):
        response = self.client.post(reverse('admissions:apply'), self.valid_payload())
        self.assertRedirects(response, reverse('admissions:apply'))
        self.assertEqual(AdmissionApplication.objects.count(), 1)

    def test_invalid_application_does_not_save(self):
        response = self.client.post(reverse('admissions:apply'), {
            'full_name': '',
            'email': 'not-an-email',
            'phone': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(AdmissionApplication.objects.count(), 0)

    def test_application_without_course_selection_is_rejected(self):
        payload = self.valid_payload()
        payload['course_interested'] = ''
        response = self.client.post(reverse('admissions:apply'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(AdmissionApplication.objects.count(), 0)

    def test_duplicate_submission_within_window_is_not_double_saved(self):
        payload = self.valid_payload()
        self.client.post(reverse('admissions:apply'), payload)
        self.client.post(reverse('admissions:apply'), payload)
        self.assertEqual(AdmissionApplication.objects.count(), 1)
