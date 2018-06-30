import csv
import time
import io

import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

req = requests.get('https://www.boardgamegeek.com/xmlapi/geeklist/219847')
root = ET.fromstring(req.content)

with io.open('bgg-library.csv', 'w', encoding='utf8') as f:
    f.write(u'id,title')
    for item in root.findall('item'):
        f.write(item.get('objectid') + u',' + item.get('objectname') + u'\n')