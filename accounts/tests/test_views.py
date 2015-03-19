# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from accounts.tests.factories import UserFactory


class ProfileTest(TestCase):
    def setUp(self):
        self.url = reverse('accounts:profile')
        self.user1 = UserFactory()
        logged_in = self.client.login(
            username=self.user1.username, password='1')
        self.assertTrue(logged_in)

    def test_is_forbidden_for_anonymous(self):
        self.client.logout()
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_renders_user_form_for_authenticated(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('name="first_name"', resp.content)
        self.assertIn('name="last_name"', resp.content)
        self.assertIn('name="email"', resp.content)

    def test_changes_user_data_on_post(self):
        post_data = {
            'first_name': '%s updated' % self.user1.first_name,
            'last_name': '%s updated' % self.user1.last_name,
            'email': 'updated_%s' % self.user1.email
        }
        resp = self.client.post(self.url, post_data)
        self.assertEqual(resp.status_code, 302)

        updated_user = User.objects.get(username=self.user1.username)

        # is it the same object?
        self.assertEqual(updated_user.id, self.user1.id)

        self.assertEqual(
            updated_user.first_name,
            '%s updated' % self.user1.first_name)

        self.assertEqual(
            updated_user.last_name,
            '%s updated' % self.user1.last_name)

        self.assertEqual(
            updated_user.email,
            'updated_%s' % self.user1.email)
