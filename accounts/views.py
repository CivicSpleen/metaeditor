# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.views.generic.edit import UpdateView

from social.backends.utils import load_backends


class UserUpdate(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'accounts/profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        kwargs['available_backends'] = load_backends(settings.AUTHENTICATION_BACKENDS)
        return kwargs

    def get_success_url(self, *args, **kwargs):
        return reverse('accounts:profile')
