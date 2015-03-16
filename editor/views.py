# -*- coding: utf-8 -*-
import json

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from editor.forms import DatasetForm, DataFileFormset, DocumentFileFormset
from editor.models import Category, Source, Format, Dataset,\
    DataFile, DocumentFile


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
    # TODO: add messages
    template_name = 'editor/tree.html'

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden('Forbidden for anonymous users.')
        return super(BaseCreateView, self).post(request, *args, **kwargs)

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
    # TODO: add messages
    template_name = 'editor/tree.html'

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden('Forbidden for anonymous users.')
        return super(BaseUpdateView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
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
            'dataset-create', kwargs={'source_pk': self.object.pk})
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


class DatasetCreate(CreateView):
    # TODO: that view should handle upload too.
    model = Dataset
    form_class = DatasetForm

    def dispatch(self, request, *args, **kwargs):
        self.source = get_object_or_404(Source, pk=self.kwargs['source_pk'])
        return super(DatasetCreate, self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        form_kwargs = self.get_form_kwargs()
        form_kwargs['source'] = self.source
        return form_class(self.request.user, **form_kwargs)


class DatasetUpdate(UpdateView):
    model = Dataset
    form_class = DatasetForm

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        datafile_formset = DataFileFormset(prefix='datafile', instance=self.object)
        docfile_formset = DocumentFileFormset(prefix='documentfile', instance=self.object)
        if 'save-and-continue' in self.request.POST:
            return self.object.get_absolute_url()
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
        self.object = self.get_object()
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
        messages.add_message(self.request, messages.SUCCESS, 'Dataset saved.')
        if 'save-and-continue' in self.request.POST:
            return self.object.get_absolute_url()
        return reverse('dataset-list')

    def form_valid(self, form, datafile_formset, docfile_formset):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """
        self.object = form.save()
        datafile_formset.save()
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

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        return form_class(self.request.user, **self.get_form_kwargs())


# FIXME: remove csrf_exempt and learn client side to send cookie
@csrf_exempt
@login_required
def upload(request):
    if 'docfile' in request.GET:
        model_class = DocumentFile
    else:
        model_class = DataFile
    df = model_class()
    df.save()
    df.f.save(request.FILES['file'].name, request.FILES['file'])
    response_data = {}
    response_data['file'] = {
        'id': df.id,
        'url': df.f.url,
        'name': df.f.name
    }
    return HttpResponse(
        json.dumps(response_data),
        content_type='application/json')
