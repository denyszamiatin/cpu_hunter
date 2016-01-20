# this code gives us all links from page

import re
import requests
# -*- coding: utf-8 -*-

url = 'http://olx.ua/elektronika/kompyutery/q-%D0%BF%D1%80%D0%BE%D1%86%D0%B5%D1%81%D1%81%D0%BE%D1%80/'

def get_web_page(url):
    page = requests.get(url)
    return page._content

page = get_web_page(url)
links = re.findall('href="(http://.*?)"', page)
for link in links:
    print link
