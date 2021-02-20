# -*- coding: utf-8 -*-

from __future__ import absolute_import

import six
import six.moves.urllib.parse as urlparse


def quote(s):
    if issubclass(type(s), six.text_type):
        s = s.encode('utf-8')

    return urlparse.quote(s)


def append_parameters(url, query_params):
    parsed_url = list(urlparse.urlparse(url))
    parsed_url_query_params = urlparse.parse_qsl(parsed_url[4])
    unquoted_query_params = [
        (urlparse.unquote(n), urlparse.unquote(v)) for n, v in query_params
    ]
    parsed_url[4] = urlparse.urlencode(
        parsed_url_query_params + unquoted_query_params
    )
    return urlparse.urlunparse(parsed_url)
