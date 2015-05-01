# -*- coding: utf-8 -*-

from django.test import TestCase

import fudge
from fudge.inspector import arg

from editor.models import Format, Dataset
from editor.tests.factories import FormatFactory, ExtensionFactory,\
    DatasetFactory, DataFileFactory


class FormatTest(TestCase):

    def test_returns_format_found_by_extension(self):
        format1 = FormatFactory()
        ExtensionFactory(format=format1, name='csv')
        self.assertEqual(
            Format.guess_by_path('/some/path/file.csv'),
            format1)

    def test_returns_none_if_extension_does_not_exist(self):
        self.assertEqual(
            Format.guess_by_path('/some/path/file.csv'),
            None)


class DatasetTest(TestCase):
    def test_update_formats_adds_missed_formats(self):
        format1 = FormatFactory()
        format2 = FormatFactory()
        ds1 = DatasetFactory()
        DataFileFactory(dataset=ds1, file_format=format1)
        DataFileFactory(dataset=ds1, file_format=format2)
        ds1.update_formats()
        self.assertEquals(
            ds1.formats.all().count(), len([format1, format2]))
        self.assertIn(format1, ds1.formats.all())
        self.assertIn(format2, ds1.formats.all())

    def test_deletes_redundant_formats(self):
        dataset_format = FormatFactory()
        datafile_format1 = FormatFactory()
        datafile_format2 = FormatFactory()

        # create dataset with one format
        ds1 = DatasetFactory()
        ds1.formats.add(dataset_format)

        # create files with formats
        DataFileFactory(dataset=ds1, file_format=datafile_format1)
        DataFileFactory(dataset=ds1, file_format=datafile_format2)
        ds1.update_formats()

        # now dataset should have datafiles formats only
        self.assertEquals(
            ds1.formats.all().count(), len([datafile_format1, datafile_format2]))
        self.assertIn(datafile_format1, ds1.formats.all())
        self.assertIn(datafile_format2, ds1.formats.all())

    def test_leaves_existing_formats_if_dataset_does_not_have_datafiles(self):
        dataset_format = FormatFactory()

        # create dataset with one format
        ds1 = DatasetFactory()
        ds1.formats.add(dataset_format)

        # dataset should not have any datafile
        self.assertFalse(ds1.datafile_set.all().exists())

        # create files with formats
        ds1.update_formats()

        # now dataset should have datafiles formats only
        self.assertIn(
            dataset_format, ds1.formats.all())

    @fudge.patch(
        'editor.models.ambry_utils.get_vid')
    def test_gets_vid_from_ambry_if_vid_is_empty(self, fake_get):
        fake_get.expects_call()\
            .returns('d0000001')
        ds1 = DatasetFactory(vid=None)
        self.assertEquals(
            Dataset.objects.get(id=ds1.id).vid,
            'd0000001')

    def test_saves_given_vid(self):
        ds1 = DatasetFactory(vid='abcde')
        self.assertEquals(
            Dataset.objects.get(id=ds1.id).vid,
            'abcde')


class DataFileTest(TestCase):

    @fudge.patch('editor.models.Dataset.update_formats')
    def test_updates_dataset_formats_after_save(self, fake_update):
        fake_update.expects_call()
        dataset1 = DatasetFactory()
        DataFileFactory(dataset=dataset1)
