# -*- coding: utf-8 -*-
import json
import logging

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404

from django.views.decorators.http import require_POST
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from editor.forms import DatasetForm, DataFileFormset, DocumentFileFormset, ScrapeForm
from editor.models import Category, Source, Format, Dataset
from editor.utils import get_links

logger = logging.getLogger(__name__)


class IndexView(View):
    template_name = 'editor/index.html'

    def get(self, request):
        return render(request, self.template_name)


class BaseTreeView(ListView):
    template_name = 'editor/tree.html'

    def get_context_data(self, **kwargs):
        kwargs['nodes'] = self.model.objects.all()
        kwargs['create_url'] = self.model.get_create_url()
        return kwargs


class BaseCreateView(CreateView):
    template_name = 'editor/tree.html'

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden('Forbidden for anonymous users.')
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
        kwargs['nodes'] = self.model.objects.all()
        kwargs['create_url'] = self.model.get_create_url()
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
        kwargs['nodes'] = self.model.objects.all()
        kwargs['create_url'] = self.model.get_create_url()
        kwargs['selected_node'] = self.object
        return kwargs


class CategoryList(BaseTreeView):
    model = Category


class CategoryCreate(BaseCreateView):
    model = Category
    fields = ['name', 'parent']


class CategoryUpdate(BaseUpdateView):
    model = Category
    fields = ['name', 'parent']


class SourceList(BaseTreeView):
    model = Source


class SourceCreate(BaseCreateView):
    model = Source
    fields = ['name', 'parent', 'abbreviation', 'domain', 'homepage', 'about', 'categories']


class SourceUpdate(BaseUpdateView):
    model = Source
    fields = ['name', 'parent', 'abbreviation', 'domain', 'homepage', 'about', 'categories']

    def get_context_data(self, **kwargs):
        ctx = super(SourceUpdate, self).get_context_data(**kwargs)
        ctx['create_dataset_url'] = reverse(
            'editor:dataset-create',
            kwargs={'source_pk': self.object.pk})
        return ctx


class FormatList(BaseTreeView):
    model = Format


class FormatCreate(BaseCreateView):
    model = Format
    fields = ['name', 'parent']


class FormatUpdate(BaseUpdateView):
    model = Format
    fields = ['name', 'parent']


class DatasetList(ListView):
    model = Dataset

    def get_queryset(self, *args, **kwargs):
        qs = super(DatasetList, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get('query')
        if query:
            qs = qs.filter(
                Q(title__icontains=query)
                | Q(source__name__icontains=query)
                | Q(page__icontains=query))

        order_by = self.request.GET.get('o')
        if order_by not in ('title', 'source__name', 'page'):
            order_by = None
        if order_by:
            qs = qs.order_by(order_by)
        return qs.select_related('source')


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
        datafile_formset = DataFileFormset(prefix='datafile', instance=self.object)
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
        if 'save-and-continue' in self.request.POST:
            return self.object.get_absolute_url()
        return reverse('editor:dataset-list')

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


class DatasetUpdate(DatasetEditMixin, UpdateView):
    model = Dataset
    form_class = DatasetForm

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


@require_POST
@login_required
def scrape(request):
    response_data = {}
    form = ScrapeForm(request.POST)
    if form.is_valid():
        try:
            response_data['links'] = get_links(form.cleaned_data['url'])
        except Exception as exc:
            response_data['errors'] = [u'Failed to get urls. Please, try later.']
            logger.error(
                u'Failed to retrieve links from %s because of %s' % (form.cleaned_data['url'], exc))
    else:
        errors = []
        for field, field_errors in form.errors.iteritems():
            errors.append('%s' % '; '.join(field_errors))
        response_data['errors'] = errors

    return HttpResponse(
        json.dumps(response_data),
        content_type='application/json')
