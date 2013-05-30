import requests
import os
from pprint import pprint

TOKEN = os.environ.get('SCRIBBLELIVE_TOKEN')
USERNAME = os.environ.get('SCRIBBLELIVE_USERNAME')
PASSWORD = os.environ.get('SCRIBBLELIVE_PASSWORD')
FLUSH = os.environ.get('SCRIBBLELIVE_FLUSH')
ARCHIVE = 'events'
URL_BASE = "http://apiv1.scribblelive.com/api/rest"
WEBSITE = 907


def req(url, method='GET', extra_params={}, auth=None):
    params = {'Token': TOKEN}
    params.update(extra_params)
    res = requests.get(URL_BASE + url,
                       auth=auth,
                       params=params,
                       headers={'Accept': 'application/json'})
    return res


def get_auth():
    res = req('/user', auth=(USERNAME, PASSWORD))
    return res.json().get('Auth')


def get_event(event):
    #pprint(event)
    print (event.get('Id'), event.get('Title'), event.get('Pages'))
    for page in range(event.get('Pages')):
        res = req('/event/%s/page/%s' % (event.get('Id'), page))
        file_name = os.path.join(ARCHIVE, 'event_%s_page_%s.json' % (event.get('Id'), page))
        with open(file_name, 'wb') as fh:
            fh.write(res.content)
        res = req('/event/%s/page/%s' % (event.get('Id'), page),
                  extra_params={'callback': 'sponGetData'})
        file_name = os.path.join(ARCHIVE, 'event_%s_page_%s_cb.json' % (event.get('Id'), page))
        with open(file_name, 'wb') as fh:
            fh.write(res.content)


def flush_event(event_id):
    auth = get_auth()
    res = req('/event/%s' % event_id)
    event = res.json()
    if event.get('IsLive'):
        print "Event %s is live, not flushing..." % event_id
        return
    get_event(event)
    print ['Flushing %s...' % event.get('Title')]
    for page in range(event.get('Pages')):
        res = req('/event/%s/page/%s' % (event.get('Id'), page))
        for post in res.json().get('Posts'):
            res = req('/post/%s/delete' % post.get('Id'),
                      extra_params={'Auth': auth})
            print res.json()


def get_events():
    if not os.path.isdir(ARCHIVE):
        os.makedirs(ARCHIVE)
    res = req('/website/%s/events' % WEBSITE,
              extra_params={'Max': 1000})
    for event in res.json().get('Events'):
        get_event(event)


if __name__ == '__main__':
    get_events()
    for flush_id in FLUSH.split(','):
        flush_event(int(flush_id))
