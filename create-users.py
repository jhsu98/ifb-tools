import argparse
from ifb import IFB
import json
import string
from secrets import choice
import random
from prettytable import PrettyTable

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--server', dest='servername', help='iFormBuilder server name (ie. app.iformbuilder.com)')
    parser.add_argument('--client-id', dest='client_id', help='Client ID from iFormBuilder API App')
    parser.add_argument('--client-secret', dest='client_secret', help='Client Secret from iFormBuilder API App')
    parser.add_argument('--profile-id', dest='profile_id', help='Profile ID for Pages')

    args = parser.parse_args()
    server = args.servername or ""
    client_id = args.client_id or ""
    client_secret = args.client_secret or ""
    profile_id = args.profile_id or ""
    filename = args.file or ""

    # Load JSON file
    if filename.split(".")[-1].lower().strip() == "json":
        try:
            f = open(filename)
            data = json.load(f)
        except Exception as e:
            print(e)
            exit()
    else:
        print("Selected file is not valid JSON...exiting")
        exit()

    createUsers(IFB(server,client_id,client_secret),profile_id,data)

def createUsers(ifb,profile_id,data):
    users = []
    for i in range(len(data)):
        user = {}
        user['username'] = data[i]['username'] if 'username' in data[i].keys() else None
        user['password'] = ifb.genPassword()
        user['first_name'] = data[i]['first_name'] if 'first_name' in data[i].keys() else None
        user['last_name'] = data[i]['last_name'] if 'last_name' in data[i].keys() else None
        user['email'] = data[i]['email'] if 'email' in data[i].keys() else None
        
        if user['username'] != None and user['email'] != None:
            users.append(user)

    print("Attempting to create %s users..." % len(users))
    response = ifb.createUsers(profile_id,users)

    t = PrettyTable(['Status','Username','Password','ID'])

    for i in range(len(users)):
        if 'id' in response[i].keys():
            t.add_row(['✓',users[i]['username'],users[i]['password'],response[i]['id']])
        else:
            t.add_row(['✘',users[i]['username'],'',''])

    print(t)

if __name__ == "__main__":
    main()