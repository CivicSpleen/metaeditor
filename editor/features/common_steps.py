# -*- coding: utf-8 -*-
from time import sleep
from lettuce import step, world

from accounts.tests.helpers import give_perm
from editor.tests.factories import FormatFactory, CategoryFactory
from editor.models import Category, Source, Format, DataFile,\
    DocumentFile, Dataset, Extension


@step(u'(Given|and) I access the "([^"]*)" url')
def given_i_access_the_url(step, unused, url):
    world.browser.get('%s%s' % (world.live_server_url, url))


@step(u'and I click save button')
def and_i_click_save_button(step):
    world.elem('.btn-primary').click()


@step(u'and I see add child link')
def and_i_see_add_child_link(step):
    world.get_a('Add child')


@step(u'(When|and) I click on "([^"]*)" link$')
def when_i_click_on_given_link(step, unused, link_text):
    sleep(0.2)
    elem = world.get_a(link_text)
    elem.click()


@step(u'and I click on "([^"]*)" button')
def and_i_click_on_button_with_given_text(step, button_text):
    btn = world.get_button(button_text)
    btn.click()


@step(u'(Given|and) "([^"]*)" format exists')
def and_given_format_exists(step, unused, format_name):
    FormatFactory(name=format_name)


@step(u'(Given|and) "([^"]*)" format with "([^"]*)" extensions exists')
def and_format_with_given_extensions_exists(step, unused, format_name, extensions):
    try:
        root = Format.objects.get(parent__isnull=True)
    except Format.DoesNotExist:
        root = FormatFactory()
    format = FormatFactory(name=format_name, parent=root)
    Extension.update(format, extensions)


@step(u'and I have permission to (add|change) (.*)$')
def and_i_have_permission_to_create_category(step, action, model_name):
    name_to_model_map = {
        'category': Category,
        'source': Source,
        'format': Format,
        'datafile': DataFile,
        'documentfile': DocumentFile,
        'dataset': Dataset
    }
    user = world.get_current_user()
    assert model_name in name_to_model_map
    model_class = name_to_model_map[model_name]
    codename = '%s_%s' % (action, model_name)
    give_perm(user, model_class, codename)


@step(u'and category node with "([^"]*)" name exists')
def and_category_node_with_group1_name_exists(step, name):
    root = Category.objects.get(parent__isnull=True)
    CategoryFactory(name=name, parent=root)
