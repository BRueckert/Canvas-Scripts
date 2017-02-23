# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 10:45:47 2017

@author: brueckert
"""

import requests, json
from ConfigPro import base_url, api_url, token, account_id

def getTermIDs():
    '''
    Returns a dict with all active terms in the specified account.
    Each term object contains name, id, and other properties
    '''
    r = requests.get(api_url + 'accounts/' + account_id + '/terms',
            headers = {'Authorization': 'Bearer {}'.format(token)})
    d = r.json()
    
    while 'next' in r.links:
        r = requests.get(r.links["next"]["url"],
            headers = {'Authorization': 'Bearer {}'.format(token)})
        rtemp = r.json()
        d['enrollment_terms'] = d['enrollment_terms'] + rtemp['enrollment_terms']
    
    #output pretty printed
    print(json.dumps(d,sort_keys=True,indent=4))
    return d


def getCourseIDs(termID):
    '''
    Takes int termID as parameter, returns list containing course name and id     
    '''
    payload = {'enrollment_term_id':termID}
    
    r = requests.get(api_url + 'accounts/' + account_id + '/courses',
            headers = {'Authorization': 'Bearer {}'.format(token)}, params=payload)
    d = r.json()
    
    #Cycles through pages of responses and builds course object list
    while 'next' in r.links:
        r = requests.get(r.links["next"]["url"],
            headers = {'Authorization': 'Bearer {}'.format(token)})
        d = d + r.json()
    
    #Each course name and id placed into list
    courseIDs = []
    for i in d:
        temp = []
        temp.append(i['name'])
        temp.append(i['id'])
        courseIDs.append(temp)
    return courseIDs


def getUsersInCourse(courseID):
    '''
    Returns list of all users in specified course. Can access dict keywords:
    'id', 'name', 'login_id' and others.
    '''
    payload = {'enrollment_type':'student'}
    r = requests.get(api_url + '/courses/' + courseID + '/users',
            headers = {'Authorization': 'Bearer {}'.format(token)}, params=payload)
    d = r.json()
    while 'next' in r.links:
        r = requests.get(r.links["next"]["url"],
            headers = {'Authorization': 'Bearer {}'.format(token)}, params=payload)
        rtemp = r.json()
        d += rtemp
    print(json.dumps(d,sort_keys=True,indent=4))
    return d


def getOutcomeAssessmentPoints(courseID):
    '''
    Returns list of all outcome assessment points in a course. Can take an 
    optional parameter of user_id to return for specific user or list of users.
    '''
    r = requests.get(api_url + 'courses/' + courseID + '/outcome_results',
            headers = {'Authorization': 'Bearer {}'.format(token)})
    d = r.json()
    while 'next' in r.links:
        r = requests.get(r.links["next"]["url"],
            headers = {'Authorization': 'Bearer {}'.format(token)})
        rtemp = r.json()
        d['outcome_results'] += rtemp['outcome_results']
    print(json.dumps(d,sort_keys=True,indent=4))    
    return [x for x in d['outcome_results']]

def getOutcomeResults(courseID):
    '''
    Returns all outcome rollup scores --> essentially returns the LMG for a course
    in dict form. Outcomes are not tied to groups within returned data structure.
    returned dict contains three keys; "linked" which contains group data, "meta"
    which mostly we don't need, and "rollups" which contain actual users and scores.
    '''
    payload = {'include':['outcome_groups']}
    r = requests.get(api_url + 'courses/' + '1057737' + '/outcome_rollups',
            headers = {'Authorization': 'Bearer {}'.format(token)}, params=payload)
    d = r.json()
    while 'next' in r.links:
        r = requests.get(r.links["next"]["url"],
            headers = {'Authorization': 'Bearer {}'.format(token)}, params=payload)
        rtemp = r.json()
        d['rollups'] += rtemp['rollups']
    print(json.dumps(d,sort_keys=True,indent=4))
    
    return d

def getMissingAssignments(userID):
    '''
    Returns list of missing assignment names and due dates for given user
    '''
    r = requests.get(api_url + 'users/' + userID + '/missing_submissions',
            headers = {'Authorization': 'Bearer {}'.format(token)})
    d = r.json()
    
    missingList = []
    for i in d:
        tempDict = {}
        tempDict['Assignment Name'] = d[0]['name']
        tempDict['Due Date'] = d[0]['due_at']
        missingList.append(tempDict)
    
    return missingList
        

print('Done')






