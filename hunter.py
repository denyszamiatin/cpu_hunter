# -*- coding: utf-8 -*-
import ConfigParser

import requests
import chardet

CONFIG_FILENAME = 'hunter.cfg'


class ConfigReader(object):
    def __init__(self, filename=CONFIG_FILENAME):
        self.config = ConfigParser.ConfigParser()
        self.config.read(filename)

    def get_url(self):
        return self.config.get('initial_configuration', 'url')


def get_web_page(url):
    return requests.get(url).content


def get_encoding(page):
    return chardet.detect(page)['encoding']


config = ConfigReader()
url = config.get_url()
page = get_web_page(url)
encoding = get_encoding(page)
unicode_page = page.decode(encoding)
print unicode_page
