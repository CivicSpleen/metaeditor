# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.test import TestCase

from editor.models import Category, Dataset

from editor.tests.factories import DatasetFactory, CategoryFactory,\
    SourceFactory, FormatFactory, UserFactory


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

    def test_all_existing_datasets_are_listed(self):
        dataset1 = DatasetFactory()
        dataset2 = DatasetFactory()
        dataset3 = DatasetFactory()
        resp = self.client.get(self.url)
        self.assertEqual(resp.context['object_list'].count(), 3)
        self.assertIn(
            dataset1.title, resp.content)
        self.assertIn(
            dataset2.title, resp.content)
        self.assertIn(
            dataset3.title, resp.content)

    def test_filters_by_title(self):
        ds1 = DatasetFactory(title='abcde 1')
        DatasetFactory(title='abcde 2')
        url = '%s?query=de 1' % self.url
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['object_list'].count(), 1)
        self.assertEqual(resp.context['object_list'][0], ds1)

    def test_filters_by_source_name(self):
        ds1 = DatasetFactory(source__name='abcde 1')
        DatasetFactory(source__name='abcde 2')
        url = '%s?query=de 1' % self.url
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['object_list'].count(), 1)
        self.assertEqual(resp.context['object_list'][0], ds1)

    def test_filters_by_page(self):
        ds1 = DatasetFactory(page='abcde 1')
        DatasetFactory(page='abcde 2')
        url = '%s?query=de 1' % self.url
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['object_list'].count(), 1)
        self.assertEqual(resp.context['object_list'][0], ds1)


class DatasetCreateTest(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        logged_in = self.client.login(
            username=self.user1.username,
            password='1')
        self.assertTrue(logged_in)
        self.source1 = SourceFactory()
        self.url = reverse('dataset-create', kwargs={'source_pk': self.source1.id})

    def test_is_disabled_for_anonymous(self):
        self.client.logout()
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)
        # TODO: Is it really redirect to login page? Test that.

    def test_renders_dataset_form_on_get(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('name="title"', resp.content)
        self.assertIn('name="start_year"', resp.content)

        # source should not be rendered because it can be retrieved from url
        self.assertNotIn('name="source"', resp.content)

        # user should not be rendered to prevent changing
        self.assertNotIn('name="user"', resp.content)

    def test_creates_new_instance_on_post(self):
        categ1 = CategoryFactory()
        post_params = {
            'title': 'Title 1',
            'categories': [categ1.id],
            'variant': 'Variant1',
            'start_year': 1976,
            'end_year': 1976,
            'coverage': Dataset.STATE,
            'region': Dataset.STATE,
            'page': 'http://ya.ru',
            'download_page': 'http://ya.ru',
            'contacts': 'contact@gmail.com',
            'formats': [FormatFactory().id],
            'entry_time_minutes': 15}

        resp = self.client.post(self.url, post_params)
        if resp.status_code == 200:
            # Form error
            raise AssertionError('Submitted form is invalid: %s' % resp.context['form'].errors)
        self.assertEqual(resp.status_code, 302)
        qs = Dataset.objects.filter(title=post_params['title'])
        self.assertEqual(qs.count(), 1)


class DatasetUpdateTest(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        logged_in = self.client.login(
            username=self.user1.username,
            password='1')
        self.assertTrue(logged_in)
        self.ds1 = DatasetFactory()
        self.url = reverse('dataset-update', kwargs={'pk': self.ds1.id})

    def test_is_disabled_for_anonymous(self):
        self.client.logout()
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)
        # TODO: Is it really redirect to login page? Test that.

    def test_renders_dataset_form_on_get(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('name="title"', resp.content)
        self.assertIn('name="start_year"', resp.content)

        # source should not be rendered because it can be retrieved from url
        self.assertNotIn('name="source"', resp.content)

        # user should not be rendered to prevent changing
        self.assertNotIn('name="user"', resp.content)

    def test_updates_instance_on_change(self):
        post_params = {
            'title': '%s updated' % self.ds1.title,
            'categories': [CategoryFactory().id],
            'variant': '%s updated' % self.ds1.variant,
            'start_year': 1976,
            'end_year': 1976,
            'coverage': Dataset.STATE,
            'region': Dataset.STATE,
            'page': 'http://ya.ru',
            'download_page': 'http://ya.ru',
            'contacts': 'contact@gmail.com',
            'formats': [FormatFactory().id],
            'entry_time_minutes': 15}

        resp = self.client.post(self.url, post_params)
        if resp.status_code == 200:
            # Form error
            raise AssertionError('Submitted form is invalid: %s' % resp.context['form'].errors)
        self.assertEqual(resp.status_code, 302)
        qs = Dataset.objects.filter(title=post_params['title'])
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0].title, '%s updated' % self.ds1.title)
