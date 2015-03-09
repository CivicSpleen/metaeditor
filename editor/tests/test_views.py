# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.test import TestCase

from editor.models import Category

from editor.tests.factories import DatasetFactory, CategoryFactory, SourceFactory, FormatFactory


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


class CategoryCreateTest(TestCase):
    def setUp(self):
        self.url = reverse('category-create')

    def test_renders_category_form_on_get(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('name="name"', resp.content)
        self.assertIn('name="parent"', resp.content)

    def test_renders_full_tree_on_get(self):
        categ1 = CategoryFactory()
        categ2 = CategoryFactory()
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(categ1.name, resp.content)
        self.assertIn(categ2.name, resp.content)

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
        categ1 = CategoryFactory()
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


class CategoryListTest(TestCase):
    def setUp(self):
        self.url = reverse('category-list')

    def test_renders_category_tree_on_get(self):
        categ1 = CategoryFactory()
        categ2 = CategoryFactory()
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(categ1.name, resp.content)
        self.assertIn(categ2.name, resp.content)


class SourceListTest(TestCase):
    def setUp(self):
        self.url = reverse('source-list')

    def test_renders_category_tree_on_get(self):
        source1 = SourceFactory()
        source2 = SourceFactory()
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(source1.name, resp.content)
        self.assertIn(source2.name, resp.content)


class FormatListTest(TestCase):
    def setUp(self):
        self.url = reverse('format-list')

    def test_renders_format_tree_on_get(self):
        format1 = FormatFactory()
        format2 = FormatFactory()
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(format1.name, resp.content)
        self.assertIn(format2.name, resp.content)


class DatasetListTest(TestCase):

    def setUp(self):
        self.url = reverse('dataset-list')

    def test_renders_existing_datasets(self):
        dataset1 = DatasetFactory()
        dataset2 = DatasetFactory()
        dataset3 = DatasetFactory()
        resp = self.client.get(self.url)
        self.assertIn(
            dataset1.title, resp.content)
        self.assertIn(
            dataset2.title, resp.content)
        self.assertIn(
            dataset3.title, resp.content)
