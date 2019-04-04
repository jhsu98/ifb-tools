import argparse
from ifb import IFB
import json
from collections import OrderedDict
import string
from secrets import choice
import random
from prettytable import PrettyTable

parser = argparse.ArgumentParser(description='')

parser.add_argument('--server', dest='servername', help='iFormBuilder server name (ie. app.iformbuilder.com)')
parser.add_argument('--client-id', dest='client_id', help='Client ID from iFormBuilder API App')
parser.add_argument('--client-secret', dest='client_secret', help='Client Secret from iFormBuilder API App')
parser.add_argument('--profile-id', dest='profile_id', help='Profile ID for Pages')

args = parser.parse_args()

server = args.servername
client_id = args.client_id
client_secret = args.client_secret

## DEBUGGING LINE TO HARDCODE API APP INFO
# server = ''
# client_id = ''
# client_secret = ''

ifb = IFB(server,client_id,client_secret)

def genPassword():
    alphabet = string.ascii_letters
    uppercase = string.ascii_uppercase
    numbers = string.digits
    specials = "!@#$%^&"

    password = ''.join(choice(specials))
    password += ''.join(choice(numbers))
    password += ''.join(choice(uppercase))
    password += ''.join(choice(alphabet) for i in range(5))

    return ''.join(random.sample(password,len(password)))

if args.profile_id == None:
    print('Retrieving Profiles...')
    profiles = ifb.getAllProfiles()

    profile_dict = {}

    print('Listing Profile(s): ')
    for profile in profiles:
        if profile['id'] != 1:
            print("[%s] %s" % (profile['id'],profile['name']))
            profile_dict[profile['id']] = profile['name']
        
    selected_profile = int(input('Select Profile ID: ').strip())
    if selected_profile == 1 or selected_profile not in profile_dict:
        print('Invalid Profile ID...exiting')
        exit()
else:
    selected_profile = args.profile_id

profile = ifb.getProfile(selected_profile)

# Load JSON file
filename = input("Select the JSON file to load: ")
if filename.split(".")[-1].lower() == "json":
    try:
        f = open(filename)
        data = json.load(f,object_pairs_hook=OrderedDict)
    except Exception as e:
        print(e)
        exit()
    else:
        users = []
        for i in range(len(data)):
            user = {}
            user['username'] = data[i]['username'] if 'username' in data[i].keys() else None
            user['password'] = genPassword()
            user['first_name'] = data[i]['first_name'] if 'first_name' in data[i].keys() else None
            user['last_name'] = data[i]['last_name'] if 'last_name' in data[i].keys() else None
            user['email'] = data[i]['email'] if 'email' in data[i].keys() else None
            
            if user['username'] != None and user['email'] != None:
                users.append(user)
        
        print("Attempting to create %s users..." % len(users))
        response = ifb.postUsers(selected_profile,users)
        
        t = PrettyTable(['Status','Username','Password','ID'])

        for i in range(len(users)):
            if 'id' in response[i].keys():
                t.add_row(['✓',users[i]['username'],users[i]['password'],response[i]['id']])
            else:
                t.add_row(['✘',users[i]['username'],'',''])

        # print("Script complete, %s out of %s users created" % (created_count,len(users)))
        print(t)
else:
    print("Selected file is not valid JSON...exiting")
    exit()