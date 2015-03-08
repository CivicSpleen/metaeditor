# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from social.backends.utils import load_backends


@login_required
def profile(request):
    template = 'accounts/profile.html'
    ctx = {
        'available_backends': load_backends(settings.AUTHENTICATION_BACKENDS)
    }
    return render_to_response(template, ctx, context_instance=RequestContext(request))
