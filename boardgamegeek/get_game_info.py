import csv
import time

import requests
from bs4 import BeautifulSoup


def get_val(tag, term):
    try:
        val = tag.find(term)['value'].encode('ascii', 'ignore')
    except:
        val = 'NaN'
    return val

def get_max(item):
    results = item.findAll('result', { 'value': 'Best'})
    recommendedplayers = 0
    maxvotes = 0
    player = 0
    for r in results:
        player = player + 1
        numvotes = int(r['numvotes'])
        if numvotes > maxvotes:
            maxvotes = numvotes
            recommendedplayers = player
    return recommendedplayers or ''

base = 'http://www.boardgamegeek.com/xmlapi2/thing?id={}&stats=1'
detailbase = 'https://boardgamegeek.com/boardgame/'
with open('ids.txt') as f:
    ids = [line.strip() for line in f.readlines()]
split = 30
f = open('games.csv', 'w')
writer = csv.writer(f)
writer.writerow((
    'ID',
    'GAME',
    'RATING',
    'TIME',
    'MIN PLAYERS',
    'MAX PLAYERS',
    'REC PLAYERS',
    'MECHANICS',
    'DEMO',
    'WANTS TO PLAY',
    'OWNS',
    'PLAYED',
    'BGG LINK'    
))
for i in range(0, len(ids), split):
    url = base.format(','.join(ids[i:i+split]))
    print('Requesting {}'.format(url))
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'xml')
    items = soup.find_all('item')
    for item in items:

        results = item.findAll('result', { 'value': 'Recommended'})
        id = item['id']
        gname = get_val(item, 'name')
        avg = get_val(item.statistics.ratings, 'average')
        gplay = get_val(item, 'playingtime')
        gmin = get_val(item, 'minplayers')
        gmax = get_val(item, 'maxplayers')
        grec = get_max(item)
        mechanics = ', '.join(m['value'] for m in item.findAll('link', {'type': 'boardgamemechanic'})).encode('ascii', 'ignore')
        demo = ''.encode('ascii', 'ignore')
        wantstoplay = ''.encode('ascii', 'ignore')
        owns = ''.encode('ascii', 'ignore')
        played = ''.encode('ascii', 'ignore')
        link = detailbase + item['id']

        writer.writerow((
            id,
            gname,
            avg,
            gplay,
            gmin,
            gmax,
            grec,
            mechanics,
            demo,
            wantstoplay,
            owns,
            played,
            link))
    time.sleep(2)
f.close()
