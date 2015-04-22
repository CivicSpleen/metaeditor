# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import messages
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

    def form_invalid(self, form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        messages.add_message(self.request, messages.ERROR, 'Submitted form is invalid.')
        return super(UserUpdate, self).form_invalid(form)

    def get_success_url(self, *args, **kwargs):
        messages.add_message(self.request, messages.SUCCESS, 'Profile saved.')
        if 'save-and-continue' in self.request.POST:
            return reverse('accounts:profile')
        return reverse('dataset-list')
