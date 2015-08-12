#!/usr/bin/python
#

__author__ = 'Chris Burton'

import yaml
import requests
from collections import OrderedDict
from json import JSONDecoder

def make_unique(key, dct):
    counter = 0
    unique_key = key

    while unique_key in dct:
        counter += 1
        unique_key = '{}_{}'.format(key, counter)
    return unique_key


def parse_object_pairs(pairs):
    dct = OrderedDict()
    for key, value in pairs:
        if key in dct:
            key = make_unique(key, dct)
        dct[key] = value

    return dct

# Returns a valid Authorization header
def authenticate():
    import base64

    settings = yaml.load(open("settings.yml", 'r'))
    url = 'https://' + settings['host'] + '/'

    decoded = settings['clientid'] + ':' + settings['clientsecret']
    encoded = base64.b64encode(decoded.encode('utf-8'))
    headers = {'Authorization': 'Basic ' + encoded.decode('ascii')}

    for i in range(settings['iterations']):
        while True:
            try:
                authresponse = requests.post(url + 'oauth/access_token?grant_type=client_credentials', headers=headers)

                if authresponse.status_code != 200:
                    authresponse.raise_for_status()
                else:
                    authjson = authresponse.json()

                    authHeader = {'Authorization': 'Bearer ' + authjson['access_token']}
                    return authHeader

            except requests.exceptions.ConnectionError as e:
                print('Could not Connect to Halo Instance. \nCheck your settings.yaml and try again.')
                quit()
            except requests.exceptions.HTTPError as e:
                print(str(e) + ' \nCheck your settings.yaml or Contact Customer Success')
                quit()
            except requests.exceptions.URLRequired:
                print('The URL is incorrectly formed.')
                quit()
            except requests.exceptions.TooManyRedirects:
                print('Too Many Redirects to be healthy.  Giving up')
                quit()
            except requests.exceptions.Timeout:
                print('The request timed due to network or server problems.\n Retrying.')
                continue
            break
