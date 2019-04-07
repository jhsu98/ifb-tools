import argparse
from ifb import IFB
import json
import time

def main(ifb,profile_id,page_id):
    start_time = time.time()

    print("Fetching form structure...")
    structure = buildStructure(profile_id,page_id)

    print("Building field grammar...")
    fields = buildGrammar(structure,False)

    print("Fetching records...")
    data = ifb.getAllRecords(profile_id,page_id,fields)

    if len(data) > 0:
        name = "%s-%s-%s.json" % (profile_id,page_id,int(time.time()))
        print("Writing to JSON file <%s>" % name)
        with open(name,'w') as outfile:
            json.dump(data,outfile,indent=2)
    else:
        print("No data to download...")

    print("--- Script completed in %s seconds ---" % round(time.time() - start_time,2))

def buildStructure(profile_id,page_id):
    dcns = []

    elements = ifb.getAllElements(profile_id,page_id,"name,data_type,data_size")

    for i in range(len(elements)):
        if elements[i]['data_type'] in (16,17,35):
            pass
        elif elements[i]['data_type'] == 18:
            temp = {}
            temp[elements[i]['name']] = buildStructure(profile_id,elements[i]['data_size'])
            dcns.append(temp)
        else:
            dcns.append(elements[i]['name'])

    return dcns

def buildGrammar(structure,meta=True):
    fields = "id,parent_record_id,parent_page_id,parent_element_id,created_date,created_by,created_location,created_device_id,modified_date,modified_by,modified_location,modified_device_id,server_modified_date," if meta == True else ""

    for i in range(len(structure)):
        if isinstance(structure[i],dict):
            key = next(iter(structure[i]))
            fields += key + "[%s]," % buildGrammar(structure[i][key]) 
        else:
            fields += structure[i] + ","

    return fields.rstrip(',')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--server', dest='servername', help='iFormBuilder server name (ie. app.iformbuilder.com)')
    parser.add_argument('--client-id', dest='client_id', help='Client ID from iFormBuilder API App')
    parser.add_argument('--client-secret', dest='client_secret', help='Client Secret from iFormBuilder API App')
    parser.add_argument('--profile-id', dest='profile_id', help='Profile ID for Pages')
    parser.add_argument('--page-id', dest='page_id', help='Page ID to Add Elements')

    args = parser.parse_args()
    server = args.servername or "zeriontest.iformbuilder.com"
    client_id = args.client_id or ""
    client_secret = args.client_secret or ""

    ifb = IFB(server,client_id,client_secret)

    if args.profile_id == None:
        print('Retrieving Profiles for Server: %s' % server)
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

    if args.page_id == None:
        print("Retrieving Pages for Profile: %s..." % selected_profile)
        pages = ifb.getAllPages(selected_profile,"id,name,label")

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