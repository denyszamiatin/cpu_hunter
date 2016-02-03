# -*- coding: utf-8 -*-
import ConfigParser
import abc
import re
from urlparse import urlparse

import requests
import chardet
from lxml import html
from pymongo import MongoClient


CONFIG_FILENAME = 'hunter.cfg'
MONGO_DB = 'hunter_database'


class Reader(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_url(self):
        pass


class AbsoluteUrl(object):
    def __init__(self, adress):
        self.domain = urlparse(adress).netloc
        self.path = urlparse(adress).path
        self.scheme = urlparse(adress).scheme()
        self.port = urlparse(adress).port


class ConfigReader(Reader):
    """
    Reads a config file and gives methods for getting config parameters
    """

    def __init__(self, filename=CONFIG_FILENAME):
        self.config = ConfigParser.ConfigParser()
        self.config.read(filename)

    def get_url(self):
        return self.config.get('initial_configuration', 'url')

    def get_link_template(self):
        return self.config.get('initial_configuration', 'linktemplate')


class XMLReader(Reader):
    def get_url(self):
        pass


class MongoWorker(object):
    """
    Writes data to local MongoDB
    """

    mongo_client = MongoClient()
    db = mongo_client[MONGO_DB]

    def write_item(self, data):
        return self.db.items.insert_one(data).inserted_id


class Page(object):

    def __init__(self, url, content):
        self.url = url
        self.content = content

    def decode(self, encoding):
        self.content = self.content.decode(encoding)


def get_web_page(url):
    """
    Downloads WebPage by given URL
    """
    return Page(url, requests.get(url).content)


def get_encoding(page):
    """
    Returns guessed encoding of a given WebPage
    """
    return chardet.detect(page)['encoding']


def get_product_url(page):
    """
    Returns a set of links found on a given WebPage using a template located
    in hunter.cfg
    """
    tree = html.fromstring(page)
    return tree.xpath(config.get_link_template())


CHARS = {
    'TITLE': re.compile('.*<title>(.*)</title>'),
    'DESCRIPTION': re.compile('.*<meta name="description" content="(.*)".*/>'),
    'WHERE': re.compile('<strong class="c2b small">\n(.*)</strong>'),
    "WHEN": re.compile('(.*),.*<span class="nowrap marginright5">'),
    'COMMENT': re.compile('.*<p class="pding10 lheight20 large">\n.(.*)</p>')
}


def convert_item(item):
    return item[0] if item else []


def get_details(page):
    """
    Uses a set of RegExp expressions "CHARS" to find and return a dictionary
    of values
    """
    return {char: convert_item(regex.findall(page))
            for char, regex in CHARS.items()}


config = ConfigReader()
url = config.get_url()
page = get_web_page(url)
encoding = get_encoding(page.content)
page.decode(encoding)
print get_product_url(page.content)
# print AbsoluteUrl(url).scheme
# print AbsoluteUrl(url).domain
# print AbsoluteUrl(url).path

database_worker = MongoWorker()
for cpu_url in get_product_url(page.content):
    cpu_page = get_web_page(cpu_url)
    details = get_details(cpu_page.content)
    details['url'] = cpu_page.url
    database_worker.write_item(details)
