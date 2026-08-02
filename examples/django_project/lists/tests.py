from snapshottest.django import TestCase

from .models import List


class ListTest(TestCase):
    def test_uses_home_template(self):
        List.objects.create(name="test")
        response = self.client.get("/")
        self.assertMatchSnapshot(response.content.decode())
