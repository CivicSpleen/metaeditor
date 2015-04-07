# -*- coding: utf-8 -*-
import fudge

from django.test import TestCase

from editor.utils import get_links

# tests of the https://github.com/CivicKnowledge/metaeditor/issues/26


class Test(TestCase):

    @fudge.patch('editor.utils.requests.get')
    def test_returns_all_found_links(self, fake_get):
        class FakeSuccessResponse(object):
            status_code = 200
            content = '''
              <html>
                <body>
                  <div>
                    <a href="FacilityList/HospitalListing_Dec2014.xlsx" class="c-ext-Select-like-a-Boss">
                      Hospital Listing.xlsx
                    </a>
                  </div>
                </body>
              </html>
            '''

        fake_get.expects_call()\
            .returns(FakeSuccessResponse())

        links = get_links('http://www.oshpd.ca.gov/HID/Products/Listings.html')
        self.assertEquals(len(links), 1)

        self.assertEqual(
            links[0]['href'],
            'http://www.oshpd.ca.gov/HID/Products/FacilityList/HospitalListing_Dec2014.xlsx')
