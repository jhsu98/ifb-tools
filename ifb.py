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

    ####################################
    ## TOKEN RESOURCES
    ####################################

    def requestAccessToken(self):
        """Create JWT and request iFormBuilder Access Token
        If token is successfully returned, stored in session header
        Else null token is stored in session header
        """
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

    ####################################
    ## PROFILE RESOURCES
    ####################################

    def getProfile(self,profile_id):
        """GET request for single profile
        
        Arguments:
            profile_id {int} -- iFormBuilder profile
        
        Returns:
            dict -- Decoded JSON object with profile information
        """
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
        """GET requests for all profiles, fields returned specified in grammar
        
        Keyword Arguments:
            grammar {string} -- iFormBuilder field grammar (default: {None})
        
        Returns:
            list -- Decoded array of JSON objects
        """
        offset = 0
        limit = 100
        profiles = []

        try:
            while True:
                try:
                    request = "https://%s/exzact/api/v60/profiles?offset=%s&limit=%s" % (self.server,offset,limit)
                    if grammar != None:
                        request += "&fields=%s" % grammar
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

    ####################################
    ## USER RESOURCES
    ####################################

    def getUsers(self,profile_id):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/users?limit=1" % (self.server,profile_id)
            get_users = self.session.post(request)
        except Exception as e:
            print(e)
            exit()
        else:
            return get_users

    def postUsers(self,profile_id,body):
        """POST request to create users in a given profile
        
        Arguments:
            profile_id {int} -- iFormBuilder profile id
            body {list|dict} -- List of dictionaries, minimum username/password/email
        
        Returns:
            list|dict -- Decoded Array of JSON objects or single object
        """
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/users" % (self.server,profile_id)
            post_users = self.session.post(request,data=json.dumps(body))
        except Exception as e:
            print(e)
            exit()
        else:
            return post_users.json()

    ####################################
    ## PAGE RESOURCES
    ####################################

    def getAllPages(self,profile_id,grammar=None):
        """GET request for all pages in a given profile, fields returned specified by grammar
        
        Arguments:
            profile_id {int} -- iFormBuilder profile id
        
        Keyword Arguments:
            grammar {string} -- iFormBuilder field grammar (default: {None})
        
        Returns:
            list -- Decoded Array of JSON objects
        """
        offset = 0
        limit = 100
        pages = []

        try:
            while True:
                try:
                    request = "https://%s/exzact/api/v60/profiles/%s/pages?offset=%s&limit=%s" % (self.server,profile_id,offset,limit)
                    if grammar != None:
                        request += "&fields=%s" % grammar
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

    ####################################
    ## OPTION LIST RESOURCES
    ####################################

    def getAllOptionLists(self,profile_id,grammar=None):
        """GET request for all Option Lists in a given profile, fields returned specified by grammar
        
        Arguments:
            profile_id {int} -- iFormBuilder profile id
        
        Keyword Arguments:
            grammar {string} -- iFormBuilder field grammar (default: {None})
        
        Returns:
            list -- Decoded Array of JSON objects
        """
        offset = 0
        limit = 100
        option_lists = []

        try:
            while True:
                try:
                    request = "https://%s/exzact/api/v60/profiles/%s/optionlists?offset=%s&limit=%s" % (self.server,profile_id,offset,limit)
                    if grammar != None:
                        request += "&fields=%s" % grammar
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
        """GET request for dependencies of a given Option List
        Dependencies are Elements where the Option List is assigned
        
        Arguments:
            profile_id {int} -- iFormBuilder profile id
            option_list_id {int} -- iFormBuilder option list id
        
        Returns:
            list -- Decoded Array of JSON objects
        """
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/optionlists/%s/dependencies" % (self.server,profile_id,option_list_id)
            get_option_list_dependencies = self.session.get(request)
        except Exception as e:
            print(e)
            exit()
        else:
            return get_option_list_dependencies.json()

    def deleteOptionList(self,profile_id,option_list_id):
        """DELETE request for a single option list
        
        Arguments:
            profile_id {int} -- iFormBuilder profile id
            option_list_id {int} -- iFormBuilder option list id
        
        Returns:
            dict -- Decoded JSON object
        """
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/optionlists/%s" % (self.server,profile_id,option_list_id)
            del_option_list = self.session.delete(request)
        except Exception as e:
            print(e)
            exit()
        else:
            return del_option_list.json()

    ####################################
    ## ELEMENT RESOURCES
    ####################################

    def getAllElements(self,profile_id,page_id,grammar=None):
        """GET request for all elements in a specified page, fields returned by specified grammar
        
        Arguments:
            profile_id {int} -- iFormBuilder profile id
            page_id {int} -- iFormBuilder page id
        
        Keyword Arguments:
            grammar {string} -- iFormBuilder field grammar (default: {None})
        
        Returns:
            list -- Decoded Array of JSON objects
        """
        offset = 0
        limit = 100
        elements = []
        
        try:
            while True:
                try:
                    request = "https://%s/exzact/api/v60/profiles/%s/pages/%s/elements?offset=%s&limit=%s" % (self.server,profile_id,page_id,offset,limit)
                    if grammar != None:
                        request += "&fields=%s" % grammar
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
        """POST request to add elements to a given page
        
        Arguments:
            profile_id {int} -- iFormBuilder profile id
            page_id {int} -- iFormBuilder page id
            body {list|dict} -- List of dictionaries or single dictionary to be added to page
        
        Returns:
            list -- Decoded Array of JSON objects
        """
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/pages/%s/elements" % (self.server,profile_id,page_id)
            post_elements = self.session.post(request,data=json.dumps(body))
        except Exception as e:
            print(e)
            exit()
        else:
            return post_elements.json()

    ####################################
    ## RECORD RESOURCES
    ####################################

    def getRecord(self,profile_id,page_id,record_id):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/pages/%s/records/%s" % (self.server,profile_id,page_id,record_id)
            get_record = self.session.get(request)
        except Exception as e:
            print(e)
            exit()
        else:
            return get_record.json()

    def getRecords(self,profile_id,page_id,grammar=None,limit=100,offset=0):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/pages/%s/records?offset=%s&limit=%s" % (self.server,profile_id,page_id,offset,limit)
            if grammar != None:
                request += "&fields=%s" % grammar
            get_records = self.session.get(request)
        except Exception as e:
            print(e)
            exit()
        else:
            return get_records.json()

    def getAllRecords(self,profile_id,page_id,grammar=None):
        offset = 0
        limit = 1000
        records = []

        print("Fetching records...")
        while True:
            try:
                request = self.getRecords(profile_id,page_id,grammar,limit,offset)

                if len(request) == 0:
                    break
                else:
                    records += request
                    offset += limit
                    print("%s records fetched..." % len(records))
            except Exception as e:
                print(e)
                exit()

        return records
        
if __name__ == "__main__":
    pass