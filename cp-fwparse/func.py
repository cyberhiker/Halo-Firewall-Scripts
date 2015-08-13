#!/usr/bin/python3
#
__author__ = 'Chris Burton'

import json
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
    if flag == True:
        # Output to screen
        print(text)

def outputting(quiet, outputfile, text):
    if outputfile != None:
        # Write out the File

        if quiet == False:
            print(text)

    else:
        # Don't write to file, but you will be seeing text
        print(text)

# Returns a valid Authorization header
def authenticate(arguments, settings):
    import base64

    url = 'https://' + settings['host'] + '/'
    debugoutput(arguments['-d'], url)

    decoded = settings['clientid'] + ':' + settings['clientsecret']
    encoded = base64.b64encode(decoded.encode('utf-8'))
    debugoutput(arguments['-d'], encoded)

    headers = {'Authorization': 'Basic ' + encoded.decode('ascii')}
    debugoutput(arguments['-d'], headers)

    authjson = apiCall(url + 'oauth/access_token?grant_type=client_credentials', 'post', headers, arguments, settings)

    authHeader = {'Authorization': 'Bearer ' + authjson['access_token']}
    debugoutput(arguments['-d'], authHeader)

    return authHeader


#Returns Requested json
def apiCall(url, verb, headers, arguments, settings):

    delay = 1
    for i in range(settings['iterations']):
        while True:
            try:
                debugoutput(arguments['-d'], url + '\n' + headers['Authorization'])
                if verb == 'get':
                    r = requests.get(url, headers=headers)
                elif verb == 'post':
                    r = requests.post(url, headers=headers)

                debugoutput(arguments['-d'], 'Status Code: ' + str(r.status_code) )

                if r.status_code != 200:
                    r.raise_for_status()
                else:
                    debugoutput(arguments['-d'], r.json())
                    return r.json()

            except requests.exceptions.ConnectionError as e:
                outputting(arguments['-q'], arguments['-o'], 'Could not Connect to Halo Instance. \nCheck your settings.yaml and try again.')
                quit()
            except requests.exceptions.HTTPError as e:
                outputting(arguments['-q'], arguments['-o'], str(e) + ' \nCheck your settings.yaml and try again.')
                quit()
            except requests.exceptions.URLRequired:
                outputting(arguments['-q'], arguments['-o'], 'The URL is incorrectly formed. \nCheck your settings.yaml and try again.')
                quit()
            except requests.exceptions.TooManyRedirects:
                outputting(arguments['-q'], arguments['-o'], 'Too many redirects to be healthy.  Bravely giving up.')
                quit()
            except requests.exceptions.Timeout:
# In the case of a timeout, this will retry.  But it will add time to each retry, it doesn't do the retries so quickly.
                attempts = settings['iterations'] - i
                outputting(arguments['-q'], arguments['-o'], 'The request timed due to network or server problems.  Trying {0} more times.'.format(attempts))
                polling_time = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
                outputting(arguments['-q'], arguments['-o'], "{0}.  Napping for {1} seconds.".format(polling_time, delay))
                time.sleep(delay)
                delay *= 2
                continue
            break
