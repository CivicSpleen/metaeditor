# -*- coding: utf-8 -*-

from lettuce import step, world

from editor.models import Dataset
from editor.tests.factories import DatasetFactory


def _get_menu_elem(text):
    for e in world.elems('.masthead nav ul li'):
        if e.text == text:
            return e
    raise Exception('Menu element with %s text was not found' % text)


@step(u'and I click on "([^"]*)" menu option')
def and_i_click_on_group1_menu_option(step, elem_text):
    elem = _get_menu_elem(elem_text)
    elem.click()


@step(u'Then I see dataset list page')
def then_i_see_dataset_list_page(step):
    def is_list(browser):
        return 'Dataset List' in world.browser.title
    world.wait(is_list, msg='Timeout waiting Dataset list loading.')


@step(u'and I see table with all three datasets')
def and_i_see_table_with_all_datasets(step):
    table = world.elem('table')
    qs = Dataset.objects.all()
    assert qs.count()
    for ds in qs:
        assert ds.title in table.text


@step(u'and "([^"]*)" menu option is active')
def and_given_menu_option_is_active(step, elem_text):
    elem = _get_menu_elem(elem_text)
    assert 'active' in elem.get_attribute('class')


@step(u'Given ([^"]*) datasets exists')
def given_datasets_exists(step, amount):
    for i in range(int(amount)):
        DatasetFactory()


@step(u'Given dataset with "([^"]*)" title exists')
def given_dataset_with_given_title_exists(step, title):
    DatasetFactory(title=title)


@step(u'When I click dataset with "([^"]*)" title')
def when_i_click_dataset_with_given_title(step, title):
    for a in world.elems('table a'):
        if a.text == title:
            a.click()
            return
    raise AssertionError('link with %s title was not found in the dataset table.')


@step(u'Then I see "([^"]*)" dataset edit page')
def then_i_see_dataset_edit_page(step, title):
    assert 'Dataset Edit' in world.browser.title
    assert world.elem('#id_title').get_attribute('value') == title
