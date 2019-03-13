from django.test import Client, TestCase
from django.urls import reverse


class FrontPageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.response = self.client.get(reverse('books:front_page'))

    def test_frontpage_response(self):
        self.assertEqual(self.response.status_code, 200)

    def test_frontpage_response_invalid(self):
        self.assertNotEqual(self.response.status_code, 404)

    def test_frontpage_content(self):
        self.assertIn('html', self.response.content.decode('utf-8'))
        # self.assertEqual(self.response.content.decode('utf-8'), {})

    def test_frontpage_content_invalid(self):
        self.assertNotEqual(self.response.content.decode('utf-8'), {})
