#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import itertools

from refinery.units import Arg, Unit
from refinery.lib.patterns import defanged, indicators


class defang(Unit):
    """
    Defangs all URL, domain and IPv4 address indicators in the input data by replacing the last dot
    in the expression by `[.]`. For example, `127.0.0.1` will be replaced by `127.0.0[.]1`. For URL
    indicators, the colon after the procol scheme is also wrapped in brackets.
    """

    _WHITELIST = [
        B'wscript.shell',
    ]

    _PROTOCOL_ESCAPES = {
        B'http': B'hxxp',
        B'https': B'hxxps',
        B'ftp': B'fxp',
        B'ftps': B'fxps',
    }

    def __init__(
        self,
        url_only: Arg.Switch('-u', help='Only defang URLs, do not look for domains or IPs.') = False,
        url_protocol: Arg.Switch('-p', help='Escape the protocol in URLs.') = False,
        dot_only: Arg.Switch('-d', help='Do not escape the protocol colon in URLs.') = False,
        quote_md: Arg.Switch('-q', help='Wrap all indicators in backticks for markdown code.') = False
    ):
        self.superinit(super(), **vars())

    def _quote(self, word):
        return word if not self.args.quote_md else B'`%s`' % word

    def reverse(self, data):
        def refang(hostname):
            return hostname[0].replace(B'[.]', B'.')
        data = defanged.hostname.sub(refang, data)
        data = data.replace(B'[:]//', B'://')
        data = data.replace(B'[://]', B'://')
        data = re.sub(B'h.{3}?(s?)://', B'http\\1://', data)
        data = re.sub(B'fxp(s?)://', B'ftp\\1://', data)
        return data

    def process(self, data):
        def replace_hostname(hostname, match=True):
            if match:
                return self._quote(replace_hostname(hostname[0], False))
            self.log_info('replace:', hostname)
            host = hostname.rsplit(B':')[0].lower()
            if host in self._WHITELIST:
                return hostname
            host = re.split(BR'(\[\.\]|\.)', hostname)
            if len(host) == 1:
                return host[0]
            host[-2] = B'[.]'
            return B''.join(host)

        def replace_url(url):
            if not url:
                return url
            sep = B'://' if self.args.dot_only else B'[:]//'
            self.log_info('replace:', url)
            p, q = re.split(BR'(?:\[:\]|:)//', url)
            q = q.split(B'/', 1)
            q[0] = replace_hostname(q[0], False)
            q = B'/'.join(q)
            if self.args.url_protocol and p:
                p = self._PROTOCOL_ESCAPES.get(p.lower(), p)

            return self._quote(p + sep + q)

        urlsplit = defanged.url.split(data)
        step = defanged.url.value.groups + 1
        urlsplit[1::step] = [replace_url(t) for t in itertools.islice(iter(urlsplit), 1, None, step)]

        if not self.args.url_only:
            urlsplit[0::step] = [
                indicators.hostname.sub(replace_hostname, t)
                for t in itertools.islice(iter(urlsplit), 0, None, step)
            ]

        def fuse(urlsplit):
            txt = itertools.islice(iter(urlsplit), 0, None, step)
            url = itertools.islice(iter(urlsplit), 1, None, step)
            while True:
                try:
                    yield next(txt)
                    yield next(url)
                except StopIteration:
                    break

        return B''.join(fuse(urlsplit))
