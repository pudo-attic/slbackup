import requests
import os
import json
from pprint import pprint

TOKEN = os.environ.get('SCRIBBLELIVE_TOKEN')
AUTH = os.environ.get('SCRIBBLELIVE_AUTH')
ARCHIVE = 'events'
URL_BASE = "http://apiv1.scribblelive.com/api/rest"
WEBSITE = 907


def get_event(event):
    #pprint(event)
    print (event.get('Id'), event.get('Title'), event.get('Pages'))
    for page in range(event.get('Pages')):
        res = requests.get(URL_BASE + '/event/%s/page/%s' % (event.get('Id'), page),
            params={'Token': TOKEN},
            headers={'Accept': 'application/json'})
        file_name = os.path.join(ARCHIVE, 'event_%s_page_%s.json' % (event.get('Id'), page))
        with open(file_name, 'wb') as fh:
            fh.write(res.content)
        res = requests.get(URL_BASE + '/event/%s/page/%s' % (event.get('Id'), page),
            params={'Token': TOKEN, 'callback': 'sponGetData'},
            headers={'Accept': 'application/json'})
        file_name = os.path.join(ARCHIVE, 'event_%s_page_%s_cb.json' % (event.get('Id'), page))
        with open(file_name, 'wb') as fh:
            fh.write(res.content)



def get_events():
    if not os.path.isdir(ARCHIVE):
        os.makedirs(ARCHIVE)
    res = requests.get(URL_BASE + '/website/%s/events' % WEBSITE,
        params={'Token': TOKEN, 'Max': 1000},
        headers={'Accept': 'application/json'})
    for event in res.json().get('Events'):
        get_event(event)


if __name__ == '__main__':
    get_events()
