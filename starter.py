import argparse
from ifb import IFB

def main(ifb):
    print(ifb.access_token)

if __name__ == "__main__":
    # Define arguments for server, client-id, and client-secret
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--server', dest='servername', help='iFormBuilder server name (ie. app.iformbuilder.com)')
    parser.add_argument('--client-id', dest='client_id', help='Client ID from iFormBuilder API App')
    parser.add_argument('--client-secret', dest='client_secret', help='Client Secret from iFormBuilder API App')

    # Use empty strings to hard-code values
    args = parser.parse_args() 
    server = args.servername or ""
    client_id = args.client_id or ""
    client_secret = args.client_secret or ""

    ifb = IFB(server,client_id,client_secret)

    # Pass IFB Object to main()
    main(ifb)