from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Testimonial


class TestimonialModelTests(TestCase):
    def test_rating_within_range_is_valid(self):
        testimonial = Testimonial(name='Ali', message='Great course', rating=5)
        testimonial.full_clean()

    def test_rating_above_max_is_invalid(self):
        testimonial = Testimonial(name='Ali', message='Great course', rating=6)
        with self.assertRaises(ValidationError):
            testimonial.full_clean()

    def test_rating_below_min_is_invalid(self):
        testimonial = Testimonial(name='Ali', message='Great course', rating=0)
        with self.assertRaises(ValidationError):
            testimonial.full_clean()


class TestimonialHomepageTests(TestCase):
    def test_only_active_testimonials_shown_on_homepage(self):
        Testimonial.objects.create(name='Active Reviewer', message='Loved it', is_active=True)
        Testimonial.objects.create(name='Hidden Reviewer', message='Not shown', is_active=False)

        response = self.client.get(reverse('core:home'))
        self.assertContains(response, 'Active Reviewer')
        self.assertNotContains(response, 'Hidden Reviewer')
