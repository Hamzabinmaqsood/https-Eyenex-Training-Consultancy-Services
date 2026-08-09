import base64

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import GalleryImage

# A minimal valid 1x1 pixel PNG, used as a stand-in upload for tests.
ONE_PIXEL_PNG = base64.b64decode(
    'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII='
)


def make_test_image(name='test.png'):
    return SimpleUploadedFile(name, ONE_PIXEL_PNG, content_type='image/png')


class GalleryPageTests(TestCase):
    def setUp(self):
        self.active_image = GalleryImage.objects.create(
            title='Visible Image', image=make_test_image('visible.png'), is_active=True
        )
        self.inactive_image = GalleryImage.objects.create(
            title='Hidden Image', image=make_test_image('hidden.png'), is_active=False
        )

    def test_gallery_page_loads(self):
        response = self.client.get(reverse('gallery:gallery'))
        self.assertEqual(response.status_code, 200)

    def test_active_image_is_shown(self):
        response = self.client.get(reverse('gallery:gallery'))
        self.assertContains(response, 'Visible Image')

    def test_inactive_image_is_hidden(self):
        response = self.client.get(reverse('gallery:gallery'))
        self.assertNotContains(response, 'Hidden Image')
