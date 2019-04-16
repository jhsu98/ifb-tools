import argparse
from ifb import IFB
from prettytable import PrettyTable

def formSearch(ifb,form_name):
    profiles = ifb.readAllProfiles()

    t = PrettyTable(['Profile ID','Profile Name','Page ID','Form Name','Form Label'])

    for i in range(len(profiles)):
        print("Searching in %s..." % profiles[i]['name'])
        pages = ifb.readPages(profiles[i]['id'],"name(~\"%25"+form_name+"%25\"),label")

        if len(pages) > 0:
            for j in range(len(pages)):
                t.add_row([profiles[i]['id'],profiles[i]['name'],pages[j]['id'],pages[j]['name'],pages[j]['label']])

    print("Search results for <%s>:" % form_name)
    print(t)

def main():
    # Define arguments for server, client-id, and client-secret
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--server', dest='servername', help='iFormBuilder server name (ie. app.iformbuilder.com)')
    parser.add_argument('--client-id', dest='client_id', help='Client ID from iFormBuilder API App')
    parser.add_argument('--client-secret', dest='client_secret', help='Client Secret from iFormBuilder API App')
    parser.add_argument('--form-name', dest='form_name', help='iFormBuilder Form Name')

    # Use empty strings to hard-code values
    args = parser.parse_args() 
    server = args.servername or "zeriontest.iformbuilder.com"
    client_id = args.client_id or "3d34ee4e781d7e4750ff2c73df96cf70102d05df"
    client_secret = args.client_secret or "af69c4801d49204d76aa7d30f6e7357494bbef33"
    form_name = args.form_name or ""

    formSearch(IFB(server,client_id,client_secret),form_name)

if __name__ == "__main__":
    main()