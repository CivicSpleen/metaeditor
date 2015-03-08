# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.test import TestCase


class ProfileTest(TestCase):
    def setUp(self):
        self.url = reverse('accounts:profile')

    def test_is_forbidden_for_anonymous(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)
