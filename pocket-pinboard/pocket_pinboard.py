import os
import json
import requests

FILE_DIR = os.path.dirname(os.path.realpath(__file__))

class Pinboard(object):

    url = 'https://api.pinboard.in/v1'

    def __init__(self, token):
        self.token   = token
        self.payload = dict(auth_token=self.token, format='json') 

    def _get(self, endpoint, **kw):
        url  = os.path.join(self.url, endpoint)
        kw.update(self.payload) 
        return requests.get(url, params=kw)

    def get_posts(self):
        return self._get('posts/all').json()

    def add_post(self, url, description, tags=None):
        kw = [('url', url), ('description', description)]
        return self._get('posts/add', **(dict(kw) if not tags else dict(kw+[('tags', tags)])))

    def delete_post(self, url):
        return self._get('posts/delete', url=url)

class Pocket(object):

    url = 'https://getpocket.com/v3'

    def __init__(self, key, token):
        self.key    = key
        self.token  = token
        self.data   = dict(consumer_key=self.key, access_token=self.token)

    def _post(self, endpoint, data):
        url = os.path.join(self.url, endpoint)
        data.update(self.data)
        return requests.post(url, data=data)

    def _get(self, endpoint, params):
        url = os.path.join(self.url, endpoint)
        params.update(self.data)
        return requests.post(url, params)

    def get_posts(self):
        data = dict(detailType='simple', state='all')
        return self._post('get', data).json()

    def add_multiple(self, posts, posts_info=('url', 'tags', 'title')):
        actions = [dict([(k,p[k]) for k in posts_info if k in p] + [('action', 'add')]) for p in posts]
        data = dict(actions=json.dumps(actions))
        return self._get('send', data)

    def delete_multiple(self, item_ids):
        actions = [dict(item_id=int(i), action='delete') for i in item_ids]
        data    = dict(actions=json.dumps(actions))
        return self._get('send', data)

class Pinboard_to_Pocket(object):

    @staticmethod
    def load_config(cfg_path):
        with open(cfg_path, 'r') as f:
            return json.load(f)

    def __init__(self, cfg_name):
        self.cfg_path   = os.path.join(FILE_DIR, cfg_name)
        self.config     = self.load_config(self.cfg_path)
        self.pocket     = Pocket(self.config['pocket']['key'], self.config['pocket']['token'])
        self.pinboard   = Pinboard(self.config['pinboard']['token'])

if __name__ == '__main__':
    pass