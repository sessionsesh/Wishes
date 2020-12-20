from django.test import TestCase

from django.test import TestCase
from django.contrib.auth.models import User 

class UserAddCase(TestCase):
    def setUp(self):
        for i in range(333):
            User.objects.create(username="test" + str(i), password="test")

    def test_users(self):
        self.setUp()