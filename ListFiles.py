
#Script to grab and list all files within a course
#and print the total number of files

import requests
from ConfigPro import api_url, token

r = requests.get(api_url + 'courses/' + courseID + '/files/', 
	headers = {'Authorization': 'Bearer ' + '%s' % token})
	
data = r.json()
while 'next' in r.links:
	r = requests.get(r.links["next"]["url"],headers = {'Authorization': 'Bearer ' + '%s' % token})
	data = data + r.json()

myFiles = []
for i in data:
	addMe = i['display_name']
	myFiles.append(addMe)
	
for j in myFiles:
	print (j)

print('\nTotal # of Files: ' + str(len(myFiles)))

