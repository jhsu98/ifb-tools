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

    def getProfile(self,profile_id):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s" % (self.server,profile_id)
            get_profile = self.session.get(request)

            if get_profile.status_code == 200:
                return get_profile.json()
            else:
                return False
        except Exception as e:
            print(e)
            exit()

    def getAllProfiles(self,grammar=None):
        offset = 0
        limit = 100
        profiles = []

        try:
            while True:
                try:
                    request = "https://%s/exzact/api/v60/profiles?offset=%s&limit=%s" % (self.server,offset,limit)
                    if grammar != None:
                        request = request + "&%s" % grammar
                    get_profiles = self.session.get(request)
                except Exception as e:
                    print(e)
                    exit()
                else:
                    if len(get_profiles.json()) == 0:
                        break
                    else:
                        profiles = profiles + get_profiles.json()
                        offset = offset + limit
        except Exception as e:
            print(e)
            exit()
        else:
            return profiles

    def postUsers(self,profile_id,body):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/users" % (self.server,profile_id)
            post_users = self.session.post(request,data=json.dumps(body))
        except Exception as e:
            print(e)
            exit()
        else:
            return post_users.json()

    def getAllPages(self,profile_id,grammar=None):
        offset = 0
        limit = 100
        pages = []

        try:
            while True:
                try:
                    request = "https://%s/exzact/api/v60/profiles/%s/pages?offset=%s&limit=%s" % (self.server,profile_id,offset,limit)
                    if grammar != None:
                        request = request + "&%s" % grammar
                    get_pages = self.session.get(request)
                except Exception as e:
                    print(e)
                    exit()
                else:
                    if len(get_pages.json()) == 0:
                        break
                    else:
                        pages = pages + get_pages.json()
                        offset = offset + limit
        except Exception as e:
            print(e)
            exit()
        else:
            return pages

    def getAllOptionLists(self,profile_id,grammar=None):
        offset = 0
        limit = 100
        option_lists = []

        try:
            while True:
                try:
                    request = "https://%s/exzact/api/v60/profiles/%s/optionlists?offset=%s&limit=%s" % (self.server,profile_id,offset,limit)
                    if grammar != None:
                        request = request + "&%s" % grammar
                    get_option_lists = self.session.get(request)
                except Exception as e:
                    print(e)
                    exit()
                else:
                    if len(get_option_lists.json()) == 0:
                        break
                    else:
                        option_lists = option_lists + get_option_lists.json()
                        offset = offset + limit
        except Exception as e:
            print(e)
            exit()
        else:
            return option_lists

    def getOptionListDependencies(self,profile_id,option_list_id):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/optionlists/%s/dependencies" % (self.server,profile_id,option_list_id)
            get_option_list_dependencies = self.session.get(request)
        except Exception as e:
            print(e)
            exit()
        else:
            return get_option_list_dependencies.json()

    def deleteOptionList(self,profile_id,option_list_id):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/optionlists/%s" % (self.server,profile_id,option_list_id)
            del_option_list = self.session.delete(request)
        except Exception as e:
            print(e)
            exit()
        else:
            return del_option_list.json()

    def getAllElements(self,profile_id,page_id,grammar=None):
        offset = 0
        limit = 100
        elements = []
        
        try:
            while True:
                try:
                    request = "https://%s/exzact/api/v60/profiles/%s/pages/%s/elements?offset=%s&limit=%s" % (self.server,profile_id,page_id,offset,limit)
                    if grammar != None:
                        request = request + "&%s" % grammar
                    get_elements = self.session.get(request)
                except Exception as e:
                    print(e)
                    exit()
                else:
                    if len(get_elements.json()) == 0:
                        break
                    else:
                        elements = elements + get_elements.json()
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