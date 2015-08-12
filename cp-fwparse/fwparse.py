#!/usr/bin/python3
#
__author__ = 'Chris Burton'

doc = """
Usage:
  fwparse.py [-o FILE]
  fwparse.py (-h | --help)
  fwparse.py (-v | --version)

Options:
  -o FILE   Output to a specified file.
  -h --help     Show this screen.
  -v --version  Show version.

"""

import json
import func
import requests
import yaml
from collections import OrderedDict
from json import JSONDecoder
from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(doc, version='0.1')
    #print(arguments)

settings = yaml.load(open("settings.yml", 'r'))
url = 'https://' + settings['host'] + '/v1/'

authHeader = func.authenticate()

Policies = requests.get(url + 'firewall_policies', headers=authHeader)
print(str(Policies.json()))
PolicyData = Policies.json()

if PolicyData['count'] == 0:
    print('No Policies Available.')
    quit()

MyLine = 'Name|Source IP(s)|Description|Application Name|Direction|Action|Service Name|Port|Protocol'
print (MyLine)

for s in PolicyData['firewall_policies']:
    policyID = s['id']
    zoneID = ''

    for zone in s['used_by']:
        try:
            zoneID = str(s['used_by'][0]['id'])
        except IndexError:
            pass
    print(zoneID)

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

            print(MyLine)
