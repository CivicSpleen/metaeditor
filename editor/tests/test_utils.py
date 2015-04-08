# -*- coding: utf-8 -*-
import fudge

from django.test import TestCase

from editor.tests.factories import FormatFactory
from editor.utils import get_links, guess_format


class GetLinksTest(TestCase):

    @fudge.patch('editor.utils.requests.get')
    def test_returns_all_found_links(self, fake_get):
        class FakeSuccessResponse(object):
            status_code = 200
            content = '''
                <html>
                    <body>
                        <div>
                            <a href="http://python.org" title="Python">Python</a>
                        </div>
                        <a href="http://clojure.org" title="Clojure">Clojure</a>
                    </body>
                </html>
            '''

        fake_get.expects_call()\
            .returns(FakeSuccessResponse())

        links = get_links('http://fake.ru')
        self.assertEquals(len(links), 2)

        expected_python = {
            'href': 'http://python.org',
            'title': 'Python',
            'text': 'Python'}
        self.assertIn(
            expected_python, links)

        expected_clojure = {
            'href': 'http://clojure.org',
            'title': 'Clojure',
            'text': 'Clojure'}
        self.assertIn(
            expected_clojure, links)

    @fudge.patch('editor.utils.requests.get')
    def test_extends_relative_urls(self, fake_get):
        class FakeSuccessResponse(object):
            status_code = 200
            content = '''
                <html>
                    <body>
                        <a href="/index" title="Python">Python</a>
                    </body>
                </html>
            '''

        fake_get.expects_call()\
            .returns(FakeSuccessResponse())

        links = get_links('http://python.org/versions')
        self.assertEquals(len(links), 1)
        self.assertEquals(links[0]['href'], 'http://python.org/index')


class GuessFormatTest(TestCase):
    @fudge.patch(
        'editor.models.Format.guess_by_path')
    def test_extends_links_with_found_format(self, fake_guess):
        format1 = FormatFactory()
        fake_guess.expects_call()\
            .returns(format1)
        links = [{'href': 'http://ya.ru'}]
        guessed_links = guess_format(links)
        self.assertIn('format', guessed_links[0])
        self.assertEqual(guessed_links[0]['format']['id'], format1.id)
        self.assertEqual(guessed_links[0]['format']['name'], format1.name)
