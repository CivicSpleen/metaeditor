# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.test import TestCase

from editor.models import Category


class IndexViewTest(TestCase):
    def setUp(self):
        self.url = reverse('index')

    def test_renders_menu(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)

        self.assertIn('Dataset List', resp.content)

        self.assertIn('Source Hierarchy Editor', resp.content)
        self.assertIn(reverse('source-list'), resp.content)

        self.assertIn('Formats Hierarchy Editor', resp.content)
        self.assertIn(reverse('format-list'), resp.content)

        self.assertIn('Categories Hierarchy Editor', resp.content)
        self.assertIn(reverse('category-list'), resp.content)


class AddCategoryTest(TestCase):
    def setUp(self):
        self.url = reverse('add-category')

    def test_renders_category_form_on_get(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('name="name"', resp.content)
        self.assertIn('name="parent"', resp.content)

    def test_creates_new_root_category_on_post(self):
        post_params = {
            'name': 'Category1'
        }
        resp = self.client.post(self.url, post_params)
        self.assertEqual(resp.status_code, 302)
        # TODO: check flash message
        self.assertEqual(
            Category.objects.filter(name='Category1', parent__isnull=True).count(),
            1)

    def test_sets_given_category_as_root_of_new_category(self):
        categ1 = Category.objects.create(name='Category1')
        post_params = {
            'name': 'Category2',
            'parent': categ1.id
        }
        resp = self.client.post(self.url, post_params)
        self.assertEqual(resp.status_code, 302)
        # TODO: check flash message
        self.assertEqual(
            Category.objects.filter(name='Category2', parent=categ1).count(),
            1)


class CategoriesTest(TestCase):
    def setUp(self):
        self.url = reverse('category-list')

    def test_renders_categories_on_get(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        # Categories tree will be added using js, so checking for placeholder only.
        self.assertIn('id="tree"', resp.content)


class SourcesTest(TestCase):
    def setUp(self):
        self.url = reverse('source-list')

    def test_renders_categories_on_get(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        # Source tree will be added using js, so checking for placeholder only.
        self.assertIn('id="tree"', resp.content)


class FormatsTest(TestCase):
    def setUp(self):
        self.url = reverse('format-list')

    def test_renders_categories_on_get(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        # Format tree will be added using js, so checking for placeholder only.
        self.assertIn('id="tree"', resp.content)
