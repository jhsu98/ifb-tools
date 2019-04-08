import argparse
from ifb import IFB

def main(ifb,profile_id):
    print("Retrieving Option Lists for %s..." % profile_id)
    option_lists = ifb.readAllOptionLists(profile_id)

    print('Deleting Option Lists with Zero Dependencies...')
    num_deleted = 0
    for option_list in option_lists:
        if len(ifb.readOptionListDependencies(profile_id,option_list['id'])) == 0:
            print("[%s] %s has no dependencies, deleting..." % (option_list['id'],option_list['name']))
            ifb.deleteOptionList(profile_id,option_list['id'])
            num_deleted = num_deleted + 1

    print("Script complete, deleted %s Option Lists" % num_deleted)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--server', dest='servername', help='iFormBuilder server name (ie. app.iformbuilder.com)')
    parser.add_argument('--client-id', dest='client_id', help='Client ID from iFormBuilder API App')
    parser.add_argument('--client-secret', dest='client_secret', help='Client Secret from iFormBuilder API App')
    parser.add_argument('--profile-id', dest='profile_id', help='Profile ID of Option Lists')

    args = parser.parse_args()
    server = args.servername or ""
    client_id = args.client_id or ""
    client_secret = args.client_secret or ""

    ifb = IFB(server,client_id,client_secret)

    if args.profile_id == None:
        print('Retrieving Profiles...')
        profiles = ifb.readAllProfiles()

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
    else:
        selected_profile = args.profile_id

    main(ifb,selected_profile)