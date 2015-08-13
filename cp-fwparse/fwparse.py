#!/usr/bin/python
__author__ = 'Chris Burton'

import json
import string
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

# Establish File Names
ZoneFile = '/Users/cburton/Dropbox/20150708-FW-Zone-Dump.json'
RuleFile = '/Users/cburton/Dropbox/20150708-FW-Rule-Dump.json'

# Open Zone File
Zones = open(ZoneFile).read()
ZoneData = json.loads(Zones)

decoder = JSONDecoder(object_pairs_hook=parse_object_pairs)

# Open Rules File
Rules = open(RuleFile).read()
RuleData = decoder.decode(Rules)

# Print Header
print('Name|Destination IP(s)|Description|Application Name|Direction|Action|Service Name|Port|Protocol|Source')

# Cycle through the Zones
for s in ZoneData['firewall_zones']:
    zoneID = ''

    # See if the Zone is used, then don't investigate
    try:
        zoneID = str(s['used_by'][0]['id'])
    except IndexError:
        pass

    # If the ZoneID is empty then the Zone is not in use
    if zoneID != '':

        # Loop through the Active Zones
        for key, policy in RuleData.items():
            ruleID = policy['id']
            name = policy['name']

            # Match the Zone to the Rule
            if zoneID == ruleID:

                # Loop through the rules for this Zone
                for rule in policy['firewall_rules']:

                    try:
                        MyLine = s['name'] + '|' + s['ip_address'] + '|' + \
                                 str(s['description']).replace('|',' ').replace('\r', ' ').replace('\n', ' ') + '|' + \
                                 name + '|' + \
                                 rule['chain'] + '|' + \
                                 rule['action'] + '|' + \
                                 rule['firewall_service']['name'] + '|' + \
                                 rule['firewall_service']['port'] + '|' + \
                                 rule['firewall_service']['protocol'] + '|' + \
                                 rule['firewall_source']['name']
                                 #rule['firewall_source']['name'] + '|' + \

                        # Print out the Results
                        print(MyLine)

                    except TypeError:
                        pass

                    except KeyError:
                        pass
