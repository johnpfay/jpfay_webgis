#https://github.com/Esri/ago-tools

# Requires admin role.
import csv, time
from agoTools.admin import Admin

logAdmin = "john.fay"
if not "logPwd" in dir():
    logPwd = raw_input("Enter password: ")

agoAdmin = Admin('john.fay',password=logPwd) 
users = agoAdmin.getUsers()
roles = agoAdmin.getRoles()

#Make a dictionary of the roles so we can convert custom roles from their ID to their associated name.
roleLookup = {}
for role in roles:
    roleLookup[role["id"]] = role["name"]

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

moveItems('env761_jpfay','jpfay_dukeuniv')