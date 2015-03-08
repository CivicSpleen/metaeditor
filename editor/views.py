import json

from django.shortcuts import render, render_to_response, redirect
from django.views.generic import View
from django.template import RequestContext

from editor.models import Category, Source, Format
from editor import forms


def get_nodes(node):
    """ Generates tree of the given node as root.

    Args:
        node: root of the tree

    Returns:
        tree
        # TODO: give an example
    """
    d = {}
    d['text'] = node.name
    children = node.get_children()
    if children is not None and len(children) > 0:
        d['nodes'] = [get_nodes(child) for child in children]
    return d


def get_root_or_none(model_class):
    """ Returns root node of the given class or None if there is no such.

    Args:
        model_class:

    Returns:
        root node as the instance of the given model_class
    """
    roots = list(model_class.objects.filter(level=0))
    if roots:
        root = roots[0]
        # TODO: Why first only?
    else:
        root = None
    return root


class IndexView(View):
    template_name = 'editor/index.html'

    def get(self, request):
        return render(request, self.template_name)


def categories(request):
    template = 'editor/categories.html'
    root = get_root_or_none(Category)
    if root:
        data = get_nodes(root)
    else:
        data = []

    return render_to_response(template, {'data': json.dumps(data)}, context_instance=RequestContext(request))


def add_category(request):
    template = 'editor/add_category.html'
    if request.method == 'POST':
        form = forms.CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category-list')
    else:
        form = forms.CategoryForm()
    return render_to_response(template, {'form': form}, context_instance=RequestContext(request))


def sources(request):
    template = 'editor/sources.html'
    root = get_root_or_none(Source)
    if root:
        data = get_nodes(root)
    else:
        data = []

    return render_to_response(template, {'data': json.dumps(data)}, context_instance=RequestContext(request))


def formats(request):
    template = 'editor/formats.html'
    root = get_root_or_none(Format)
    if root:
        data = get_nodes(root)
    else:
        data = []

    return render_to_response(template, {'data': json.dumps(data)}, context_instance=RequestContext(request))
