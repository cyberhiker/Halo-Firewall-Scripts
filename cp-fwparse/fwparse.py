#!/usr/bin/python3
#
__author__ = 'Chris Burton'

doc = """
Usage:
  fwparse.py [-o FILE]
  fwparse.py [-s FILE]
  fwparse.py [(-q -o FILE)]
  fwparse.py -d
  fwparse.py -h
  fwparse.py -v

Options:
  -o FILE     Set an output file
  -s FILE     Reference a settings file
  -d          Displays Debug Output
  -h          This Screen
  -v          Displays Version

"""

import json
import func
import os.path
import requests
import yaml
from collections import OrderedDict
from json import JSONDecoder
from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(doc, version='0.1')
    print(arguments)

if arguments['-s'] != None:
    if os.path.exists(arguments['-s']) == True:
        func.outputting(arguments['-q'], arguments['-o'], "Using Command Line Specified Settings File")
        settings = yaml.load(open(arguments['-s'], 'r'))
    else:
        func.outputting(arguments['-q'], arguments['-o'], arguments['-s'] + " does not exist.\n")
        quit()
else:
    settings = yaml.load(open("settings.yml", 'r'))

if arguments['-q'] != None and arguments['-q'] == True :
    if arguments['-o'] == None:
        print('-o must be specified if using -q')
        quit()

url = 'https://' + settings['host'] + '/v1/'

authHeader = func.authenticate(arguments)

Policies = requests.get(url + 'firewall_policies', headers=authHeader)
func.debugoutput(arguments['-d'], str(Policies.json()))
PolicyData = Policies.json()

if PolicyData['count'] == 0:
    func.outputting(arguments['-q'], arguments['-o'], 'No Policies Available.')
    quit()

MyLine = 'Name|Source IP(s)|Description|Application Name|Direction|Action|Service Name|Port|Protocol'
func.outputting(arguments['-q'], arguments['-o'], MyLine)

for s in PolicyData['firewall_policies']:
    policyID = s['id']
    zoneID = ''

    for zone in s['used_by']:
        try:
            zoneID = str(s['used_by'][0]['id'])
        except IndexError:
            pass
    func.debugoutput(arguments['-d'], zoneID)

    Rules = requests.get(url + 'firewall_policies/'+ policyID + '/firewall_rules', headers=authHeader)
    RuleData = json.loads(Rules.json())

    for key, policy in RuleData.items():
        ruleID = policy['id']
        name = policy['name']

        for rule in policy['firewall_rules']:
            try:
                MyLine = s['name'] + '|' + s['ip_address'] + '|' + \
                         str(s['description']).replace('|',' ').strip() + '|' + \
                         name + '|' + \
                         rule['chain'] + '|' + \
                         rule['action'] + '|' + \
                         rule['firewall_service']['name'] + '|' + \
                         rule['firewall_service']['port'] + '|' + \
                         rule['firewall_service']['protocol']
            except TypeError:
                pass
                #print('Type Error: ' + str(rule))
            except KeyError:
                pass

            func.outputting(arguments['-q'], arguments['-o'], MyLine)
