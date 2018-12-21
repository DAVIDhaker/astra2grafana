#!/usr/bin/python3

# (c) DAVIDhaker

from json import loads, dumps
from urllib.parse import urlparse
from os import listdir
from copy import deepcopy
from math import floor
from operator import itemgetter
from sys import argv

def die(msg):
    print(msg) 
    exit()

def jload(file):
    return loads(open(file).read())

def id():
    try:
        id.counter += 1
    except:
        id.counter = 1000

    return id.counter

try:
    astra_conf = jload(argv[1])
except:
    die('Fail to load/parse astra config')

try:
    board = jload('grafana/__dashboard__.json')
except Exception as e:
    die('Fail to read/parse source dashboard: ' + e)

board['title'] = input('Dashboard title: ')
datasource = input('Datasource name (in Grafana, must be influx): ')
maxDataPoints = 40

y = 0

for file in sorted(listdir('grafana')):
    if file in ['.', '..', '__dashboard__.json']:
        continue

    name = file[file.find('_') + 1:-5:]

    print('Processing ' + name)

    _panel = jload('grafana/' + file)

    if name == 'channel' or name == 'transponder':
        item_counter = 0

        try:
            for sequence in sorted(astra_conf['make_stream' if name == 'channel' else 'dvb_tune'], key=itemgetter('name')):
                if not sequence['enable']: # Show only enabled streams and transponders
                    continue

                print('\t' + sequence['name'])

                panel = deepcopy(_panel)
                panel['maxDataPoints'] = maxDataPoints
                panel['datasource'] = datasource
                panel['title'] = sequence['name']
                panel['id'] = id()
                panel['gridPos']['x'] = floor(item_counter % 4) * 6
                panel['gridPos']['y'] = floor(item_counter / 4) * (6 if name == 'channel' else 7) + y

                for target in panel['targets']:
                    target['query'] = target['query'].replace('{id}', sequence['id'])

                board['panels'].append(panel)
                item_counter += 1
            y = panel['gridPos']['y'] + panel['gridPos']['h']
        except:
            print('\tFail to process ' + name)        
    else:
        panel = deepcopy(_panel)

        try:
            panel['datasource'] = datasource
        except:
            pass

        try:
            panel['maxDataPoints'] = maxDataPoints
        except:
            pass
        
        panel['gridPos']['y'] = y
        
        y += panel['gridPos']['h']

        panel['id'] = id()
        board['panels'].append(panel)

open('out.json', 'w').write(dumps(board, indent=4))



