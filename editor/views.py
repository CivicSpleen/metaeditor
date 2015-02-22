from django.shortcuts import render, render_to_response
from django.views.generic import View
from django.template import RequestContext
import json

from editor.models import Category, Source, Format

class IndexView(View):
    template_name = 'editor/index.html'

    def get(self, request):
        return render(request, self.template_name)


def get_nodes(node):
    d = {}
    d['text'] = node.name
    children = node.get_children()
    if children is not None and len(children)>0:
        d['nodes'] = [get_nodes(child) for child in children]
    return d

def categories(request):
    root = Category.objects.filter(level=0)[0]
    data = get_nodes(root)

    return render_to_response("editor/categories.html", {'data': json.dumps(data)}, context_instance=RequestContext(request))

def sources(request):
    root = Source.objects.filter(level=0)[0]
    data = get_nodes(root)

    return render_to_response("editor/sources.html", {'data': json.dumps(data)}, context_instance=RequestContext(request))

def formats(request):
    root = Format.objects.filter(level=0)[0]
    data = get_nodes(root)

    return render_to_response("editor/formats.html", {'data': json.dumps(data)}, context_instance=RequestContext(request))
