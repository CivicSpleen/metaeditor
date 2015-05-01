# -*- coding: utf-8 -*-

from django.test import TestCase

import fudge
from fudge.inspector import arg

from compat.ambry_utils import get_vid


class GetVidTest(TestCase):
    @fudge.patch('compat.ambry_utils.NumberServer')
    def test_gets_vid_from_ambry_number_server(self, fake_number):
        FakeNumberServer = fudge.Fake().provides('next').returns('d0000001')

        fake_number.expects_call()\
            .returns(FakeNumberServer)
        self.assertEquals(get_vid(), 'd0000001')

    @fudge.patch(
        'compat.ambry_utils.NumberServer',
        'compat.ambry_utils.logger.error')
    def test_logs_vid_retrieve_error(self, fake_number, fake_error):
        class MyFakeException(Exception):
            pass

        FakeNumberServer = fudge.Fake().provides('next').raises(MyFakeException)

        fake_number.expects_call()\
            .returns(FakeNumberServer)

        fake_error.expects_call()\
            .with_args(arg.contains('error while retrieving vid'))
        get_vid()
