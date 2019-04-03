import argparse
from ifb import IFB

parser = argparse.ArgumentParser(description='')

parser.add_argument('--server', dest='servername', help='iFormBuilder server name (ie. app.iformbuilder.com)')
parser.add_argument('--client-id', dest='client_id', help='Client ID from iFormBuilder API App')
parser.add_argument('--client-secret', dest='client_secret', help='Client Secret from iFormBuilder API App')

args = parser.parse_args()

server = args.servername
client_id = args.client_id
client_secret = args.client_secret

## DEBUGGING LINE TO HARDCODE API APP INFO
# server = ''
# client_id = ''
# client_secret = ''

ifb = IFB(server,client_id,client_secret)

print('Retrieving Profiles...')
profiles = ifb.getAllProfiles()

profile_dict = {}

print('Listing Profiles: ')
for profile in profiles:
    if profile['id'] != 1:
        print("[%s] %s" % (profile['id'],profile['name']))
        profile_dict[profile['id']] = profile['name']
    
selected_profile = int(input('Select Profile ID: ').strip())
if selected_profile == 1 or selected_profile not in profile_dict:
    print('Invalid Profile ID...exiting')
    exit()

print("Retrieving Option Lists for %s..." % profile_dict[selected_profile])
option_lists = ifb.getAllOptionLists(selected_profile)

print('Deleting Option Lists with Zero Dependencies...')
num_deleted = 0
for option_list in option_lists:
    if len(ifb.getOptionListDependencies(selected_profile,option_list['id'])) == 0:
        print("[%s] %s has no dependencies, deleting..." % (option_list['id'],option_list['name']))
        ifb.deleteOptionList(selected_profile,option_list['id'])
        num_deleted = num_deleted + 1

print("Script complete, deleted %s Option Lists" % num_deleted)