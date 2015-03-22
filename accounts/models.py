# -*- coding: utf-8 -*-
import logging

from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import mail_admins
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def send_success_registration(sender, **kwargs):
    """ Notificates admin via email on new user creation. """
    if kwargs.get('created'):
        user = kwargs['instance']
        subject = 'New registration.'
        tmpl = 'editor/emails/success_registration.txt'
        html_tmpl = 'editor/emails/success_registration.html'

        site_domain = settings.SITE_DOMAIN
        user_edit_url = reverse('admin:auth_user_change', args=[user.id])
        ctx = {'user_edit_url': 'http://%s%s' % (site_domain, user_edit_url)}
        message = render_to_string(tmpl, ctx)
        html_message = render_to_string(html_tmpl, ctx)
        try:
            mail_admins(
                subject, message, fail_silently=False,
                html_message=html_message)
        except Exception as exc:
            logger.error(u'New registration message sending failed because of %s' % exc)

post_save.connect(send_success_registration, sender=User)
