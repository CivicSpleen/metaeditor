# -*- coding: utf-8 -*-

import fudge

from django.test import TestCase

from editor.models import Format
from editor.tests.factories import FormatFactory, ExtensionFactory


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
