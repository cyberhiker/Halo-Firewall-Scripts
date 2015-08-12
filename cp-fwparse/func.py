#!/usr/bin/python3
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

def debugoutput(flag, text):
    if flag != None:
        #Output to screen
        print(text)

def outputting(verbosity, outputfile, text):
    if outputfile != None:
        #Write out the File

        if verbosity != None:
            print(text)

    else:
        #Don't write to file, but you will be seeing text
        print(text)

# Returns a valid Authorization header
def authenticate(arguments):
    import base64

    settings = yaml.load(open("settings.yml", 'r'))
    url = 'https://' + settings['host'] + '/'
    func.debugoutput(arguments['-d'], url)

    decoded = settings['clientid'] + ':' + settings['clientsecret']
    encoded = base64.b64encode(decoded.encode('utf-8'))
    func.debugoutput(arguments['-d'], encoded)

    headers = {'Authorization': 'Basic ' + encoded.decode('ascii')}
    func.debugoutput(arguments['-d'], headers)

    delay = 1
    for i in range(settings['iterations']):
        while True:
            try:
                authresponse = requests.post(url + 'oauth/access_token?grant_type=client_credentials', headers=headers)

                if authresponse.status_code != 200:
                    authresponse.raise_for_status()
                else:
                    authjson = authresponse.json()

                    authHeader = {'Authorization': 'Bearer ' + authjson['access_token']}
                    func.debugoutput(arguments['-d'], authHeader.json())

                    return authHeader

            except requests.exceptions.ConnectionError as e:
                func.outputting(arguments['-q'], arguments['-o'], 'Could not Connect to Halo Instance. \nCheck your settings.yaml and try again.')
                quit()
            except requests.exceptions.HTTPError as e:
                func.outputting(arguments['-q'], arguments['-o'], str(e) + ' \nCheck your settings.yaml and try again.')
                quit()
            except requests.exceptions.URLRequired:
                func.outputting(arguments['-q'], arguments['-o'], 'The URL is incorrectly formed. \nCheck your settings.yaml and try again.')
                quit()
            except requests.exceptions.TooManyRedirects:
                func.outputting(arguments['-q'], arguments['-o'], 'Too Many Redirects to be healthy.  Giving up')
                quit()
            except requests.exceptions.Timeout:
                attempts = settings['iterations'] - i
                func.outputting(arguments['-q'], arguments['-o'], 'The request timed due to network or server problems.  Trying {0} more times.'.format(attempts))
                polling_time = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
                func.outputting(arguments['-q'], arguments['-o'], "{0}. Sleeping for {1} seconds.".format(polling_time, delay))
                time.sleep(delay)
                delay *= 2
                continue
            break
