# -*- coding: utf-8 -*-

import requests

URL = 'http://olx.ua/elektronika/kompyutery/q-процессор/'


def get_web_page(url):
    return requests.get(url).content


print get_web_page(URL)
