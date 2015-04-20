# -*- coding: utf-8 -*-
import json
import logging

import requests

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import URLValidator
from django.db.models import Q, Count
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404

from django.views.decorators.http import require_POST
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from editor.forms import DatasetForm, DataFileFormset, DocumentFileFormset, ScrapeForm,\
    SourceForm, CategoryForm, FormatForm
from editor.models import Category, Source, Format, Dataset
from editor.utils import get_links, filter_links, guess_format

logger = logging.getLogger(__name__)


class IndexView(View):
    template_name = 'editor/index.html'

    def get(self, request):
        return render(request, self.template_name)


class BaseTreeView(ListView):
    template_name = 'editor/tree.html'

    def get_context_data(self, **kwargs):
        # do not show parent node
        kwargs['nodes'] = self.model.objects.filter(parent__isnull=False)
        kwargs['create_url'] = self.model.get_create_url()
        kwargs['has_add_perm'] = self.request.user.has_perm(
            'editor.add_%s' % self.model._meta.model_name)
        kwargs['has_change_perm'] = self.request.user.has_perm(
            'editor.change_%s' % self.model._meta.model_name)
        kwargs['page_name'] = '%s-tree' % self.model._meta.model_name
        return kwargs


class BaseCreateView(CreateView):
    template_name = 'editor/tree.html'

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden('Forbidden for anonymous users.')
        if not request.user.has_perm('editor.add_%s' % self.model._meta.model_name):
            return HttpResponseForbidden('You do not have permission to perform this action.')
        return super(BaseCreateView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Saved.')
        return super(BaseCreateView, self).get_success_url()

    def form_invalid(self, form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        messages.add_message(self.request, messages.ERROR, 'Submitted form is invalid.')
        return super(BaseCreateView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        # do not render root node
        kwargs['nodes'] = self.model.objects.filter(parent__isnull=False)

        kwargs['create_url'] = self.model.get_create_url()
        kwargs['has_add_perm'] = self.request.user.has_perm(
            'editor.add_%s' % self.model._meta.model_name)
        kwargs['has_change_perm'] = self.request.user.has_perm(
            'editor.change_%s' % self.model._meta.model_name)
        # TODO: remove copy/paste. See get_initial method.
        try:
            parent_pk = int(self.request.GET.get('parent', 0))
            kwargs['selected_node'] = self.model.objects.get(pk=parent_pk)
        except (TypeError, ValueError, self.model.DoesNotExist):
            # TODO: add warning to logger because it is client side bug.
            pass
        return kwargs

    def get_initial(self):
        initial = super(BaseCreateView, self).get_initial()
        try:
            parent_pk = int(self.request.GET.get('parent', 0))
            initial['parent'] = self.model.objects.get(pk=parent_pk)
        except (TypeError, ValueError, self.model.DoesNotExist):
            # TODO: add warning to logger because it is client side bug.
            pass
        return initial


class BaseUpdateView(UpdateView):
    template_name = 'editor/tree.html'

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden('Forbidden for anonymous users.')
        if not request.user.has_perm('editor.change_%s' % self.model._meta.model_name):
            return HttpResponseForbidden('You do not have permission to perform this action.')
        return super(BaseUpdateView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Saved.')
        return super(BaseUpdateView, self).get_success_url()

    def form_invalid(self, form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        messages.add_message(self.request, messages.ERROR, 'Submitted form is invalid.')
        return super(BaseUpdateView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        """
        Returns context of the template.
        """
        kwargs['nodes'] = self.model.objects.filter(parent__isnull=False)
        kwargs['create_url'] = self.model.get_create_url()
        kwargs['selected_node'] = self.object
        kwargs['has_add_perm'] = self.request.user.has_perm(
            'editor.add_%s' % self.model._meta.model_name)
        kwargs['has_change_perm'] = self.request.user.has_perm(
            'editor.change_%s' % self.model._meta.model_name)
        return kwargs


class CategoryList(BaseTreeView):
    model = Category


class CategoryCreate(BaseCreateView):
    model = Category
    form_class = CategoryForm


class CategoryUpdate(BaseUpdateView):
    model = Category
    form_class = CategoryForm


class SourceList(BaseTreeView):
    model = Source


class SourceCreate(BaseCreateView):
    model = Source
    form_class = SourceForm
    template_name = 'editor/source_form.html'

    def form_valid(self, form):
        """
        Called if form is valid. Saves form and redirects to success page.
        """
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class SourceUpdate(BaseUpdateView):
    model = Source
    form_class = SourceForm
    template_name = 'editor/source_form.html'

    def get_context_data(self, **kwargs):
        ctx = super(SourceUpdate, self).get_context_data(**kwargs)
        if self.request.user.has_perm('editor.add_%s' % self.model._meta.model_name):
            ctx['create_dataset_url'] = reverse(
                'editor:dataset-create',
                kwargs={'source_pk': self.object.pk})
        return ctx

    def form_valid(self, form):
        """
        Called if form is valid. Saves form and redirects to success page.
        """
        source = form.save(commit=False)
        source.updated_by = self.request.user
        source.save()
        return HttpResponseRedirect(self.get_success_url())


class FormatList(BaseTreeView):
    model = Format


class FormatCreate(BaseCreateView):
    model = Format
    fields = ['name', 'parent']
    form_class = FormatForm


class FormatUpdate(BaseUpdateView):
    model = Format
    form_class = FormatForm


class DatasetList(ListView):
    model = Dataset
    paginate_by = 50

    def get_queryset(self, *args, **kwargs):
        qs = super(DatasetList, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get('query')
        qs = qs.annotate(
            datafile__count=Count('datafile'),
            documentfile__count=Count('documentfile'))

        if query:
            qs = qs.filter(
                Q(title__icontains=query)
                | Q(source__name__icontains=query)
                | Q(page__icontains=query))

        order_by = self.request.GET.get('o')
        ORDER_FIELDS = ('title', 'source__name', 'page', 'datafile__count', 'documentfile__count')
        if order_by not in ORDER_FIELDS:
            order_by = None
        if order_by:
            qs = qs.order_by(order_by)
        return qs.select_related('source')

    def get_context_data(self, **kwargs):
        ctx = super(DatasetList, self).get_context_data(**kwargs)
        ctx['query'] = self.request.GET.get('query', '')
        return ctx


class DatasetEditMixin(object):
    def get_formset_instance(self):
        """
        Returns an instance of the formset.
        """
        raise NotImplementedError('Implement me')

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = self.get_formset_instance()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        datafile_formset = DataFileFormset(prefix='datafile', instance=self.object, auto_id=False)
        docfile_formset = DocumentFileFormset(prefix='documentfile', instance=self.object)
        return self.render_to_response(
            self.get_context_data(
                form=form,
                datafile_formset=datafile_formset,
                docfile_formset=docfile_formset))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = self.get_formset_instance()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        datafile_formset = DataFileFormset(
            self.request.POST, prefix='datafile', instance=self.object)
        docfile_formset = DocumentFileFormset(
            self.request.POST, prefix='documentfile', instance=self.object)

        if (form.is_valid() and datafile_formset.is_valid() and docfile_formset.is_valid()):
            return self.form_valid(form, datafile_formset, docfile_formset)
        else:
            return self.form_invalid(form, datafile_formset, docfile_formset)

    def get_success_url(self):
        """
        Returns url where to redirect after success save.
        """
        messages.add_message(self.request, messages.SUCCESS, 'Dataset saved.')
        return self.object.get_absolute_url()

    def form_valid(self, form, datafile_formset, docfile_formset):
        """
        Called if form and formsets are valid. Saves forms and redirects to success page.
        """
        self.object = form.save()
        datafile_formset.instance = self.object
        datafile_formset.save()

        docfile_formset.instance = self.object
        docfile_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, datafile_formset, docfile_formset):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        messages.add_message(self.request, messages.ERROR, 'Submitted form is invalid.')
        return self.render_to_response(
            self.get_context_data(
                form=form,
                datafile_formset=datafile_formset,
                docfile_formset=docfile_formset))


class DatasetCreate(DatasetEditMixin, CreateView):
    model = Dataset
    form_class = DatasetForm

    def dispatch(self, request, *args, **kwargs):
        self.source = get_object_or_404(Source, pk=self.kwargs['source_pk'])
        return super(DatasetCreate, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.has_perm('editor.add_%s' % self.model._meta.model_name):
            return HttpResponseForbidden('You do not have permission to perform this action.')
        return super(DatasetCreate, self).post(request, *args, **kwargs)

    def get_formset_instance(self):
        """
        Returns an instance of the formset.
        """
        return None

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        form_kwargs = self.get_form_kwargs()
        form_kwargs['source'] = self.source
        return form_class(self.request.user, **form_kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(DatasetCreate, self).get_context_data(**kwargs)
        ctx['has_add_perm'] = self.request.user.has_perm(
            'editor.add_%s' % self.model._meta.model_name)
        ctx['has_change_perm'] = self.request.user.has_perm(
            'editor.change_%s' % self.model._meta.model_name)
        return ctx


class DatasetUpdate(DatasetEditMixin, UpdateView):
    model = Dataset
    form_class = DatasetForm

    def post(self, request, *args, **kwargs):
        if not request.user.has_perm('editor.change_%s' % self.model._meta.model_name):
            return HttpResponseForbidden('You do not have permission to perform this action.')
        return super(DatasetUpdate, self).post(request, *args, **kwargs)

    def get_formset_instance(self):
        """
        Returns an instance of the formset.
        """
        return self.get_object()

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        return form_class(self.request.user, **self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        ctx = super(DatasetUpdate, self).get_context_data(**kwargs)
        ctx['has_add_perm'] = self.request.user.has_perm(
            'editor.add_%s' % self.model._meta.model_name)
        ctx['has_change_perm'] = self.request.user.has_perm(
            'editor.change_%s' % self.model._meta.model_name)
        return ctx


@require_POST
@login_required
def scrape(request):
    has_perm = request.user.has_perm('editor.add_datafile')\
        and request.user.has_perm('editor.add_documentfile')
    if not has_perm:
        return HttpResponseForbidden('You do not have permission to perform this action.')
    response_data = {}
    form = ScrapeForm(request.POST)

    # find which extensions should be included to the response.
    include_extensions = []
    if 'documentfiles' in request.GET:
        include_extensions.extend(settings.EDITOR_DOCUMENT_EXTENSIONS)
    if 'datafiles' in request.GET:
        include_extensions.extend(settings.EDITOR_DATAFILE_EXTENSIONS)

    if form.is_valid():
        try:
            # find all urls on remote site.
            links = get_links(form.cleaned_data['url'])

            # keep the links match to extensions to include only.
            links = filter_links(links, include_extensions)

            links = guess_format(links)

            response_data['links'] = links
        except Exception as exc:
            response_data['errors'] = [u'Failed to get urls. Please, try later.']
            logger.error(
                u'Failed to retrieve links from %s because of %s' % (form.cleaned_data['url'], exc))
    else:
        # form has errors, collect them and add to response.
        errors = []
        for field, field_errors in form.errors.iteritems():
            errors.append('%s' % '; '.join(field_errors))
        response_data['errors'] = errors

    return HttpResponse(
        json.dumps(response_data),
        content_type='application/json')


@require_POST
@login_required
def validate_url(request):
    """ Validates given url and checks for its existance. """

    # let it fail if client side does not give url. That means client side error.
    url = request.POST['url']

    response_data = {}

    # validate url format.
    validate = URLValidator()
    error = None

    try:
        validate(url)
    except ValidationError, e:
        error = '; '.join(e.messages)

    if not error:
        # it is valid. What about existance?
        try:
            resp = requests.head(url)
            if resp.status_code != 200:
                error = '%s %s' % (resp.status_code, resp.reason)
        except Exception, exc:
            logger.error(
                u'Failed to validate existance of `%s` because of `%s`.' % (url, exc))
            error = 'Not available.'

    if error:
        response_data['error'] = error
    else:
        response_data['is_valid'] = True
    return HttpResponse(
        json.dumps(response_data),
        content_type='application/json')
