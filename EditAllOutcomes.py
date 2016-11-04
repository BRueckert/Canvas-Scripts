# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 11:39:56 2016

@author: brueckert
"""

import requests, json
from ConfigPro import base_url, api_url, token

courseID = ''  #ENTER YOUR COURSE ID

#get outcome group ids
print('Getting group ids')
r = requests.get(api_url + 'courses/' + courseID + '/outcome_groups',
	headers = {'Authorization': 'Bearer ' + '%s' % token})

d = r.json()

##Optional output to see what you grabbed
#print(json.dumps(d,sort_keys=True,indent=2))

groupIDs = []
for i in d:
    k = i['id']
    groupIDs.append(k)

print('Getting outcome URLs and updating settings')
for i in groupIDs:
    #get outcome list in each group
    r = requests.get(api_url + 'courses/' + courseID + '/outcome_groups/' + str(i) + '/outcomes',
        headers = {'Authorization': 'Bearer ' + '%s' % token})
    d = r.json()
    
    #Another option json dump to see what you grabbed
    #print(json.dumps(d,sort_keys=True,indent=2))
    
    #Gets all of the outcome URLs needed for editing
    outcomeURLs = []
    for j in d:
        k = j['outcome']['url']
        outcomeURLs.append(k)
    
    #update outcomes to decaying average with 65% calc int
    #in current group list using URLs retrieved above
    for q in outcomeURLs:
        payload = {'calculation_method':'decaying_average','calculation_int':'65'}
        putURL = base_url + q
        r = requests.put(putURL, headers = {'Authorization': 'Bearer ' + '%s' % token}, json = payload)

print('Done')

    
    
