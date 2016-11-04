#Script for bulk Outcome creation in the Root Outcome Group
#Created by Brian Rueckert, October 2015

import requests, csv, json
from ConfigPro import base_url, api_url, token #Be sure to check token validity and import from correct config file.
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def build_dict(source_file, headers):
	heads = headers
	a = []
	with open(source_file, 'r') as myFile:
		r = csv.DictReader(myFile, fieldnames=heads, dialect='excel')
		for i in r:
			crit_list = []
			points = 5
			crits = ['crit1', 'crit2', 'crit3', 'crit4', 'crit5']
			for j in crits:
				temp_dict = {}
				temp_dict['description'] = i.pop(j)
				temp_dict['points'] = points
				crit_list.append(temp_dict)
				points -= 1
			i['ratings'] = crit_list
			a.append(i)
	return a

def getRootOutcomeGroup(api_url, courseID, token):
	r = requests.get(api_url + 'courses/' + str(courseID) + '/root_outcome_group',
	headers = {'Authorization': 'Bearer ' + '%s' % token})
	return r

def postOutcome(outcomePostURL, token, payload):
	r = requests.post(outcomePostURL, headers = {'Authorization': 'Bearer ' + '%s' % token}, json = payload)
	return r
	
	
course_id = input("\nEnter the course ID: ")

#Get the root Outcome Group URL to use in the POST request
print ('Getting root outcomes group from Course')
data = getRootOutcomeGroup(api_url, course_id, token).json()


#Output root outcome object info for troubleshooting purposes
print (json.dumps(data, sort_keys=True, indent=2))

outcomeURL = base_url + data['outcomes_url']

print ('Choose your source .csv file.')
Tk().withdraw()
myCSV = askopenfilename()


#VERY IMPORTANT: The values in the "heads" list must match the column data in the source csv file
#Title - name of outcome in outcomes list an learning mastery gradebook
#display_name - the name students see in their outcomes report
#mastery_points - threshold for achieving mastery
#calculation_method - how Canvas will calculate mastery. Allowed values: decaying_average, n_mastery, latest, or highest
#calculation_int - variable for calculation method. Only applies to decaying_average and n_mastery
#crit - criterion levels for rubric. If more than four are desired, add additional crit columns here and change "points" in the 
#		build_dict function to the max number of points possible

heads = ['title', 'description', 'mastery_points', 'calculation_method', 'calculation_int', 'crit1', 'crit2', 'crit3', 'crit4', 'crit5']
print ('Building dictionaries and creating new Outcomes...')
master_outcome_list = build_dict(myCSV, heads)
for i in master_outcome_list:
	payload = i
	r = postOutcome(outcomeURL, token, payload)

	#Output new Outcome data to console for troubleshooting
	#outcomeData = r.json()
	#print (json.dumps(outcomeData, sort_keys=True, indent=2))

	#Alternate output option to file for troubleshooting
	#outcomeData = r.json()
	#with open('OutcomeData.txt', 'w') as outFile:
	#	json.dump(outcomeData, outFile, sort_keys=True, indent=2)

print ('Done')


