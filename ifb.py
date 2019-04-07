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
            request_token.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            self.access_token = request_token.json()['access_token']
            self.session.headers.update({ 'Authorization': "Bearer %s" % self.access_token })

    ####################################
    ## PROFILE RESOURCES
    ####################################

    def postProfile(self,body):
        try:
            request = "https://%s/exzact/api/v60/profiles"
            post_profile = self.session.post(request,data=json.dumps(body))
            post_profile.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return post_profile.json()

    def getProfile(self,profile_id):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s" % (self.server,profile_id)
            get_profile = self.session.get(request)
            get_profile.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return get_profile.json()

    def getProfiles(self,grammar=None,offset=0,limit=100):
        try:
            request = "https://%s/exzact/api/v60/profiles?offset=%s&limit=%s" % (self.server,offset,limit)
            if grammar != None:
                request += "&fields=%s" % grammar
            get_profiles = self.session.get(request)
            get_profiles.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return get_profiles.json()

    def getAllProfiles(self,grammar=None):
        offset = 0
        limit = 100
        profiles = []

        while True:
            try:
                request = self.getProfiles(grammar,offset,limit)
                if len(request) == 0:
                    break
                else:
                    profiles += request
                    offset += limit
                    print("%s profiles fetched..." % len(profiles))
            except Exception as e:
                print(e)
                exit()
        
        return profiles

    def deleteProfile(self,profile_id):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s" % (self.server,profile_id)
            delete_profile = self.session.delete(request)
            delete_profile.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return delete_profile.json()

    def deleteProfiles(self,grammar=None,offset=0,limit=100):
        try:
            request = "https://%s/exzact/api/v60/profiles?offset=%s&limit=%s" % (self.server,offset,limit)
            if grammar != None:
                request += "&fields=%s" % grammar
            delete_profiles = self.session.delete(request)
            delete_profiles.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return delete_profiles.json()

    def getCompanyInfo(self,profile_id):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/company_info" % (self.server,profile_id)
            get_company_info = self.session.get(request)
            get_company_info.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return get_company_info.json()

    ####################################
    ## USER RESOURCES
    ####################################

    def postUsers(self,profile_id,body):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/users" % (self.server,profile_id)
            post_users = self.session.post(request,data=json.dumps(body))
            post_users.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return post_users.json()

    def getUser(self,profile_id,user_id):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/users/%s" % (self.server,profile_id,user_id)
            get_user = self.session.get(request)
            get_user.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return get_user.json()

    def getUsers(self,profile_id,grammar=None,offset=0,limit=100):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/users?offset=%s&limit=%s" % (self.server,profile_id,offset,limit)
            if grammar != None:
                request += "&fields=%s" % grammar
            get_users = self.session.get(request)
            get_users.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return get_users.json()

    def getAllUsers(self,profile_id,grammar=None):
        offset = 0
        limit = 100
        users = []

        while True:
            try:
                request = self.getUsers(profile_id,grammar,offset,limit)
                if len(request) == 0:
                    break
                else:
                    users += request
                    offset += limit
                    print("%s users fetched..." % len(users))
            except Exception as e:
                print(e)
                exit()

        return users

    def deleteUser(self,profile_id,user_id):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/users/%s" % (self.server,profile_id,user_id)
            delete_user = self.session.delete(request)
            delete_user.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return delete_user.json()

    def deleteUsers(self,profile_id,grammar=None,offset=0,limit=100):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/users?offset=%s&limit=%s" % (self.server,profile_id,offset,limit)
            if grammar != None:
                request += "&fields=%s" % grammar
            delete_users = self.session.delete(request)
            delete_users.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return delete_users.json()

    ####################################
    ## PAGE RESOURCES
    ####################################

    def postPage(self,profile_id,body):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/pages" % (self.server,profile_id)
            post_page = self.session.post(request,data=json.dumps(body))
            post_page.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return post_page.json()

    def getPage(self,profile_id,page_id):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/pages/%s" % (self.server,profile_id,page_id)
            get_page = self.session.get(request)
            get_page.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return get_page.json()

    def getPages(self,profile_id,grammar=None,offset=0,limit=100):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/pages?offset=%s&limit=%s" % (self.server,profile_id,offset,limit)
            if grammar != None:
                request += "&fields=%s" % grammar
            get_pages = self.session.get(request)
            get_pages.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return get_pages.json()

    def getAllPages(self,profile_id,grammar=None):
        offset = 0
        limit = 100
        pages = []

        while True:
            try:
                request = self.getPages(profile_id,grammar,offset,limit)
                if len(request) == 0:
                    break
                else:
                    pages += request
                    offset += limit
                    print("%s pages fetched..." % len(pages))
            except Exception as e:
                print(e)
                exit()

        return pages

    def deletePage(self,profile_id,page_id):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/pages/%s" % (self.server,profile_id,page_id)
            delete_page = self.session.delete(request)
            delete_page.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return delete_page.json()

    def deletePages(self,profile_id,grammar=None,offset=0,limit=100):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/pages?offset=%s&limit=%s" % (self.server,profile_id,offset,limit)
            if grammar != None:
                request += "&fields=%s" % grammar
            delete_pages = self.session.delete(request)
            delete_pages.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return delete_pages.json()

    ####################################
    ## ELEMENT RESOURCES
    ####################################

    def postElements(self,profile_id,page_id,body):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/pages/%s/elements" % (self.server,profile_id,page_id)
            post_elements = self.session.post(request,data=json.dumps(body))
            post_elements.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return post_elements.json()

    def getElement(self,profile_id,page_id,element_id):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/pages/%s/elements/%s" % (self.server,profile_id,page_id,element_id)
            get_element = self.session.get(request)
            get_element.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return get_element.json()

    def getElements(self,profile_id,page_id,grammar=None,offset=0,limit=0):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/pages/%s/elements?offset=%s&limit=%s" % (self.server,profile_id,page_id,offset,limit)
            if grammar != None:
                request += "&fields=%s" % grammar
            get_elements = self.session.get(request)
            get_elements.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return get_elements.json()

    def getAllElements(self,profile_id,page_id,grammar=None):
        offset = 0
        limit = 100
        elements = []
        
        while True:
            try:
                request = self.getElements(profile_id,page_id,grammar,offset,limit)
                if len(request) == 0:
                    break
                else:
                    elements += request
                    offset += limit
                    print("%s elements fetched..." % len(elements))
            except Exception as e:
                print(e)
                exit()

        return elements

    def deleteElement(self,profile_id,page_id,element_id):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/pages/%s/elements/%s" % (self.server,profile_id,page_id,element_id)
            delete_element = self.session.delete(request)
            delete_element.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return delete_element.json()

    def deleteElements(self,profile_id,page_id,grammar=None,offset=0,limit=0):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/pages/%s/elements?offset=%s&limit=%s" % (self.server,profile_id,page_id,offset,limit)
            if grammar != None:
                request += "&fields=%s" % grammar
            delete_elements = self.session.delete(request)
            delete_elements.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return delete_elements.json()

    ####################################
    ## OPTION LIST RESOURCES
    ####################################

    def postOptionList(self,profile_id,body):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/optionlists" % (self.server,profile_id)
            post_option_list = self.session.post(request,data=json.dumps(body))
            post_option_list.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return post_option_list.json()

    def getOptionList(self,profile_id,option_list_id):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/optionlists/%s" % (self.server,profile_id,option_list_id)
            get_option_list = self.session.get(request)
            get_option_list.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return get_option_list.json()

    def getOptionLists(self,profile_id,grammar=None,offset=0,limit=100):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/optionlists?offset=%s&limit=%s" % (self.server,profile_id,offset,limit)
            if grammar != None:
                request += "&fields=%s" % grammar
            get_option_lists = self.session.get(request)
            get_option_lists.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return get_option_lists.json()

    def getAllOptionLists(self,profile_id,grammar=None):
        offset = 0
        limit = 100
        option_lists = []

        while True:
            try:
                request = self.getOptionLists(profile_id,grammar,offset,limit)
                if len(request) == 0:
                    break
                else:
                    option_lists += request
                    offset += limit
                    print("%s option lists fetched..." % len(option_lists))
            except Exception as e:
                print(e)
                exit()
        
        return option_lists

    def deleteOptionList(self,profile_id,option_list_id):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/optionlists/%s" % (self.server,profile_id,option_list_id)
            delete_option_list = self.session.delete(request)
            delete_option_list.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return delete_option_list.json()

    def deleteOptionLists(self,profile_id,grammar=None,offset=0,limit=100):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/optionlists?offset=%s&limit=%s" % (self.server,profile_id,offset,limit)
            if grammar != None:
                request += "&fields=%s" % grammar
            delete_option_lists = self.session.delete(request)
            delete_option_lists.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return delete_option_lists.json()

    def getOptionListDependencies(self,profile_id,option_list_id):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/optionlists/%s/dependencies" % (self.server,profile_id,option_list_id)
            get_option_list_dependencies = self.session.get(request)
            get_option_list_dependencies.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return get_option_list_dependencies.json()

    ####################################
    ## OPTION RESOURCES
    ####################################

    def postOptions(self,profile_id,page_id,body):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/optionlists/%s/options" % (self.server,profile_id,page_id)
            post_options = self.session.post(request,data=json.dumps(body))
            post_options.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return post_options.json()

    def getOption(self,profile_id,option_list_id,option_id):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/optionlists/%s/options/%s" % (self.server,profile_id,option_list_id,option_id)
            get_option = self.session.get(request)
            get_option.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return get_option.json()

    def getOptions(self,profile_id,option_list_id,grammar=None,offset=0,limit=1000):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/optionlists/%s/options?offset=%s&limit=%s" % (self.server,profile_id,option_list_id,offset,limit)
            if grammar != None:
                request += "&fields=%s" % grammar
            get_options = self.session.get(request)
            get_options.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return get_options.json()

    def getAllOptions(self,profile_id,option_list_id,grammar=None):
        offset = 0
        limit = 1000
        options = []

        while True:
            try:
                request = self.getOptions(profile_id,option_list_id,grammar,offset,limit)
                if len(request) == 0:
                    break
                else:
                    options += request
                    offset += limit
                    print("%s options fetched..." % len(options))
            except Exception as e:
                print(e)
                exit()
        
        return options

    def deleteOption(self,profile_id,option_list_id,option_id):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/optionlists/%s/options/%s" % (self.server,profile_id,option_list_id,option_id)
            delete_option = self.session.delete(request)
            delete_option.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return delete_option.json()

    def deleteOptions(self,profile_id,option_list_id,grammar=None,offset=0,limit=1000):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/optionlists/%s/options?offset=%s&limit=%s" % (self.server,profile_id,option_list_id,offset,limit)
            if grammar != None:
                request += "&fields=%s" % grammar
            delete_options = self.session.delete(request)
            delete_options.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return delete_options.json()

    ####################################
    ## RECORD RESOURCES
    ####################################

    def postRecords(self,profile_id,page_id,body):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/pages/%s/records" % (self.server,profile_id,page_id)
            post_records = self.session.post(request,data=json.dumps(body))
            post_records.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return post_records.json()

    def getRecord(self,profile_id,page_id,record_id):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/pages/%s/records/%s" % (self.server,profile_id,page_id,record_id)
            get_record = self.session.get(request)
            get_record.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return get_record.json()

    def getRecords(self,profile_id,page_id,grammar=None,offset=0,limit=1000):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/pages/%s/records?offset=%s&limit=%s" % (self.server,profile_id,page_id,offset,limit)
            if grammar != None:
                request += "&fields=%s" % grammar
            get_records = self.session.get(request)
            get_records.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return get_records.json()

    def getAllRecords(self,profile_id,page_id,grammar=None):
        offset = 0
        limit = 1000
        records = []

        while True:
            try:
                request = self.getRecords(profile_id,page_id,grammar,offset,limit)
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

    def deleteRecord(self,profile_id,page_id,record_id):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/pages/%s/records/%s" % (self.server,profile_id,page_id,record_id)
            delete_record = self.session.delete(request)
            delete_record.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return delete_record.json()

    def deleteRecords(self,profile_id,page_id,grammar=None,offset=0,limit=1000):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/pages/%s/records?offset=%s&limit=%s" % (self.server,profile_id,page_id,offset,limit)
            if grammar != None:
                request += "&fields=%s" % grammar
            delete_records = self.session.delete(request)
            delete_records.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return delete_records.json()

if __name__ == "__main__":
    pass