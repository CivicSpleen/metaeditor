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
