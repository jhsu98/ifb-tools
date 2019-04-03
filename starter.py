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