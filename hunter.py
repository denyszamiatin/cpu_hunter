# -*- coding: utf-8 -*-

import requests
import chardet


URL = 'http://olx.ua/elektronika/kompyutery/q-процессор/'


def get_web_page(url):
    return requests.get(url).content


print get_web_page(URL)


def get_page_code():
    coding = chardet.detect(get_web_page(URL)).get('encoding')
    return coding


