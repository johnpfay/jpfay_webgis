# DukeAGOL.py
#
# Description: A set of functions implementing the agoTools and PortalPy packages
#  to manage Duke's AGOL accounts
#
# AgoTools Source: https://github.com/Esri/ago-tools
# PortalPy Source: http://resources.arcgis.com/en/help/main/10.2/index.html#/PortalPy_module/017s000000m2000000/
#
# May 2016
# John.Fay@duke.edu


# Requires admin role.
import csv, time
from agoTools.admin import Admin
import portalpy

# Code to easy log in (for me)
logAdmin = "john.fay"
if not "logPwd" in dir():
    logPwd = raw_input("Enter password for {}: ".format(logAdmin))

#Create agoAdmin objects
agoAdmin = Admin(username=logAdmin,portal="https://dukeuniv.maps.arcgis.com",password=logPwd)
users = agoAdmin.getUsers()
roles = agoAdmin.getRoles()

#Create the portalpy portal object
portal = portalpy.Portal(url="https://dukeuniv.maps.arcgis.com",username=logAdmin,password=logPwd)

#Make a dictionary of the roles so we can convert custom roles from their ID to their associated name.
roleLookup = {}
for role in roles:
    roleLookup[role["id"]] = role["name"]

def disableUser(username):
    doIt = raw_input("Disable "+username+"?")
    if doIt == "y":
        print "removing "+ username
        portal.disable_user(username)

def removeNullUsers():
    '''Disables accounts that have never logged in and with no items'''
    for user in users:
        #Get data user last logged in
        lastLogin = time.strftime("%Y-%m-%d",time.gmtime(user['lastLogin']/1000))
        loginYear = time.gmtime(user['lastLogin']/1000).tm_year
        #If the user never logged in (year will be before 1971)...
        if loginYear < 1971:
            #Get items for user
            items = agoAdmin.AGOLCatalog('owner:{}'.format(user['username']))
            if len(items) == 0:
                disableUser(user['username'])

def writeUserCSV():
    '''Writes user and user info to CSV file'''
    outputFile = 'users.csv'

    with open(outputFile, 'wb') as output:
        dataWriter = csv.writer(output, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # Write header row.
        dataWriter.writerow(['Full Name', 'Email', 'Username', 'Role', 'Date Created','Last Login','Disabled','Credits','Items'])
        # Write user data.
        for user in users:
            #get role name from the id. If it's not in the roles, it's one of the standard roles so just use it.
            roleID = user['role']
            roleName = roleLookup.get(roleID,roleID)
            #get items owned by the user
            items = agoAdmin.AGOLCatalog('owner:{}'.format(user['username']))
            #write to file
            dataWriter.writerow([user['fullName'].encode('utf-8'),
                                 user['email'].encode('utf-8'),
                                 user['username'].encode('utf-8'),
                                 roleName,
                                 time.strftime("%Y-%m-%d",time.gmtime(user['created']/1000)),
                                 time.strftime("%Y-%m-%d",time.gmtime(user['lastLogin']/1000)),
                                 user['disabled'],
                                 user['availableCredits'],
                                 len(items)])


def moveItems(userFrom,userTo):
    # for migrating a single account...
    print 'Copying all items from ' + userFrom + ' to ' + userTo + '...'
    agoAdmin.reassignAllUser1ItemsToUser2(userFrom, userTo)
    print

    print 'Reassigning groups owned by ' + userFrom + ' to ' + userTo + '...'
    agoAdmin.reassignAllGroupOwnership(userFrom, userTo)
    print

    print 'Adding ' + userTo + ' as a member of ' + userFrom + "'s groups..."
    agoAdmin.addUser2ToAllUser1Groups(userFrom, userTo)
    return

# moveItems('env761_jpfay','jpfay_dukeuniv')
