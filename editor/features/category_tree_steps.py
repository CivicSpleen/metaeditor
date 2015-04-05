# -*- coding: utf-8 -*-

from lettuce import step, world

from nose.tools import assert_equals

from editor.models import Category
from editor.tests.factories import CategoryFactory


@step(u'Then I see category tree page')
def then_i_see_category_tree_page(step):
    def opened(browser):
        return world.elem('.container.category-tree').is_displayed()
    world.wait(opened, msg='Timeout waiting Category tree display')


@step(u'Then I see category node creation form')
def then_i_see_category_node_creation_form(step):
    world.elem('#id_name')


@step(u'and parent category field is empty')
def and_parent_category_field_is_empty(step):
    parent = world.elem('#id_parent')
    assert_equals(parent.get_attribute('value'), '')


@step(u'When I fill "([^"]*)" to the category name field')
def when_i_fill_given_to_the_category_name_field(step, name):
    world.elem('#id_name').send_keys(name)


@step(u'Then new root category with "([^"]*)" name creates')
def then_new_root_category_with_given_name_creates(step, name):
    qs = Category.objects.filter(name=name)
    assert qs.count() == 1
    assert qs[0].parent is None


@step(u'(Then|and) I see "([^"]*)" category update form')
def and_i_see_category_update_form(step, unused, name):
    world.elem('#id_name').get_attribute('value') == name


@step(u'and I see "([^"]*)" category in the tree')
def and_i_see_given_category_in_the_tree(step, name):
    assert name in world.elem('#tree').text


@step(u'(Given|and) root category node with "([^"]*)" name exists')
def given_root_category_node_with_given_name_exists(step, unused, name):
    CategoryFactory(name=name)


@step(u'When I click on "([^"]*)" category in the tree')
def when_i_click_on_given_category_in_the_tree(step, name):
    elem = world.get_a(name)
    elem.click()


@step(u'and parent category field contains "([^"]*)" category')
def and_parent_category_field_contains_given_category(step, name):
    parent_categ = Category.objects.get(name=name)
    parent_input = world.elem('#id_parent')
    assert int(parent_input.get_attribute('value')) == parent_categ.id


@step(u'Then new category with "([^"]*)" name and "([^"]*)" parent creates')
def then_new_category_creates(step, name, parent_name):
    def created(browser):
        qs = Category.objects.filter(name=name, parent__name=parent_name)
        return qs.count() == 1
    world.wait(created, msg='Timeout waiting Category creation')


@step(u'and I empty parent category field')
def and_i_empty_parent_category_field(step):
    parent_options = world.elems('#id_parent option')
    for option in parent_options:
        if option.get_attribute('value') == '':
            option.click()
            return
    raise Exception('Failed to select empty value in the parent field.')
