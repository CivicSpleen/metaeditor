# -*- coding: utf-8 -*-
import json

import fudge

from django.core.urlresolvers import reverse
from django.test import TestCase

from accounts.tests.helpers import give_perm

from editor.models import Category, Dataset, DataFile, DocumentFile,\
    Source, Format, Extension

from editor.tests.factories import DatasetFactory, CategoryFactory,\
    SourceFactory, FormatFactory, UserFactory, ExtensionFactory


class BaseTest(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        logged_in = self.client.login(
            username=self.user1.username,
            password='1')
        self.assertTrue(logged_in)
        self.url = self.get_url()
        self.model_class = self.get_model_class()
        self.model_factory_class = self.get_model_factory_class()
        give_perm(
            self.user1, self.model_class,
            'add_%s' % self.model_class._meta.model_name)
        give_perm(
            self.user1, self.model_class,
            'change_%s' % self.model_class._meta.model_name)

    def get_url(self):
        raise NotImplementedError

    def get_model_class(self):
        raise NotImplementedError

    def get_model_factory_class(self):
        raise NotImplementedError


class BaseCreateTest(BaseTest):
    def setUp(self):
        super(BaseCreateTest, self).setUp()
        self.create_params = self.get_create_params()

    def get_create_params(self):
        raise NotImplementedError


class BaseUpdateTest(BaseTest):
    def setUp(self):
        super(BaseUpdateTest, self).setUp()
        self.update_params = self.get_update_params()

    def get_update_params(self):
        raise NotImplementedError


class CreatePermissionTestMixin(object):
    """ Group of the tests of the permission of the creating model. """

    def test_post_is_not_available_for_anonymous(self):
        self.client.logout()
        resp = self.client.post(self.url, {})
        self.assertEqual(resp.status_code, 302)

    def test_post_is_not_available_without_permission(self):
        self.user1.user_permissions.all().delete()
        resp = self.client.post(self.url, {})
        self.assertEqual(resp.status_code, 403)


class ListPermissionTestMixin(object):
    """ Group of the tests of the permissions of the listing. """

    def test_does_not_show_create_root_node_for_user_without_permission(self):
        self.user1.user_permissions.all().delete()
        resp = self.client.get(self.url)
        self.assertNotIn(
            reverse('editor:category-create'),
            resp.content,
            'Category create url unexpectedly found.')


class UpdatePermissionTestMixin(CreatePermissionTestMixin):
    """ Group of the tests of the permissions of the updating. """
    pass


class NodeCreateTestMixin(object):
    """ Group of the tests related to node creation. Expects `model_class` and `model_factory_class`
        properties from base class. """

    def test_renders_node_form_on_get(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('name="name"', resp.content)
        self.assertIn('name="parent"', resp.content)

    def test_renders_full_tree_on_get(self):
        root = self.model_factory_class()
        node1 = self.model_factory_class(parent=root)
        node2 = self.model_factory_class(parent=root)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(node1.name, resp.content)
        self.assertIn(node2.name, resp.content)

    def test_does_not_render_root_node(self):
        root = self.model_factory_class(parent=None, name='root-categ123')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn(root.name, resp.content, 'Root node unexpectedly found.')

    def test_assigns_global_root_if_parent_was_not_given(self):
        root = self.model_factory_class(parent=None, name='root-categ123')
        post_params = self.create_params
        post_params['parent'] = ''

        resp = self.client.post(self.url, post_params)
        self.assertEqual(resp.status_code, 302)
        qs = self.model_class.objects.filter(name=post_params['name'])
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0].parent, root)

    def test_sets_given_node_as_parent_of_new_node(self):
        root = self.model_factory_class(parent=None)
        node1 = self.model_factory_class(parent=root)
        post_params = self.create_params
        post_params['parent'] = node1.id
        resp = self.client.post(self.url, post_params)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
            self.model_class.objects.filter(name='Node 2', parent=node1).count(),
            1)


class NodeListTestMixin(object):
    """ Group of tests of tree views. Expecting model_class and model_factory_class
        properties. """

    def test_renders_tree_on_get_by_anonymous(self):
        self.client.logout()
        root = self.model_factory_class(parent=None)
        node1 = self.model_factory_class(parent=root)
        node2 = self.model_factory_class(parent=root)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(
            node1.name, resp.content,
            '%s node was not found in the response' % node1.name)
        self.assertIn(
            node2.name, resp.content,
            '%s node was not found in the response' % node2.name)

    def test_renders_tree_on_get_by_authenticated(self):
        root = self.model_factory_class(parent=None)
        node1 = self.model_factory_class(parent=root)
        node2 = self.model_factory_class(parent=root)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(
            node1.name, resp.content,
            '%s node was not found in the response' % node1.name)
        self.assertIn(
            node2.name, resp.content,
            '%s node was not found in the response' % node2.name)


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


class CategoryNodeCreateTest(BaseCreateTest, CreatePermissionTestMixin, NodeCreateTestMixin):

    def get_url(self):
        return reverse('editor:category-create')

    def get_model_class(self):
        return Category

    def get_model_factory_class(self):
        return CategoryFactory

    def get_create_params(self):
        params = {
            'name': 'Node 2',
            'parent': None
        }
        return params


class CategoryListTest(BaseTest, NodeListTestMixin, ListPermissionTestMixin):

    def get_url(self):
        return reverse('editor:category-list')

    def get_model_class(self):
        return Category

    def get_model_factory_class(self):
        return CategoryFactory


class SourceNodeCreateTest(BaseCreateTest, CreatePermissionTestMixin, NodeCreateTestMixin):

    def get_url(self):
        return reverse('editor:source-create')

    def get_model_class(self):
        return Source

    def get_model_factory_class(self):
        return SourceFactory

    def get_create_params(self):
        params = {
            'name': 'Node 2',
            'homepage': 'http://ya.ru'
        }
        return params

    def test_saves_user_who_created_source(self):
        post_params = self.create_params
        resp = self.client.post(self.url, post_params)
        self.assertEqual(resp.status_code, 302)
        qs = Source.objects.filter(name=post_params['name'])
        self.assertEquals(qs.count(), 1)
        self.assertEquals(qs[0].created_by, self.user1)


class SourceNodeUpdateTest(BaseUpdateTest):
    # TODO: test other nodes too.
    def get_url(self):
        self.root = SourceFactory()
        self.source = SourceFactory(parent=self.root)
        return self.source.get_absolute_url()

    def get_model_class(self):
        return Source

    def get_model_factory_class(self):
        return SourceFactory

    def get_update_params(self):
        params = {
            'name': 'Node 2',
            'homepage': 'http://ya.ru'
        }
        return params

    def test_saves_user_who_updated_source(self):
        assert self.source.updated_by is None
        resp = self.client.post(self.url, self.update_params)
        self.assertEqual(resp.status_code, 302)

        # get updated instance from db
        source = Source.objects.get(id=self.source.id)
        self.assertEquals(source.updated_by, self.user1)

    def test_shows_user_who_created_source(self):
        self.source.created_by = self.user1
        self.source.save()

        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(
            'Created by: %s' % self.user1.get_full_name(),
            resp.content,
            'User who updated source was not found in the content')

    def test_shows_user_who_updated_source(self):
        self.source.updated_by = self.user1
        self.source.save()

        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(
            'Updated by: %s' % self.source.updated_by.get_full_name(),
            resp.content,
            'User who updated source was not found in the content')


class SourceListTest(BaseTest, NodeListTestMixin, ListPermissionTestMixin):
    def get_url(self):
        return reverse('editor:source-list')

    def get_model_class(self):
        return Source

    def get_model_factory_class(self):
        return SourceFactory

    def test_renders_abbreviation_with_name(self):
        root = SourceFactory()
        source1 = SourceFactory(parent=root, abbreviation='HHS')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(
            '%s (%s)' % (source1.name, source1.abbreviation), resp.content,
            '%s node abbreviation was not found in the response' % source1.name)


class FormatNodeCreateTest(BaseCreateTest, CreatePermissionTestMixin, NodeCreateTestMixin):

    def get_url(self):
        return reverse('editor:format-create')

    def get_model_class(self):
        return Format

    def get_model_factory_class(self):
        return FormatFactory

    def get_create_params(self):
        params = {
            'name': 'Node 2'
        }
        return params

    def test_renders_extensions_field(self):
        resp = self.client.get(self.url)
        self.assertIn('id_extensions', resp.content)

    def test_creates_extensions(self):
        # create root
        FormatFactory(parent=None)

        params = self.create_params
        params['extensions'] = 'csv, xls, xlsx'
        resp = self.client.post(self.url, params)
        if resp.status_code == 200:
            raise AssertionError('Invalid form: %s' % resp.context['form'].errors)

        self.assertEquals(resp.status_code, 302)
        self.assertEquals(
            Extension.objects.filter(
                name='csv',
                format__name=params['name']).count(),
            1)
        self.assertEquals(
            Extension.objects.filter(
                name='xls',
                format__name=params['name']).count(),
            1)
        self.assertEquals(
            Extension.objects.filter(
                name='xlsx',
                format__name=params['name']).count(),
            1)


class FormatListTest(BaseTest, NodeListTestMixin, ListPermissionTestMixin):

    def get_url(self):
        return reverse('editor:format-list')

    def get_model_class(self):
        return Format

    def get_model_factory_class(self):
        return FormatFactory


class FormatNodeUpdateTest(BaseUpdateTest):
    # TODO: check permissions
    def get_url(self):
        self.root = FormatFactory()
        self.format1 = FormatFactory(parent=self.root)
        return self.format1.get_absolute_url()

    def get_model_class(self):
        return Format

    def get_model_factory_class(self):
        return FormatFactory

    def get_update_params(self):
        params = {
            'name': 'Node 2'
        }
        return params

    def test_renders_extensions(self):
        ext1 = ExtensionFactory(format=self.format1, name='csv123')
        ext2 = ExtensionFactory(format=self.format1, name='xlsx123')
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(
            '%s, %s' % (ext1.name, ext2.name),
            resp.content,
            'Extensions was not found in the content.')

    def test_creates_extensions(self):
        params = self.update_params
        params['extensions'] = 'csv'
        resp = self.client.post(self.url, params)
        if resp.status_code == 200:
            raise AssertionError('Invalid form: %s' % resp.context['form'].errors)

        self.assertEquals(resp.status_code, 302)
        self.assertEquals(
            Extension.objects.filter(
                name='csv',
                format__name=params['name']).count(),
            1)

    def test_deletes_missed_extensions(self):
        ext1 = ExtensionFactory(format=self.format1, name='csv')
        ExtensionFactory(format=self.format1, name='xlsx')
        ExtensionFactory(format=self.format1, name='exe')
        params = self.update_params
        params['extensions'] = ext1.name
        resp = self.client.post(self.url, params)
        if resp.status_code == 200:
            raise AssertionError('Invalid form: %s' % resp.context['form'].errors)

        self.assertEquals(resp.status_code, 302)
        self.assertEquals(Extension.objects.all().count(), 1)
        self.assertEquals(
            Extension.objects.filter(
                name='csv',
                format__name=params['name']).count(),
            1)


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


class DatasetCreateTest(BaseTest):

    def get_url(self):
        self.source1 = SourceFactory()
        return reverse('editor:dataset-create', kwargs={'source_pk': self.source1.id})

    def get_model_class(self):
        return Dataset

    def get_model_factory_class(self):
        return DatasetFactory

    def test_is_not_available_for_anonymous(self):
        self.client.logout()
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_post_is_not_available_without_permission(self):
        self.user1.user_permissions.all().delete()
        resp = self.client.post(self.url, {})
        self.assertEqual(resp.status_code, 403)

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
        root_categ = CategoryFactory()
        categ1 = CategoryFactory(parent=root_categ)

        root_format = FormatFactory()
        format1 = FormatFactory(parent=root_format)
        post_params = {
            'title': 'Title 1',
            'categories': [categ1.id],
            'start_year': 1976,
            'end_year': 1976,
            'coverage': Dataset.STATE,
            'region': Dataset.STATE,
            'page': 'http://ya.ru',
            'formats': [format1.id],
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
        give_perm(self.user1, Dataset, 'add_dataset')
        give_perm(self.user1, Dataset, 'change_dataset')

    def test_returns_details_for_anonymous(self):
        self.client.logout()
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.ds1.title, resp.content)

    def test_post_is_forbidden_without_permission(self):
        self.user1.user_permissions.all().delete()
        resp = self.client.post(self.url, {})
        self.assertEqual(resp.status_code, 403)

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
        root_categ = CategoryFactory()
        categ1 = CategoryFactory(parent=root_categ)

        root_format = FormatFactory()
        format1 = FormatFactory(parent=root_format)
        post_params = {
            'title': '%s updated' % self.ds1.title,
            'categories': [categ1.id],
            'variant': '%s updated' % self.ds1.variant,
            'start_year': 1976,
            'end_year': 1976,
            'coverage': Dataset.STATE,
            'region': Dataset.STATE,
            'page': 'http://ya.ru',
            'download_page': 'http://ya.ru',
            'contacts': 'contact@gmail.com',
            'formats': [format1.id],
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
        give_perm(self.user1, DataFile, 'add_datafile')
        give_perm(self.user1, DocumentFile, 'add_documentfile')

    def test_is_disabled_for_anonymous(self):
        self.client.logout()
        resp = self.client.post(self.url)
        self.assertEqual(resp.status_code, 302)
        # TODO: Is it really redirect to login page? Test that.

    def test_post_is_forbidden_without_permission(self):
        self.user1.user_permissions.all().delete()
        resp = self.client.post(self.url, {})
        self.assertEqual(resp.status_code, 403)

    @fudge.patch('editor.views.get_links')
    def test_returns_all_links_from_given_url(self, fake_get):
        fake_get.expects_call()\
            .returns([{'text': 'Yandex', 'href': 'http://yandex.ru'}])

        post_data = {'url': 'http://yandex.ru'}
        resp = self.client.post(
            self.url, post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertIn('links', content)
        self.assertIn('text', content['links'][0])
        self.assertIn('href', content['links'][0])
        self.assertEquals(content['links'][0]['href'], 'http://yandex.ru')
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

    @fudge.patch(
        'editor.views.get_links',
        'editor.views.guess_format')
    def test_returns_guessed_formats(self, fake_get, fake_guess):
        fake_get.expects_call()\
            .returns([{'href': 'http://ya.ru'}])
        fake_guess.expects_call()\
            .returns([{'href': 'http://ya.ru', 'format': {'id': 1, 'name': 'test'}}])
        post_data = {'url': 'http://yandex.ru/'}
        resp = self.client.post(
            self.url, post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertIn('links', content)
        self.assertIn('format', content['links'][0])
        self.assertEqual(content['links'][0]['format']['id'], 1)


class ValidateURLTest(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        logged_in = self.client.login(
            username=self.user1.username,
            password='1')
        self.assertTrue(logged_in)
        self.url = reverse('editor:validate-url')

    def test_is_disabled_for_anonymous(self):
        self.client.logout()
        resp = self.client.post(self.url)
        self.assertEqual(resp.status_code, 302)

    def test_get_is_not_allowed(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 405)

    def test_returns_error_for_invalid_url(self):
        resp = self.client.post(self.url, {'url': 'bla'})
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertIn('error', content)
        self.assertIn('Enter a valid URL', content['error'])

    @fudge.patch('editor.views.requests.head')
    def test_returns_error_with_http_stasus_if_status_is_not_200(self, fake_head):
        class FakeForbidden(object):
            status_code = 403
            content = ''
            reason = ''

        fake_head.expects_call()\
            .returns(FakeForbidden)
        resp = self.client.post(self.url, {'url': 'http://ya.ru'})
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertIn('error', content)
        self.assertIn('403', content['error'])

    @fudge.patch('editor.views.requests.head')
    def test_returns_success_if_url_found(self, fake_head):
        class FakeSuccess(object):
            status_code = 200
            content = ''

        fake_head.expects_call()\
            .returns(FakeSuccess)

        resp = self.client.post(self.url, {'url': 'http://ya.ru'})
        self.assertEqual(resp.status_code, 200)
        content = json.loads(resp.content)
        self.assertIn('is_valid', content)
        self.assertTrue(content['is_valid'])
        self.assertNotIn('errors', content)
