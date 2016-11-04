
#Script to add indicated user as an observer of another user

import requests
from ConfigPro import base_url, api_url, account_id, token

#User ID for Observer
userID = ''

#ID for Observee
observeeID = ''



def deleteObservee(userID, observeeID, token):
	r = requests.delete(api_url + 'users/' + userID + '/observees/' + observeeID,
                     headers = {'Authorization': 'Bearer ' + '%s' % token})
	return r


def addObservee(userID, observeeID, token):
	r = requests.put(api_url + 'users/' + userID + '/observees/' + observeeID,
	headers = {'Authorization': 'Bearer ' + '%s' % token})
	
	return r
	
d = addObservee(userID, observeeID, token)