import requests


class WykopAPIError(Exception):
    
    def __init__(self, message, code):
        self.message = message
        self.code = code

    def __str__(self):
        return repr(self.message)


class WykopAPI:
    '''
    API wrapper of wykop.pl's API.
    API documentation: https://www.wykop.pl/dla-programistow/apiv2docs/
    '''

    api_url = 'https://a2.wykop.pl/'
    urls = {
        'hits_month': '{api_url}Hits/Month/{year}/{month}/appkey/{api_key}/page/{page}/'
    }
    
    def __init__(self, api_key, secret_key = None):
        self.api_key = api_key
        self.secret_key = secret_key
        self.session = requests.Session()

    def get_hits_month(self, year, month, page):
        '''Get best links of selected month'''
        url = self._get_url('hits_month', year=year, month=month, page=page)
        return self.get(url)

    def get(self, url):
        response = self.session.get(url)
        response.raise_for_status()
        data = response.json()
        self._raise_if_error(data)
        return data

    def _get_url(self, url_id, **kwargs):
        url = self.urls[url_id]
        return url.format(api_url=self.api_url, api_key=self.api_key, **kwargs)
    
    def _raise_if_error(self, data):
        if 'error' in data:
            err = data['error']
            raise WykopAPIError(err['message_en'], err['code'])