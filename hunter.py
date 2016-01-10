import requests
# -*- coding: utf-8 -*-

url = 'http://olx.ua/elektronika/kompyutery/q-процессор/'

def get_web_page(url):
    page = requests.get(url)
    return page._content

def write_to_text_file(filename, data):
    with open(filename, 'w') as f:
        f.write(data)
    f.closed

write_to_text_file('olx.txt', get_web_page(url))