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
            exit()
        else:
            self.session.headers.update({ 'Authorization': "Bearer %s" % self.access_token })

    def getAllProfiles(self,grammar=None):
        try:
            offset = 0
            limit = 100
            profiles = []

            while True:
                try:
                    request = "https://%s/exzact/api/v60/profiles?offset=%s&limit=%s" % (self.server,offset,limit)
                    if grammar != None:
                        request = request + "&%s" % grammar
                    request_profiles = self.session.get(request)
                except Exception as e:
                    print(e)
                    exit()
                else:
                    if len(request_profiles.json()) == 0:
                        break
                    else:
                        profiles = profiles + request_profiles.json()
                        offset = offset + limit
        except Exception as e:
            print(e)
            exit()
        else:
            return profiles

    def getAllPages(self,profile_id,grammar=None):
        try:
            offset = 0
            limit = 100
            pages = []

            while True:
                try:
                    request = "https://%s/exzact/api/v60/profiles/%s/pages?offset=%s&limit=%s" % (self.server,profile_id,offset,limit)
                    if grammar != None:
                        request = request + "&%s" % grammar
                    request_pages = self.session.get(request)
                except Exception as e:
                    print(e)
                    exit()
                else:
                    if len(request_pages.json()) == 0:
                        break
                    else:
                        pages = pages + request_pages.json()
                        offset = offset + limit
        except Exception as e:
            print(e)
            exit()
        else:
            return pages

    def getAllElements(self,profile_id,page_id,grammar=None):
        try:
            offset = 0
            limit = 100
            elements = []

            while True:
                try:
                    request = "https://%s/exzact/api/v60/profiles/%s/pages/%s/elements?offset=%s&limit=%s" % (self.server,profile_id,page_id,offset,limit)
                    if grammar != None:
                        request = request + "&%s" % grammar
                    request_elements = self.session.get(request)
                except Exception as e:
                    print(e)
                    exit()
                else:
                    if len(request_elements.json()) == 0:
                        break
                    else:
                        elements = elements + request_elements.json()
                        offset = offset + limit
        except Exception as e:
            print(e)
            exit()
        else:
            return elements

    def postElements(self,profile_id,page_id,body):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/pages/%s/elements" % (self.server,profile_id,page_id)
            post_elements = self.session.post(request,data=json.dumps(body))
        except Exception as e:
            print(e)
            exit()
        else:
            return post_elements.json()

if __name__ == "__main__":
    pass