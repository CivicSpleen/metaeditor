# -*- coding: utf-8 -*-

from django.db.models import Q

from django.shortcuts import render

from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from editor.models import Category, Source, Format, Dataset


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

    def get_context_data(self, **kwargs):
        kwargs['nodes'] = self.model.objects.all()
        kwargs['create_url'] = self.model.get_create_url()
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

    def get_context_data(self, **kwargs):
        kwargs['nodes'] = self.model.objects.all()
        kwargs['create_url'] = self.model.get_create_url()
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

        return qs.select_related('source')
