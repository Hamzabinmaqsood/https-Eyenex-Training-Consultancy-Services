import base64
from datetime import date, timedelta
from decimal import Decimal

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from courses.models import Course

from .models import AdmissionApplication, CourseAppointment


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


class CourseAppointmentTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title='NEBOSH IGC',
            short_description='NEBOSH course.',
            description='Course details.',
            duration='15 Days',
            fee=Decimal('180000.00'),
            appointment_fee=Decimal('2500.00'),
            delivery_mode=Course.DeliveryMode.BOTH,
            is_active=True,
        )
        self.url = reverse('admissions:course_appointment', args=[self.course.slug])

    def payment_image(self):
        png_bytes = base64.b64decode(
            'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII='
        )
        return SimpleUploadedFile('payment.png', png_bytes, content_type='image/png')

    def payload(self):
        return {
            'full_name': 'Ali Khan',
            'email': 'ali@example.com',
            'phone': '+92 300 1234567',
            'whatsapp_number': '+92 300 1234567',
            'city': 'Rawalpindi',
            'preferred_date': str(date.today() + timedelta(days=2)),
            'preferred_time': '14:30',
            'financial_aid_requested': '',
            'financial_aid_reason': '',
            'message': 'Please confirm the appointment.',
        }

    def test_appointment_page_loads_for_active_course(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Book an Appointment')
        self.assertContains(response, 'PKR 2,500')
        self.assertContains(response, '03408186889')
        self.assertContains(response, 'Raja Khizar Hayat')

    def test_payment_screenshot_required_when_fee_is_positive_without_aid(self):
        response = self.client.post(self.url, self.payload())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CourseAppointment.objects.count(), 0)
        self.assertContains(response, 'Please upload one screenshot')

    def test_valid_paid_appointment_saves_fee_snapshot(self):
        payload = self.payload()
        payload['payment_screenshot'] = self.payment_image()
        response = self.client.post(self.url, payload)
        self.assertRedirects(response, self.url)
        appointment = CourseAppointment.objects.get()
        self.assertEqual(appointment.course, self.course)
        self.assertEqual(appointment.appointment_fee, Decimal('2500.00'))
        self.assertFalse(appointment.financial_aid_requested)

    def test_financial_aid_requires_reason_and_does_not_require_screenshot(self):
        payload = self.payload()
        payload['financial_aid_requested'] = 'on'
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CourseAppointment.objects.count(), 0)
        self.assertContains(response, 'Please tell us why you need financial aid')

        payload['financial_aid_reason'] = 'I cannot afford the appointment fee at this time.'
        response = self.client.post(self.url, payload)
        self.assertRedirects(response, self.url)
        appointment = CourseAppointment.objects.get()
        self.assertTrue(appointment.financial_aid_requested)
        self.assertFalse(bool(appointment.payment_screenshot))

    def test_past_appointment_date_is_rejected(self):
        payload = self.payload()
        payload['preferred_date'] = str(date.today() - timedelta(days=1))
        payload['payment_screenshot'] = self.payment_image()
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CourseAppointment.objects.count(), 0)
        self.assertContains(response, 'Please choose today or a future date.')
