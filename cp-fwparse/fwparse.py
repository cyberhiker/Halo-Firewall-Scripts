#!/usr/bin/python3
#
__author__ = 'Chris Burton'

doc = """
Usage:
  fwparse.py [-o FILE]
  fwparse.py [-s FILE]
  fwparse.py [(-q -o FILE)]
  fwparse.py [-d]
  fwparse.py [-h]

Options:
  -o FILE     Set an output file
  -s FILE     Reference a settings file outside this directory
  -q          Quietly, must use -o
  -d          Displays Debug Output
  -h          This Screen

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
    func.debugoutput(arguments['-d'], arguments)

# Take actions based on command line arguments
if arguments['-s'] != None:
    if os.path.exists(arguments['-s']) == True:
        func.outputting(arguments['-q'], arguments['-o'], "Using Command Line Specified Settings File")
        settings = yaml.load(open(arguments['-s'], 'r'))
    else:
        func.outputting(arguments['-q'], arguments['-o'], arguments['-s'] + " does not exist.\n")
        quit()
else:
    settings = yaml.load(open("settings.yml", 'r'))

# Validate Quiet Enablement
if arguments['-q'] != None and arguments['-q'] == True :
    if arguments['-o'] == None:
        print('-o must be specified if using -q')
        quit()

# Set up the URL
url = 'https://' + settings['host'] + '/v1/'

# Get the AuthHeader and make sure we can access the API
authHeader = func.authenticate(arguments, settings)

# Make the API Call and retrieve the JSON
PolicyData = func.apiCall(url + 'firewall_policies', 'get', authHeader, arguments, settings)
func.debugoutput(arguments['-d'], str(PolicyData))

# Check to see if there is anything worth seeing.
if PolicyData['count'] == 0:
    func.outputting(arguments['-q'], arguments['-o'], 'No Policies Available.')
    quit()

ZoneData = func.apiCall(url + 'firewall_zones', 'get', authHeader, arguments, settings)

# Print a Header
MyLine = 'Source Name|Destination Zone|Destination IP(s)||Service Name|Port|Protocol|Active|Direction|Action|Description'
func.outputting(arguments['-q'], arguments['-o'], MyLine)

# Cycle through the zones to find who uses them and what they are configured for.
for s in ZoneData['firewall_zones']:
    # Clear out from previous loop
    policyID = ''

    # Set the Description for this zone and deal with the cruft inside this string
    description = str(s['description']).replace('|',' ').replace('\r', ' ').replace('\n', ' ')

    # Look to see if this zone has a policy associated with it.
    try:
        policyID = str(s['used_by'][0]['id'])
    except IndexError:
        pass

    # There isn't a policy on this zone, then we aren't going to worry about it.
    if policyID != '':

        # Make an API Call to see what the rules are for this policy
        RuleData = func.apiCall(url + 'firewall_policies/' + policyID + '/firewall_rules', 'get', authHeader, arguments, settings)

        # Cycle through the rules for this policy
        for rule in RuleData['firewall_rules']:
            ruleID = rule['id']

            # Deal with the ones that may or may not be in there.
            try:
                destinationname = rule['firewall_source']['name']
                servicename = rule['firewall_service']['name']
                serviceport = rule['firewall_service']['port']
                protocol = rule['firewall_service']['protocol']
            except KeyError:
                pass
            except TypeError:
                pass

            # Construct the line to be written
            NewLine = s['name'] + '|' + \
                    destinationname + '|' + s['ip_address'] + '|' + \
                    str(servicename)  + '|' + \
                    str(serviceport) + '|' + \
                    str(protocol) + '|' + \
                    str(rule['active']) + '|' + \
                    rule['chain'] + '|' + \
                    rule['action'] + '|' + \
                    description

            # Don't reprint if one of the other values makes the rule different
            if NewLine != MyLine:
                func.outputting(arguments['-q'], arguments['-o'], NewLine)
                MyLine = NewLine
