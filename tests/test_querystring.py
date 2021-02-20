# -*- coding: utf-8 -*-

from __future__ import absolute_import

import unittest

import six
import six.moves.urllib.parse as urlparse

import urlparselib.querystring as querystring


class TestQuote(unittest.TestCase):
    def test_bytestring(self):
        quoted_string = querystring.quote(u'€'.encode('utf-8'))
        self.assertEqual('%E2%82%AC', quoted_string)

    def test_text(self):
        quoted_string = querystring.quote(u'€')
        self.assertEqual('%E2%82%AC', quoted_string)


class TestAppendQueryStringParameters(unittest.TestCase):
    def test_append_one_param(self):
        base_url = 'http://www.example.com/path/'
        query_params = [
            ('param€', '€'),
            ('paramῬ', 'δ'),
        ]
        query_string = '&'.join(
            ['{}={}'.format(querystring.quote(n), querystring.quote(v))
             for n, v in query_params]
        )
        url = '{}?{}'.format(base_url, query_string)
        new_query_params = [
            ('paramό', 'ς')
        ]
        quoted_new_query_params = [
            (querystring.quote(n), querystring.quote(v))
            for n, v in new_query_params
        ]
        final_url = querystring.append_parameters(url, quoted_new_query_params)
        unquoted_final_url = urlparse.unquote_to_bytes(final_url)
        decoded_final_url = unquoted_final_url.decode('utf-8')
        parsed_final_url = urlparse.urlparse(decoded_final_url)
        final_url_query_params = urlparse.parse_qsl(parsed_final_url[4])
        expected_query_params = [
            (urlparse.unquote_to_bytes(n).decode('utf-8'),
             urlparse.unquote_to_bytes(v).decode('utf-8'))
            for n, v in query_params + new_query_params
        ]

        six.assertCountEqual(
            self,
            expected_query_params,
            final_url_query_params
        )
