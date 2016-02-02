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
    Wrires data to local MongoDB
    """

    mongo_client = MongoClient()
    db = mongo_client.items_database
    def write_item(self, data):
        information = data
        return MongoWorker.db.items.insert_one(information).inserted_id


def get_web_page(url):
    """
    Downloads WebPage by given URL
    """
    return requests.get(url).content


def get_encoding(page):
    """
    Returns guessed encoding of a given WebPage
    """
    return chardet.detect(page)['encoding']


def get_product_url(page):
    """
    Returns a set of links found on a given WebPage using a template located in hunter.cfg
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


def get_details(page):
    """
    Uses a set of RegExp expressions "CHARS" to find and return a dictionary of values
    """
    dict_to_return = {}
    for char, regex in CHARS.items():
        dict_to_return.update({char : regex.findall(page)})
    return dict_to_return


config = ConfigReader()
url = config.get_url()
page = get_web_page(url)
encoding = get_encoding(page)
unicode_page = page.decode(encoding)
print get_product_url(unicode_page)
print AbsoluteUrl(url).scheme
print AbsoluteUrl(url).domain
print AbsoluteUrl(url).path

database_worker = MongoWorker()
for i in get_product_url(unicode_page):
    database_worker.write_item(get_details(get_web_page(i)))
