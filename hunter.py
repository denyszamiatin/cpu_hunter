# -*- coding: utf-8 -*-
import ConfigParser
import abc
import re
from urlparse import urlparse

import requests
import chardet

CONFIG_FILENAME = 'hunter.cfg'


class Reader(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_url(self):
        pass


class AbsoluteUrl(object):
    def __init__(self, adress):
        self.domain = urlparse(adress).netloc
        self.path = urlparse(adress).path
        self.scheme = urlparse(adress).scheme
        self.port = urlparse(adress).port


class ConfigReader(Reader):
    def __init__(self, filename=CONFIG_FILENAME):
        self.config = ConfigParser.ConfigParser()
        self.config.read(filename)

    def get_url(self):
        return self.config.get('initial_configuration', 'url')


class XMLReader(Reader):
    def get_url(self):
        pass


def get_web_page(url):
    return requests.get(url).content


def get_encoding(page):
    return chardet.detect(page)['encoding']


CHARS = {
    'TITLE': re.compile('.*<title>(.*)</title>'),
    'DESCRIPTION': re.compile('.*<meta name="description" content="(.*)".*/>'),
    'WHERE': re.compile('<strong class="c2b small">\n(.*)</strong>'),
    "WHEN": re.compile('(.*),.*<span class="nowrap marginright5">'),
    'COMMENT': re.compile('.*<p class="pding10 lheight20 large">\n.(.*)</p>')
}


def get_details(page):
    for char, regex in CHARS.items():
        print '{}: {}'.format(char, regex.findall(page)[0].strip())



config = ConfigReader()
url = config.get_url()
page = get_web_page(url)
encoding = get_encoding(page)
unicode_page = page.decode(encoding)
print AbsoluteUrl(url).scheme
print AbsoluteUrl(url).domain
print AbsoluteUrl(url).path


