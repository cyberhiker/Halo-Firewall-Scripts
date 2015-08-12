#!/usr/bin/python
#
__author__ = 'Chris Burton'

import json
import requests
import func
import yaml
from collections import OrderedDict
from json import JSONDecoder

stream = open("settings.conf", 'r')
settings = yaml.load(stream)

ZoneFile = '/Users/chris/Google Drive/20150708-FW-Zone-Dump.json'
RuleFile = '/Users/chris/Google Drive/20150708-FW-Rule-Dump.json'

Zones = open(ZoneFile)
ZoneData = json.load(Zones)

Rules = open(RuleFile)
decoder = JSONDecoder(object_pairs_hook=func.parse_object_pairs)
RuleData = decoder.decode(Rules.read())
#RuleData = json.load(Rules)

MyLine = 'Name|Source IP(s)|Description|Application Name|Direction|Action|Service Name|Port|Protocol'
print (MyLine)
for s in ZoneData['firewall_zones']:
    zoneID = ''

    try:
        zoneID = str(s['used_by'][0]['id'])
    except IndexError:
        pass

    if zoneID != '':
        for key, policy in RuleData.items():
            ruleID = policy['id']
            name = policy['name']

            if zoneID == ruleID:

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
                    
print(settings['host'])
