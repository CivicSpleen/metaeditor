# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase


class ProfileTest(TestCase):
    def setUp(self):
        self.url = reverse('accounts:profile')
        self.user1 = User.objects.get_or_create(username='tester1')[0]
        self.user1.set_password('1')
        self.user1.save()
        logged_in = self.client.login(username=self.user1.username, password='1')
        self.assertTrue(logged_in)

    def test_is_forbidden_for_anonymous(self):
        self.client.logout()
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_renders_user_for_authenticated(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
