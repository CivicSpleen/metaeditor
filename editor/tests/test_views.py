# -*- coding: utf-8 -*-
import json

import fudge

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
        self.assertIn(reverse('editor:source-list'), resp.content)

        self.assertIn('Formats Hierarchy Editor', resp.content)
        self.assertIn(reverse('editor:format-list'), resp.content)

        self.assertIn('Categories Hierarchy Editor', resp.content)
        self.assertIn(reverse('editor:category-list'), resp.content)


class CategoryCreateTest(TestCase):
    def setUp(self):
        self.url = reverse('editor:category-create')

        self.user1 = UserFactory()
        logged_in = self.client.login(
            username=self.user1.username,
            password='1')
        self.assertTrue(logged_in)

    def test_post_is_forbidden_for_anonymous(self):
        self.client.logout()
        resp = self.client.post(self.url, {})
        self.assertEqual(resp.status_code, 403)

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
        self.url = reverse('editor:category-list')

    def test_renders_category_tree_on_get(self):
        categ1 = CategoryFactory()
        categ2 = CategoryFactory()
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(categ1.name, resp.content)
        self.assertIn(categ2.name, resp.content)


class SourceListTest(TestCase):
    def setUp(self):
        self.url = reverse('editor:source-list')

    def test_renders_category_tree_on_get(self):
        source1 = SourceFactory()
        source2 = SourceFactory()
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(source1.name, resp.content)
        self.assertIn(source2.name, resp.content)


class FormatListTest(TestCase):
    def setUp(self):
        self.url = reverse('editor:format-list')

    def test_renders_format_tree_on_get(self):
        format1 = FormatFactory()
        format2 = FormatFactory()
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(format1.name, resp.content)
        self.assertIn(format2.name, resp.content)


class DatasetListTest(TestCase):

    def setUp(self):
        self.url = reverse('editor:dataset-list')

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
        # TODO: refactor all filters.
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

    def test_sorts_by_title(self):
        # TODO: refactor all sorts
        ds1 = DatasetFactory(title='abcde 1')
        ds2 = DatasetFactory(title='abcde 2')
        url = '%s?o=title' % self.url
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['object_list'][0], ds1)
        self.assertEqual(resp.context['object_list'][1], ds2)

    def test_sorts_by_source_title(self):
        ds1 = DatasetFactory(source__name='abcde 3')
        ds2 = DatasetFactory(source__name='abcde 2')
        url = '%s?o=source__name' % self.url
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['object_list'][0], ds2)
        self.assertEqual(resp.context['object_list'][1], ds1)

    def test_sorts_by_page(self):
        ds1 = DatasetFactory(page='abcde 3')
        ds2 = DatasetFactory(page='abcde 2')
        url = '%s?o=page' % self.url
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['object_list'][0], ds2)
        self.assertEqual(resp.context['object_list'][1], ds1)


class DatasetCreateTest(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        logged_in = self.client.login(
            username=self.user1.username,
            password='1')
        self.assertTrue(logged_in)
        self.source1 = SourceFactory()
        self.url = reverse('editor:dataset-create', kwargs={'source_pk': self.source1.id})

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
            'entry_time_minutes': 15,
            'datafile-MAX_NUM_FORMS': 1000,
            'datafile-TOTAL_FORMS': 0,
            'datafile-INITIAL_FORMS': 1,
            'documentfile-MAX_NUM_FORMS': 1000,
            'documentfile-TOTAL_FORMS': 0,
            'documentfile-INITIAL_FORMS': 1,
        }

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
        self.url = reverse('editor:dataset-update', kwargs={'pk': self.ds1.id})

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
            'entry_time_minutes': 15,
            'datafile-MAX_NUM_FORMS': 1000,
            'datafile-TOTAL_FORMS': 0,
            'datafile-INITIAL_FORMS': 1,
            'documentfile-MAX_NUM_FORMS': 1000,
            'documentfile-TOTAL_FORMS': 0,
            'documentfile-INITIAL_FORMS': 1,
        }

        resp = self.client.post(self.url, post_params)
        if resp.status_code == 200:
            # Form error
            raise AssertionError('Submitted form is invalid: %s' % resp.context['form'].errors)
        self.assertEqual(resp.status_code, 302)
        qs = Dataset.objects.filter(title=post_params['title'])
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0].title, '%s updated' % self.ds1.title)


class ScrapeTest(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        logged_in = self.client.login(
            username=self.user1.username,
            password='1')
        self.assertTrue(logged_in)
        self.url = reverse('editor:scrape')

    def test_is_disabled_for_anonymous(self):
        self.client.logout()
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)
        # TODO: Is it really redirect to login page? Test that.

    @fudge.patch('editor.views.get_links')
    def test_returns_all_links_from_given_url(self, fake_get):
        fake_get.expects_call()\
            .returns([{'text': 'Yandex', 'url': 'http://yandex.ru'}])

        post_data = {'url': 'http://yandex.ru'}
        resp = self.client.post(
            self.url, post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertIn('links', content)
        self.assertIn('text', content['links'][0])
        self.assertIn('url', content['links'][0])
        self.assertEquals(content['links'][0]['url'], 'http://yandex.ru')
        self.assertEquals(content['links'][0]['text'], 'Yandex')

    def test_returns_error_if_wrong_url_given(self):
        post_data = {'url': 'ru'}
        resp = self.client.post(
            self.url, post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertIn('errors', content)
        self.assertIn('Enter a valid URL', content['errors'][0])
        self.assertNotIn('links', content)

    @fudge.patch(
        'editor.views.get_links',
        'editor.views.logger.error')
    def test_get_links_error_goes_to_log(self, fake_get, fake_error):
        fake_get.expects_call()\
            .raises(Exception('My fake exception'))
        fake_error.expects_call()
        post_data = {'url': 'http://yandex.ru/'}
        resp = self.client.post(
            self.url, post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertIn('errors', content)
        self.assertIn('Failed to get urls', content['errors'][0])
        self.assertNotIn('links', content)
