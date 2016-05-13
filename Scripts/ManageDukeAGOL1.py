#ManageDukeAGOL.py
#
# Description: A set of functions to manage Duke's AGOL portal
#

#REQUIRES: portalpy in the C:\Python27\ArcGIS10.2\Lib\site-packages directory
#->Info on portalpy: http://resources.arcgis.com/en/help/main/10.2/index.html#/PortalPy_module/017s000000m2000000/

# July 2014
# John.Fay@duke.edu

import sys, time
from portalpy import Portal
import pprint as pp

logAdmin = "john.fay"
if not "logPwd" in dir():
    logPwd = raw_input("Enter password: ")

def login(u,p):
    """Login to the portal account"""
    return Portal("https://dukeuniv.maps.arcgis.com", logAdmin,logPwd)

def getRoles():
    '''Roles keyed by AGOL ID'''
    roles = {}
    roles['4PQw5JGUQ3lnj2ao'] = "Gardens_Editor"
    roles['fuLRJ3lhjn9RoGH5'] = "LibraryWorkshop"
    roles['GAy5YMGQZuXU1DiK'] = "NSOEStudent"
    roles['GWAlbOXhYfnajYYW'] = "LibraryGeocode"
    roles['GzsVwPntNMjvUkhJ'] = "LibraryLimited"
    roles['n37uOUkvgXo6lRw0'] = "NSOElimited"
    roles['OaQP2pBZ7xxeqhfT'] = "ENV761Student"
    roles['P1RUEbCiCueTEX4z'] = "Facilities_Editor"
    roles['v4WSoECYlyiLKtHh'] = "LibraryTrusted"
    roles['Wqv2YfqyFjGnnYJO'] = "NSOEauthor"
    roles['XM6xDoXN3THEvZzN'] = "ENV859Student"
    roles['O3gFwOpNOXKHb1FF'] = "DUHS_limited"
    roles['org_admin'] = "org_admin"
    roles['org_publisher'] = "org_publisher"
    roles['org_user'] = "org_user"
    return roles

def listAllUsers(portal, inactive = 0, nocontent = 0):
    """Returns a list of all users"""
    users = portal.get_org_users()
    for user in users:
        if user['created'] == user['modified'] or inactive == 0:
            print user['fullName'],user['lastLogin']

def getRoleUsers(portal, role):
    """Returns a list of all users in the provdided role"""
    users = portal.get_org_users()
    #for user in users:
    
def getUserEmails(portal,inactive = 0, nocontent = 0):
    """Returns a list of all users along with emails and user roles"""
    outList = []
    for user in portal.get_org_users():
        if user['created'] <> user['modified']:
            outList.append((user['fullName'],user['email'],user['role']))
    return outList

def neverLoggedIn(portal):
    users = portal.get_org_users()
    nlUsers = []
    for user in users:
        if user['lastLogin'] == -1:
            #print user['fullName'],user['lastLogin'], user['email']
            nlUsers.append(user)
    return nlUsers
    
def generateToken(username, password, portalUrl):
    '''Retrieves a token to be used with API requests.'''
    parameters = urllib.urlencode({'username' : username,
                                   'password' : password,
                                   'client' : 'referer',
                                   'referer': portalUrl,
                                   'expiration': 60,
                                   'f' : 'json'})
    response = urllib.urlopen(portalUrl + '/sharing/rest/generateToken?',
                              parameters).read()
    try:
        jsonResponse = json.loads(response)
        if 'token' in jsonResponse:
            return jsonResponse['token']
        elif 'error' in jsonResponse:
            print jsonResponse['error']['message']
            for detail in jsonResponse['error']['details']:
                print detail
    except ValueError, e:
        print 'An unspecified error occurred.'
        print e


def getByEmail(portal, email):
    users = portal.search_users('email:'+email)
    for u in users:
        pp.pprint(u)
    return u

def deleteUser(username):
    doIt = raw_input("Delete "+username+"?")
    if doIt == "y":
        print "removing "+ username


### MAIN PROGRAM ###
print "Logging into portal"
portal = login(logAdmin,logPwd)

print "Getting role dictionary"
roles = getRoles()

#Create a file of user names
outFile = "ArcGISOnlineNames.csv"
f = open(outFile,'w')
f.write("User, Email, Role\n")
for u in allUsers:
    f.write("{},{}, {}\n".format(u[0],u[1],roles[u[2]]))
f.close()

sys.exit()

#### EXCESS CODE --- DOES NOT RUN ####
# Delete all inactive users in ENV761
users = neverLoggedIn(portal)
for user in users:
    print user['fullName'],roles[user['role']]
    

sys.exit()

#Create a file of user names
outFile = "ArcGISOnlineNames.csv"
f = open(outFile,'w')
f.write("User, Email, Role\n")
for u in allUsers:
    f.write("{},{}, {}\n".format(u[0],u[1],roles[u[2]]))
f.close()
    