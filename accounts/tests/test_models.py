# -*- coding: utf-8 -*-

import fudge

from django.contrib.auth.models import User
from django.test import TestCase


class SendSuccessRegistrationTest(TestCase):

    @fudge.patch(
        'accounts.models.mail_admins')
    def test_sends_email_on_user_creation(self, fake_mail):
        fake_mail.expects_call()
        User.objects.create_user('user1')

    @fudge.patch(
        'accounts.models.mail_admins',
        'accounts.models.logger.error')
    def test_logs_error(self, fake_mail, fake_error):
        fake_mail.expects_call()\
            .raises(Exception('My fake exception'))
        fake_error.expects_call()
        User.objects.create_user('user1')
