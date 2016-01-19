# -*- coding: utf-8 -*-

import requests
import chardet
import ConfigParser


def get_page_code():
    coding = chardet.detect(get_web_page(URL)).get('encoding')
    return coding


def read_config_file():
    config = ConfigParser.ConfigParser()
    config.read('hunter.cfg')
    return dict(config.items('initial_configuration'))


def get_web_page(url):
    return requests.get(url).content

CONFIG = read_config_file()
URL = CONFIG.get('url')

print get_web_page(URL)