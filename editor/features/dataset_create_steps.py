# -*- coding: utf-8 -*-
import subprocess

from lettuce import step, world, after

from nose.tools import assert_equals, assert_true, assert_in

import fudge

from editor.models import Dataset
from editor.tests.factories import SourceFactory
from editor import views


@after.each_scenario
def kill_pydoc(scenario):
    if hasattr(world, '__pydoc_process'):
        world.__pydoc_process.kill()


def _get_formset_block(name):
    if name == 'Data files':
        fieldset_index = 0
    elif name == 'Documents':
        fieldset_index = 1
    else:
        raise Exception('Do not now the location of the %s fieldset' % name)
    fieldset = world.elems('fieldset')[fieldset_index]
    assert_equals(
        fieldset.find_element_by_css_selector('legend').text,
        name)
    return fieldset


@step(u'(Given|and) source edit page is opened')
def and_source_edit_page_is_opened(step, unused):
    source = SourceFactory()
    world.browser.get('%s%s' % (world.live_server_url, source.get_absolute_url()))


@step(u'(Then|and) I see dataset edit form')
def then_i_see_dataset_edit_form(step, unused):
    assert_true(world.elem('#id_title').is_displayed())


@step(u'and I see Data files and Documents blocks')
def and_i_see_data_files_and_documents_blocks(step):
    legends = [x.text for x in world.elems('fieldset legend')]
    assert_equals(len(legends), 2)
    assert_in('Data files', legends)
    assert_in('Documents', legends)


@step(u'and I see "([^"]*)" button in the "([^"]*)" block')
def and_i_see_button_with_given_text_in_the_given_block(step, button_text, fieldset_legend):
    formset = _get_formset_block(fieldset_legend)
    buttons = [x.text for x in formset.find_elements_by_css_selector('button')]
    assert_in(button_text, buttons)


@step(u'(Given|and) dataset create form is opened')
def and_dataset_create_form_is_opened(step, unused):
    source = SourceFactory()
    world.browser.get(
        '%s%s' % (world.live_server_url, source.get_dataset_create_url()))


@step(u'When I populate dataset form title with "([^"]*)"')
def when_i_populate_dataset_form_title_with_given(step, title):
    world.elem('#id_title').send_keys(title)


@step(u'and I populate other fields of the dataset form with random values')
def and_i_populate_other_fields_of_the_dataset_form_with_random_values(step):
    # populate required minimum
    def set_value(field_id, keys):
        """ clears field and populate field with given keys """
        field = world.elem(field_id)
        field.clear()
        field.send_keys(keys)

    set_value('#id_variant', 'Variant1')
    set_value('#id_start_year', 1976)
    set_value('#id_end_year', 1976)
    world.elems('#id_coverage option')[1].click()
    world.elems('#id_region option')[1].click()
    set_value('#id_page', 'http://ya.ru')
    set_value('#id_download_page', 'http://ya.ru')
    set_value('#id_contacts', 'Contacts')
    set_value('#id_entry_time_minutes', '15')


@step(u'Then new dataset with "([^"]*)" creates')
def then_new_dataset_with_given_title_creates(step, title):
    def created(browser):
        return Dataset.objects.filter(title=title).count() == 1
    world.wait(created, msg='Timeout waiting Dataset creation')


@step(u'(Then|and) I see dataset edit form')
def and_i_see_dataset_edit_form(step, unused):
    world.elem('#id_title').is_displayed()


@step(u'and I populate "([^"]*)" first form with "([^"]*)", "([^"]*)" and "([^"]*)"')
def and_i_populate_formset_first_form(step, formset_name, name, format, url):
    formset = _get_formset_block(formset_name)
    formset.find_element_by_css_selector('.formset .name').send_keys(name)
    formset.find_elements_by_css_selector('.formset select option')[1].click()
    formset.find_element_by_css_selector('.formset .url').send_keys(url)


@step(u'and "([^"]*)" dataset contains "([^"]*)" data file')
def and_dataset_contains_tiven_data_file_name(step, title, datafile_name):
    dataset = Dataset.objects.get(title=title)
    assert_in(datafile_name, [x.name for x in dataset.datafile_set.all()])


@step(u'and "([^"]*)" dataset contains "([^"]*)" document file')
def and_dataset_contains_given_document_file_name(step, title, doc_filename):
    dataset = Dataset.objects.get(title=title)
    assert_in(doc_filename, [x.name for x in dataset.documentfile_set.all()])


@step(u'and dataset form contains "([^"]*)" data file')
def and_dataset_form_contains_given_data_file(step, datafile_name):
    formset = _get_formset_block('Data files')
    name_elems = formset.find_elements_by_css_selector('.formset .name')
    form_names = [x.get_attribute('value') for x in name_elems]
    assert_in(datafile_name, form_names)


@step(u'and dataset form contains "([^"]*)" document file')
def and_dataset_form_contains_given_document_file(step, doc_name):
    formset = _get_formset_block('Documents')
    form_name = formset\
        .find_element_by_css_selector('.formset .name')\
        .get_attribute('value')
    assert_equals(form_name, doc_name)


@step(u'(When|and) I check input next to the "([^"]*)" url')
def when_i_check_input_next_to_the_given_url(step, unused, url_text):
    for tr in world.elems('table.links tbody.content tr'):
        if tr.find_element_by_css_selector('a').text == url_text:
            tr.find_element_by_css_selector('input').click()
            return
    raise Exception('Table row with link with %s text was not found' % url_text)


@step(u'When I click on "([^"]*)" button inside "([^"]*)" block')
def when_i_click_on_given_button_inside_given_block(step, button_text, fieldset_legend):
    formset = _get_formset_block(fieldset_legend)
    for btn in formset.find_elements_by_css_selector('button'):
        if btn.text == button_text:
            btn.click()
            return
    raise Exception('Button with %s text was not found inside %s block' % (button_text, fieldset_legend))


@step(u'and pydoc http server is running on "([^"]*)"')
def and_pydoc_http_server_is_running(step, group1):
    cmd = 'pydoc -p 1234'
    world.__pydoc_process = subprocess.Popen(
        'exec %s' % cmd, stdout=subprocess.PIPE, shell=True)


@step(u'and I populate download page with "([^"]*)" url')
def and_i_populate_download_page_with_group1_page(step, pydoc_url):
    world.elem('#id_download_page').clear()
    world.elem('#id_download_page').send_keys(pydoc_url)


@step(u'Then I see popup with urls scrapped from pydoc http server')
def then_i_see_popup_with_urls_scrapped_from_pydoc_http_server(step):
    popup = world.elem('#remoteLinksModal')
    assert_true(popup.is_displayed())

    def contains_builtin(browser):
        popup = world.elem('#remoteLinksModal')
        return '__builtin__' in popup.text

    world.wait(contains_builtin, msg='Timeout while waiting __builtin__')

    def contains_future(browser):
        popup = world.elem('#remoteLinksModal')
        return '__future__' in popup.text

    world.wait(contains_future, msg='Timeout while waiting __future__')


@step(u'Then I see "([^"]*)" urls added to "([^"]*)" formset')
def then_i_see_urls_added_to_given_formset(step, urls, fieldset_legend):
    urls = urls.split(',')
    formset = _get_formset_block(fieldset_legend)
    rendered_urls = [
        x.get_attribute('value') for x in formset.find_elements_by_css_selector('.formset .name')]
    for url in urls:
        assert_in(url.strip(), rendered_urls)


@step(u'When I select "([^"]*)" file format in both urls')
def when_i_select_given_file_format_in_both_urls(step, fieldset_legend):
    formset = _get_formset_block('Data files')
    for i, select in enumerate(formset.find_elements_by_css_selector('.formset select')):
        select.find_elements_by_css_selector('option')[1].click()
        if i == 1:
            # do not change last empty form
            return


@step(u'and datafiles filtering drops everything except urls containing "([^"]*)"')
def and_datafiles_filtering_drops_everything_except_urls_containing_given_part(step, part):

    def fake_filter(links, include_extensions):
        ret = [x for x in links if part in x['href']]
        return ret

    fudge.patch_object(views, 'filter_links', fake_filter)
