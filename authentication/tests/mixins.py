from django.test import TestCase

from common.test_mixins import TestMixin


class AbstractTestCase(TestCase, TestMixin):

    def setUp(self):
        """Set up test data to be shared by the entire test case."""

        self.user = self.create_user()
        self.superuser = self.create_user(superuser=True)
