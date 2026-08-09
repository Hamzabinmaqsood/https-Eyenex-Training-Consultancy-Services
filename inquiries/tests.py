from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Inquiry


class InquiryModelTests(TestCase):
    def test_valid_phone_passes_validation(self):
        inquiry = Inquiry(full_name='Zain', phone='+92 300 1234567')
        inquiry.full_clean()

    def test_invalid_phone_fails_validation(self):
        inquiry = Inquiry(full_name='Zain', phone='not-a-phone-number!!')
        with self.assertRaises(ValidationError):
            inquiry.full_clean()

    def test_course_display_falls_back_to_free_text(self):
        inquiry = Inquiry(full_name='Zain', phone='+92 300 1234567', course_interested='Fire Safety')
        self.assertEqual(inquiry.course_display, 'Fire Safety')

    def test_course_display_defaults_to_general_inquiry(self):
        inquiry = Inquiry(full_name='Zain', phone='+92 300 1234567')
        self.assertEqual(inquiry.course_display, 'General Inquiry')
