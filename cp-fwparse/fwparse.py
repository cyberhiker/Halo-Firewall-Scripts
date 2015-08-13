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

# Print a Header
MyLine = 'Name|Source IP(s)|Description|Application Name|Direction|Action|Service Name|Port|Protocol'
func.outputting(arguments['-q'], arguments['-o'], MyLine)

# Cycle through the policies to find who uses them and what they are configured for.
for s in PolicyData['firewall_policies']:
    policyID = s['id']
    zoneID = ''

    for zone in s['used_by']:
        try:
            zoneID = str(s['used_by'][0]['id'])
        except IndexError:
            pass
    func.debugoutput(arguments['-d'], zoneID)

# Make an API Call to see what the rules are for this policy
    RuleData = func.apiCall(url + 'firewall_policies/'+ policyID + '/firewall_rules', 'get', authHeader, arguments, settings)
    func.debugoutput(arguments['-d'], RuleData)

# Cycle through the rules for this policy
    for rule in RuleData['firewall_rules']:
        ruleID = rule['id']
        comment = rule['comment']

        ZoneData = func.apiCall(url + 'firewall_policies/'+ policyID + '/firewall_rules', 'get', authHeader, arguments, settings)
        func.debugoutput(arguments['-d'], ZoneData)
# Examine each rule and begin constructing the line item for it.
        try:
            MyLine = s['name'] + '|' + s['ip_address'] + '|' + \
                     str(s['description']).replace('|',' ').strip() + '|' + \
                     comment + '|' + \
                     rule['chain'] + '|' + \
                     rule['action'] + '|' + \
                     rule['firewall_service']['name'] + '|' + \
                     rule['firewall_service']['port'] + '|' + \
                     rule['firewall_service']['protocol']
            func.outputting(arguments['-q'], arguments['-o'], MyLine)

# Catch the errors, but then move on.
        except TypeError:
            pass
            print('Type Error: ' + str(rule))
            quit()

# Output the result
        func.outputting(arguments['-q'], arguments['-o'], MyLine)
