import argparse
from ifb import IFB

def main(ifb,profile_id,page_id):
    print("Retrieving Elements for %s..." % page_id)
    elements = ifb.readAllElements(profile_id,page_id)

    elements_list = []
    for element in elements:
        elements_list.append(element['name'])

    print("Preparing Built-In Functions for %s..." % page_id)
    built_in_functions = {}
    built_in_functions['server_name'] = 'iformbuilder.serverName'
    built_in_functions['profile_id'] = 'iformbuilder.profileID'
    built_in_functions['page_id'] = 'iformbuilder.pageID'
    built_in_functions['app_name'] = 'iformbuilder.appName'
    built_in_functions['app_version'] = 'iformbuilder.appVersion'
    built_in_functions['os_type'] = 'iformbuilder.osType'
    built_in_functions['os_version'] = 'iformbuilder.osVersion'
    built_in_functions['device_model'] = 'iformbuilder.deviceModel'
    built_in_functions['device_language'] = 'iformbuilder.deviceLanguage'

    elements_post_body = []
    for key in built_in_functions:
        if key in elements_list:
            print("Skipping %s, already exists" % key)
        else:
            elements_post_body.append({ 'name':key,'label':key,'data_type':33,'dynamic_value':built_in_functions[key],'condition_value':'false','reference_id_1':'ELEMENT_SKIP_REPORT' })

    if len(elements_post_body) > 0:
        print("Posting Built-In Functions for %s..." % page_id)
        ifb.createElements(profile_id,page_id,elements_post_body)
    else:
        print("No elements to add...exiting")
        exit()

    print("Script complete, elements added")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--server', dest='servername', help='iFormBuilder server name (ie. app.iformbuilder.com)')
    parser.add_argument('--client-id', dest='client_id', help='Client ID from iFormBuilder API App')
    parser.add_argument('--client-secret', dest='client_secret', help='Client Secret from iFormBuilder API App')
    parser.add_argument('--profile-id', dest='profile_id', help='Profile ID for Pages')
    parser.add_argument('--page-id', dest='page_id', help='Page ID to Add Elements')

    args = parser.parse_args()
    server = args.servername or ""
    client_id = args.client_id or ""
    client_secret = args.client_secret or ""

    ifb = IFB(server,client_id,client_secret)

    if args.profile_id == None:
        print('Retrieving Profiles...')
        profiles = ifb.readAllProfiles()

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

    if args.page_id == None:
        print("Retrieving Pages for %s..." % selected_profile)
        pages = ifb.readAllPages(selected_profile,"fields=id,name,label")

        pages_dict = {}

        print('Listing Page(s): ')
        for page in pages:
            print("[%s] %s" % (page['id'],page['label']))
            pages_dict[page['id']] = page['label']

        selected_page = int(input('Select Profile ID: ').strip())
        if selected_page not in pages_dict:
            print('Invalid Page ID...exiting')
            exit()
    else:
        selected_page = args.page_id

    main(ifb,selected_profile,selected_page)