from django.test import TestCase

# Create your tests here.

# Example test (optional)
class BasicTestCase(TestCase):
    def test_homepage_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
