#https://gist.github.com/oevans/6128188


####  PART 1 -- GET AND INSPECT TOKEN  ####

import sys, urllib

## attempt to import the "fay" module; exit if not
try:
    import fay
except:
    print "Failed to located the password module"
    sys.exit()

# Replace <USERNAME>, and <PASSWORD> with your ArcGIS Online subscription account credentials
# Using f=pjson for examples/debugging, should use f=json for scripts
username = 'johnpfay_student'
password = fay.getStudentPwd()

# parameters = urllib.urlencode({'username':username,'password':password,'client':'requestip','f':'pjson'})
parameters = urllib.urlencode({'username':username,'password':password,'client':'referer','referer':'http://www.arcgis.com','f':'pjson'})
print parameters

# See http://resources.arcgis.com/en/help/arcgis-rest-api/index.html#/Generate_Token/02r3000000m5000000/
# POST required (see doc), parameters not appended to URL, but passed separately -- use "," not "+" below
stem = 'https://www.arcgis.com/sharing/rest/generateToken?'
response = urllib.urlopen(stem, parameters).read()
print response

# Start parsing JSON response
import json
# json.loads and json.dumps take *string* inputs, which is what we have (cf. json.load, json.dump)
token = json.loads(response)['token']
print token

tokenExpires = json.loads(response)['expires']
print tokenExpires

# Convert epoch time (milliseconds) to readable local time
import time
tokenExpiresReadable = time.strftime('%Y-%m-%d %I:%M:%S %p (%Z)', time.localtime(tokenExpires/1000))
print tokenExpiresReadable


####  PART 2 -- GET AND INSPECT USER CONTENT  ####

# Reassign parameters using token
parameters = urllib.urlencode({'token':token,'f':'pjson'})
print parameters

# Request "User Content" for <USERNAME>
# See http://resources.arcgis.com/en/help/arcgis-rest-api/index.html#/User_Content/02r30000007p000000/
# If no subfolder is specified, root folder items and subfolder list are returned (see doc)
# GET request (see doc), parameters appended to URL -- use "+" not "," below
stem = 'https://www.arcgis.com/sharing/rest/content/users/' + username + '?'
print stem

userContent = urllib.urlopen(stem + parameters).read()
print userContent

print json.loads(userContent)['currentFolder']
print json.loads(userContent)['username']

# Work with folders
folders = json.loads(userContent)['folders']   # make a list of folders...each item is a dictionary
print folders

foldersPretty = json.dumps(folders, sort_keys=True, indent=4, separators=(',',': '))   # pretty printing
print foldersPretty

# List all folder names
for folder in folders:   # iterate through folder list
    print folder['title']

# ...with date created
for folder in folders:
    print folder['title'] + ' (created: ' + time.strftime('%Y-%m-%d', time.localtime(folder['created']/1000)) + ")"

# ...with '<SEARCHSTRING>' in title (replace <SEARCHSTRING> with text to search for, search is CaSe SeNsItIvE)
for folder in folders:
	if '<SEARCHSTRING>' in folder['title']:
		print folder['title']

# Work with items
items = json.loads(userContent)['items']   # make a list of items...each item is a dictionary...some keys store lists
print items

itemsPretty = json.dumps(items, sort_keys=True, indent=4, separators=(',',': '))   # pretty printing
print itemsPretty

# List all IDs of items in root folder
for item in items:
    print item['id']
    
# List titles of all web maps
for item in items:
    if item['type'] == 'Web Map':
        print item['title']

# List URLs for all hosted feature services with <SEARCHSTRING> in title
for item in items:
    if item['type'] == 'Feature Service':
        if '<SEARCHSTRING>' in item['title']:
            print item['url']


####  PART 3 -- CREATE THINGS IN MY CONTENT  ####

# Reassign parameters to include folder name
parameters = urllib.urlencode({'title':'My Folder','token':token,'f':'json'})

# Create a folder
stem = 'http://www.arcgis.com/sharing/rest/content/users/' + username + '/createFolder?'
response = urllib.urlopen(stem, parameters).read()

# Reassign parameters to include item information
parameters = urllib.urlencode({'URL':'http://storymaps.esri.com','title':'Esri Storymaps Site','type':'Web Mapping Application','tags':'story maps, Esri','token':token,'f':'json'})

# Create a new Web App Item
stem = 'http://www.arcgis.com/sharing/rest/content/users/' + username + '/addItem?'
response = urllib.urlopen(stem, parameters).read()