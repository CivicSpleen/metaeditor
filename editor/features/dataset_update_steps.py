# -*- coding: utf-8 -*-

from lettuce import step, world

from nose.tools import assert_equals, assert_true

from editor.models import Dataset, Format
from editor.tests.factories import FormatFactory,\
    DataFileFactory, DatasetFactory


@step(u'Given dataset "([^"]*)" exists')
def given_dataset_exists(step, dataset_title):
    DatasetFactory(title=dataset_title)


@step(u'and "([^"]*)" dataset has datafile with "([^"]*)" format')
def and_dataset_has_datafile_with_given_format(step, dataset_title, format_name):
    dataset = Dataset.objects.get(title=dataset_title)
    try:
        file_format = Format.objects.get(name=format_name)
    except Format.DoesNotExist:
        try:
            root = Format.objects.get(parent__isnull=True)
        except Format.DoesNotExist:
            root = FormatFactory()
        file_format = FormatFactory(name=format_name, parent=root)
    DataFileFactory(dataset=dataset, file_format=file_format)


@step(u'When I open "([^"]*)" dataset update page')
def when_i_open_dataset_update_page(step, dataset_title):
    dataset = Dataset.objects.get(title=dataset_title)
    world.browser.get('%s%s' % (world.live_server_url, dataset.get_absolute_url()))


@step(u'(Then|and) I see "([^"]*)" format selected in the dataset formats')
def then_i_see_format_selected_in_the_dataset_formats(step, unused, format_name):
    format = Format.objects.get(name=format_name)
    for checkbox in world.elems('#id_formats input'):
        if checkbox.get_attribute('value') == unicode(format.id):
            assert_equals(checkbox.get_attribute('checked'), 'true')
            return
    raise AssertionError('Checkbox with %s format was not found.' % format_name)


@step(u'and I see dataset formats checkboxes are disabled')
def and_i_see_dataset_formats_checkboxes_are_disabled(step):
    disabled = False
    for checkbox in world.elems('#id_formats input'):
        disabled = True
        assert_equals(checkbox.get_attribute('selected'), 'true')
    assert_true(disabled)
