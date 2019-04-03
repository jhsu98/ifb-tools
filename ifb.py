import time
import jwt
import json
import requests

class IFB():

    def __init__(self,server,client_id,client_secret):
        self.server = server
        self.client_id = client_id
        self.client_secret = client_secret

        self.access_token = None
        self.session = requests.Session()
        self.session.headers.update({ 'Content-Type': 'application/json' })

        try:
            self.requestAccessToken()
        except Exception as e:
            print(e)
            exit()

    def requestAccessToken(self):
        try:
            token_endpoint = "https://%s/exzact/api/oauth/token" % self.server
            jwt_payload = {
                'iss': self.client_id,
                'aud': token_endpoint,
                'iat': time.time(),
                'exp': time.time() + 300
            }

            encoded_jwt = jwt.encode(jwt_payload,self.client_secret,algorithm='HS256')
            token_body = {
                'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                'assertion': encoded_jwt 
            }

            request_token = requests.post(token_endpoint,data=token_body,timeout=5)

            self.access_token = request_token.json()['access_token'] if request_token.status_code == 200 else None
        
        except Exception as e:
            print(e)
        else:
            self.session.headers.update({ 'Authorization': "Bearer %s" % self.access_token })

if __name__ == "__main__":
    pass