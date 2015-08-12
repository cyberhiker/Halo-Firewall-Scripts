__author__ = 'Chris Burton'

import json
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


ZoneFile = '/Users/cburton/Downloads/20150708-FW-Zone-Dump.json'
RuleFile = '/Users/cburton/Downloads/20150708-FW-Rule-Dump.json'

Zones = open(ZoneFile)
ZoneData = json.load(Zones)

Rules = open(RuleFile)
decoder = JSONDecoder(object_pairs_hook=parse_object_pairs)
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
