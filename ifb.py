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

    def readAccessToken(self):
        try:
            request = "https://%s/exzact/api/v60/token" % (self.server)
            get_access_token = self.session.get(request)
            get_access_token.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return get_access_token.json()

    ####################################
    ## PROFILE RESOURCES
    ####################################

    def createProfile(self,body):
        try:
            request = "https://%s/exzact/api/v60/profiles" % self.server
            post_profile = self.session.post(request,data=json.dumps(body))
            post_profile.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return post_profile.json()

    def readProfile(self,profile_id):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s" % (self.server,profile_id)
            get_profile = self.session.get(request)
            get_profile.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return get_profile.json()

    def readProfiles(self,grammar=None,offset=0,limit=100):
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

    def readAllProfiles(self,grammar=None):
        offset = 0
        limit = 100
        profiles = []

        while True:
            try:
                request = self.readProfiles(grammar,offset,limit)
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

    def updateProfile(self,profile_id,body):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s" % (self.server,profile_id)
            put_profile = self.session.put(request,data=json.dumps(body))
            put_profile.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return put_profile.json()

    def readCompanyInfo(self,profile_id):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/company_info" % (self.server,profile_id)
            get_company_info = self.session.get(request)
            get_company_info.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return get_company_info.json()

    def updateCompanyInfo(self,profile_id,body):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/company_info" % (self.server,profile_id)
            put_company_info = self.session.put(request,data=json.dumps(body))
            put_company_info.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return put_company_info.json()

    ####################################
    ## USER RESOURCES
    ####################################

    def createUsers(self,profile_id,body):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/users" % (self.server,profile_id)
            print(body)
            post_users = self.session.post(request,data=json.dumps(body))
            post_users.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return post_users.json()

    def readUser(self,profile_id,user_id):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/users/%s" % (self.server,profile_id,user_id)
            get_user = self.session.get(request)
            get_user.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return get_user.json()

    def readUsers(self,profile_id,grammar=None,offset=0,limit=100):
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

    def readAllUsers(self,profile_id,grammar=None):
        offset = 0
        limit = 100
        users = []

        while True:
            try:
                request = self.readUsers(profile_id,grammar,offset,limit)
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

    def updateUser(self,profile_id,user_id,body):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/users/%s" % (self.server,profile_id,user_id)
            put_user = self.session.put(request,data=json.dumps(body))
            put_user.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return put_user.json()

    def updateUsers(self,profile_id,body,grammar=None,offset=0,limit=100):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/users?offset=%s&limit=%s" % (self.server,profile_id,offset,limit)
            if grammar != None:
                request += "&fields=%s" % grammar
            put_users = self.session.put(request,data=json.dumps(body))
            put_users.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return put_users.json()

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

    def createPage(self,profile_id,body):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/pages" % (self.server,profile_id)
            post_page = self.session.post(request,data=json.dumps(body))
            post_page.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return post_page.json()

    def readPage(self,profile_id,page_id):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/pages/%s" % (self.server,profile_id,page_id)
            get_page = self.session.get(request)
            get_page.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return get_page.json()

    def readPages(self,profile_id,grammar=None,offset=0,limit=100):
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

    def readAllPages(self,profile_id,grammar=None):
        offset = 0
        limit = 100
        pages = []

        while True:
            try:
                request = self.readPages(profile_id,grammar,offset,limit)
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

    def updatePage(self,profile_id,page_id,body):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/pages/%s" % (self.server,profile_id,page_id)
            put_page = self.session.put(request,data=json.dumps(body))
            put_page.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return put_page.json()

    def updatePages(self,profile_id,body,grammar=None,offset=0,limit=100):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/pages?offset=%s&limit=%s" % (self.server,profile_id,offset,limit)
            if grammar != None:
                request += "&fields=%s" % grammar
            put_pages = self.session.put(request,data=json.dumps(body))
            put_pages.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return put_pages.json()

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

    def createElements(self,profile_id,page_id,body):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/pages/%s/elements" % (self.server,profile_id,page_id)
            post_elements = self.session.post(request,data=json.dumps(body))
            post_elements.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return post_elements.json()

    def readElement(self,profile_id,page_id,element_id):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/pages/%s/elements/%s" % (self.server,profile_id,page_id,element_id)
            get_element = self.session.get(request)
            get_element.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return get_element.json()

    def readElements(self,profile_id,page_id,grammar=None,offset=0,limit=0):
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

    def readAllElements(self,profile_id,page_id,grammar=None):
        offset = 0
        limit = 100
        elements = []
        
        while True:
            try:
                request = self.readElements(profile_id,page_id,grammar,offset,limit)
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

    def updateElement(self,profile_id,page_id,element_id,body):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/pages/%s/elements/%s" % (self.server,profile_id,page_id,element_id)
            put_element = self.session.put(request,data=json.dumps(body))
            put_element.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return put_element.json()

    def updateElements(self,profile_id,page_id,body,grammar=None,offset=0,limit=100):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/pages/%s/elements?offset=%s&limit=%s" % (self.server,profile_id,page_id,offset,limit)
            if grammar != None:
                request += "&fields=%s" % grammar
            put_elements = self.session.put(request,data=json.dumps(body))
            put_elements.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return put_elements.json()

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

    def createOptionList(self,profile_id,body):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/optionlists" % (self.server,profile_id)
            post_option_list = self.session.post(request,data=json.dumps(body))
            post_option_list.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return post_option_list.json()

    def readOptionList(self,profile_id,option_list_id):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/optionlists/%s" % (self.server,profile_id,option_list_id)
            get_option_list = self.session.get(request)
            get_option_list.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return get_option_list.json()

    def readOptionLists(self,profile_id,grammar=None,offset=0,limit=100):
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

    def readAllOptionLists(self,profile_id,grammar=None):
        offset = 0
        limit = 100
        option_lists = []

        while True:
            try:
                request = self.readOptionLists(profile_id,grammar,offset,limit)
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

    def updateOptionList(self,profile_id,option_list_id,element_id,body):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/optionlists/%s" % (self.server,profile_id,option_list_id)
            put_option_list = self.session.put(request,data=json.dumps(body))
            put_option_list.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return put_option_list.json()

    def updateOptionLists(self,profile_id,body,grammar=None,offset=0,limit=100):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/optionlists?offset=%s&limit=%s" % (self.server,profile_id,offset,limit)
            if grammar != None:
                request += "&fields=%s" % grammar
            put_option_lists = self.session.put(request,data=json.dumps(body))
            put_option_lists.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return put_option_lists.json()

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

    def readOptionListDependencies(self,profile_id,option_list_id):
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

    def createOptions(self,profile_id,page_id,body):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/optionlists/%s/options" % (self.server,profile_id,page_id)
            post_options = self.session.post(request,data=json.dumps(body))
            # post_options.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return post_options.json()

    def readOption(self,profile_id,option_list_id,option_id):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/optionlists/%s/options/%s" % (self.server,profile_id,option_list_id,option_id)
            get_option = self.session.get(request)
            get_option.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return get_option.json()

    def readOptions(self,profile_id,option_list_id,grammar=None,offset=0,limit=1000):
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

    def readAllOptions(self,profile_id,option_list_id,grammar=None):
        offset = 0
        limit = 1000
        options = []

        while True:
            try:
                request = self.readOptions(profile_id,option_list_id,grammar,offset,limit)
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

    def updateOption(self,profile_id,option_list_id,option_id,element_id,body):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/optionlists/%s/options/%s" % (self.server,profile_id,option_list_id,option_id)
            put_option = self.session.put(request,data=json.dumps(body))
            put_option.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return put_option.json()

    def updateOptions(self,profile_id,option_list_id,body,grammar=None,offset=0,limit=1000):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/optionlists/%s/options?offset=%s&limit=%s" % (self.server,profile_id,option_list_id,offset,limit)
            if grammar != None:
                request += "&fields=%s" % grammar
            put_options = self.session.put(request,data=json.dumps(body))
            put_options.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return put_options.json()

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

    def createRecords(self,profile_id,page_id,body):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/pages/%s/records" % (self.server,profile_id,page_id)
            post_records = self.session.post(request,data=json.dumps(body))
            post_records.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return post_records.json()

    def readRecord(self,profile_id,page_id,record_id):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/pages/%s/records/%s" % (self.server,profile_id,page_id,record_id)
            get_record = self.session.get(request)
            get_record.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return get_record.json()

    def readRecords(self,profile_id,page_id,grammar=None,offset=0,limit=1000):
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

    def readAllRecords(self,profile_id,page_id,grammar=None):
        offset = 0
        limit = 1000
        records = []

        while True:
            try:
                request = self.readRecords(profile_id,page_id,grammar,offset,limit)
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

    def updateRecord(self,profile_id,page_id,record_id,body):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/pages/%s/records/%s" % (self.server,profile_id,page_id,record_id)
            put_record = self.session.put(request,data=json.dumps(body))
            put_record.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return put_record.json()

    def updateRecords(self,profile_id,page_id,body,grammar=None,offset=0,limit=1000):
        try:
            request = "https://%s/exzact/api/v60/profiles/%s/pages/%s/records?offset=%s&limit=%s" % (self.server,profile_id,page_id,offset,limit)
            if grammar != None:
                request += "&fields=%s" % grammar
            put_records = self.session.put(request,data=json.dumps(body))
            put_records.raise_for_status()
        except Exception as e:
            print(e)
            exit()
        else:
            return put_records.json()

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