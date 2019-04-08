import argparse
from ifb import IFB
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import shutil
import os
import pprint

def main(ifb,profile_id,page_id):
    page_name = ifb.readPage(profile_id,page_id)['name']

    print("Retrieving form structure...")
    elements = getAllMediaElements(profile_id,page_id)
    fields = buildGrammar(elements,False)

    print("Retrieving records...")
    records = ifb.readAllRecords(profile_id,page_id,fields)

    print("Downloading images...")
    downloadImages(records,page_name)

    print("Script complete!")

def getAllMediaElements(profile_id,page_id):
    dcns = []

    elements = ifb.readAllElements(profile_id,page_id,"name,data_type((=\"11\")|(=\"18\")|(=\"28\")),data_size")

    for i in range(len(elements)):
        if elements[i]['data_type'] == 18:
            temp = {}
            temp[elements[i]['name']] = getAllMediaElements(profile_id,elements[i]['data_size'])
            if len(temp[elements[i]['name']]) > 0:
                dcns.append(temp)
        else:
            dcns.append(elements[i]['name'])

    return dcns

def buildGrammar(structure,meta=True):
    fields = "" if meta == False else "id,parent_record_id,parent_page_id,parent_element_id,created_date,created_by,created_location,created_device_id,modified_date,modified_by,modified_location,modified_device_id,server_modified_date,"

    for i in range(len(structure)):
        if isinstance(structure[i],dict):
            key = next(iter(structure[i]))
            fields += key + "[%s]," % buildGrammar(structure[i][key],meta)
        else:
            fields += structure[i] + ","

    return fields.rstrip(',')

def downloadImages(records,page_name):
    try:
        os.makedirs(page_name)
    except FileExistsError:
        pass

    for i in range(len(records)):
        for key in records[i]:
            if isinstance(records[i][key],list):
                downloadImages(records[i][key],"%s/%s" % (page_name,key))
            elif key != "id" and records[i][key] is not None:
                r = requests.get(records[i][key],verify=False, stream=True)
                r.raw.decode_content = True
                with open("%s/%s_%s.jpg" % (page_name,records[i]['id'],key),'wb') as f:
                    shutil.copyfileobj(r.raw,f)

if __name__ == "__main__":
    # Define arguments for server, client-id, and client-secret
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--server', dest='servername', help='iFormBuilder server name (ie. app.iformbuilder.com)')
    parser.add_argument('--client-id', dest='client_id', help='Client ID from iFormBuilder API App')
    parser.add_argument('--client-secret', dest='client_secret', help='Client Secret from iFormBuilder API App')
    parser.add_argument('--profile-id', dest='profile_id', help='Profile ID for Pages')
    parser.add_argument('--page-id', dest='page_id', help='Page ID to Add Elements')

    # Use empty strings to hard-code values
    args = parser.parse_args() 
    server = args.servername or ""
    client_id = args.client_id or ""
    client_secret = args.client_secret or ""

    ifb = IFB(server,client_id,client_secret)

    if args.profile_id == None:
        print('Retrieving Profiles for Server: %s' % server)
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
        print("Retrieving Pages for Profile: %s..." % selected_profile)
        pages = ifb.readAllPages(selected_profile,"id,name,label")

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

    # Pass IFB Object to main()
    main(ifb,selected_profile,selected_page)