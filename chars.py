# this code gives us all links from page

import re
import requests

# -*- coding: utf-8 -*-

url = 'http://olx.ua/obyavlenie/protsesor-intel-i5-560m-IDhZVoE.html#a78a8da37c'


def get_web_page(url):
    page = requests.get(url)
    return page._content


page = get_web_page(url)
titles = re.findall('.*<title>(.*)</title>', page)
for title in titles:
    print 'TITLE:', title.strip()
description = re.findall('.*<meta name="description" content="(.*)".*/>', page)
for descriptio in description:
    print 'DESCRIPTION:', descriptio.strip()
place = re.findall('<strong class="c2b small">\n(.*)</strong>', page)
for pl in place:
    print 'WHERE:', pl.strip()
time = re.findall('(.*),.*<span class="nowrap marginright5">', page)
for tm in time:
    print "WHEN:", tm.strip()
comment =re.findall('.*<p class="pding10 lheight20 large">\n.(.*)</p>', page)
for comm in comment:
    print 'COMMENT:', comm.strip()

