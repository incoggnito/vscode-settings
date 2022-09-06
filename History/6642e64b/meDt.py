
import requests
from urllib import parse
import json
import sys


class Requestor():
    """Creates a request session and some helper functions"""

    headers = {
        "accept": "text/plain",
        "Content-Type": "application/json",
    }

    def __init__(self, url:str=""):

        self.url = url
        self.s = requests.Session()

    def _checkResponse(self, r, method: str):
        if r.status_code == 200:
            print(f"Successful {method}!")
        else:
            print(f"Failed {method}!")
            sys.exit(0)

    def login(self):
        """"Call the specific login method"""
        self.connection.login()


    # def getRequestURL(self):
    #     """get a correct url template to ask for the tokenID
    #     try to do kind of a stupid login
    #     """

    #     r = self.s.get(f"{self.url}/loginUrl", headers=self.headers, verify=verify, proxies=proxies)
    #     self.request_url = r.text

    #     # authURL, read client_id, scope, response_type, redirect_uri
    #     parsed_uri = parse.urlparse(self.request_url)
    #     self.authURL = "{u.scheme}://{u.netloc}/{u.path}".format(u=parsed_uri)
    #     self.qParams = parse.parse_qs(parse.urlsplit(r.text).query)

    #     self._checkResponse(r, "get request url")

    # def getAuthID(self):
    #     """post my login credentials to get a temporary authenthication ID"""
    #     data = {"goto": [self.request_url]}

    #     r = self.s.post(
    #         f"{self.authServer}/authenticate",
    #         params=json.dumps(data),
    #         headers=self.headers,
    #         verify=verify,
    #         proxies=proxies
    #     )

    #     self.authId = r.json()["authId"]

    #     self._checkResponse(r, "get authID")
# 
    # def getLoginMethod(self):
    #     """required to chose the login method (IWA-Login vs credentials)"""
    #     data = {
    #         "authId": self.authId,
    #         "callbacks": [
    #             {
    #                 "type": "ChoiceCallback",
    #                 "output": [
    #                     {
    #                         "name": "prompt",
    #                         "value": "Please select the authentication method",
    #                     },
    #                     {
    #                         "name": "choices",
    #                         "value": ["Login with Password", "IWA Login"],
    #                     },
    #                     {"name": "defaultChoice", "value": 0},
    #                 ],
    #                 "input": [{"name": "IDToken1", "value": "0"}],
    #             }
    #         ],
    #     }

    #     data = json.dumps(data)
    #     r = self.s.post(
    #         f"{self.authServer}/authenticate",
    #         headers=self.headers,
    #         data=data,
    #         verify=verify,
    #         proxies=proxies
    #     )
    #     self.authId = r.json()["authId"]

    #     self._checkResponse(r, "choise of login method")

    # def authenticate(self):
    #     """authentificate through the bmw server"""
    #     data = {
    #         "authId": self.authId,
    #         "callbacks": [
    #             {
    #                 "type": "TextOutputCallback",
    #                 "output": [
    #                     {"name": "message", "value": " "},
    #                     {"name": "messageType", "value": "0"},
    #                 ],
    #             },
    #             {
    #                 "type": "NameCallback",
    #                 "output": [{"name": "prompt", "value": "User Name"}],
    #                 "input": [{"name": "IDToken2", "value": self.uID}],
    #             },
    #             {
    #                 "type": "PasswordCallback",
    #                 "output": [{"name": "prompt", "value": "Password"}],
    #                 "input": [{"name": "IDToken3", "value": self.pID}],
    #             },
    #             {
    #                 "type": "ConfirmationCallback",
    #                 "output": [
    #                     {"name": "prompt", "value": ""},
    #                     {"name": "messageType", "value": 0},
    #                     {
    #                         "name": "options",
    #                         "value": ["Login", "IWA Login", "Strong Authentication"],
    #                     },
    #                     {"name": "optionType", "value": -1},
    #                     {"name": "defaultOption", "value": 0},
    #                 ],
    #                 "input": [{"name": "IDToken4", "value": "0"}],
    #             },
    #         ],
    #     }

    #     data = json.dumps(data)
    #     self.pID = ""

    #     r = self.s.post(
    #         f"{self.authServer}/authenticate",
    #         headers=self.headers,
    #         data=data,
    #         verify=verify,
    #         proxies=proxies
    #     )

    #     self._checkResponse(r, "authentification")

    #     # if r.status_code != 200:
    #     #     print("Failed authentification!")
    #     #     return False
    #     # else:
    #     #     return True

    # def getToken(self):
    #     """Get the token from the response.url

    #     Returns:
    #         [type]: [description]
    #     """
    #     r = self.s.get(self.request_url, headers=self.headers, verify=verify, proxies=proxies)

    #     self._checkResponse(r, "get token method")

    #     self.token = r.url.split("id_token=")[1]

    #     self.BearerHeaders = {
    #         "accept": "application/json",
    #         "Authorization": f"Bearer {self.token}",
    #     }

    # def getFromQuery(self, query, headers=None):

    #     if headers == None:
    #         headers = self.BearerHeaders

    #     r = self.s.get(f"{self.url}{query}", headers=self.BearerHeaders, verify=verify, proxies=proxies)
    #     return r

    # def postQuery(self, query: str, data: dict):

    #     headers = self.BearerHeaders
    #     headers["Content-Type"] = "application/json"
    #     self.headers = headers

    #     data = json.dumps(data)
    #     self.data = data
    #     r = self.s.post(
    #         f"{self.url}{query}",
    #         headers=self.BearerHeaders,
    #         data=data,
    #         # cert=()
    #         verify=verify,
    #         proxies=proxies
    #     )

    #     if r.status_code == 200:
    #         return "Sucessfull Post!"
    #     else:
    #         print(r.text)

    # def getWikiList(self):
    #     l = self.getFromQuery("/wiki").json()["data"]
    #     for d in l:
    #         if "title" in d.keys() and "_id" in d.keys():
    #             print(d["title"], d["_id"])

    # def getWikiID(self, name="Projektnummern"):
    #     dicts = self.getFromQuery("/wiki").json()["data"]
    #     d = next(item for item in dicts if item["title"] == name)
    #     return d["_id"]

    # def searchWiki(self, wiki="Projektnummern", search="G20"):
    #     wikiID = self.getWikiID(wiki)
    #     return self.getFromQuery(f"/wiki/{wikiID}/values/find/{search}")

    # def getWiki(self, wiki="Projektnummern"):
    #     wikiID = self.getWikiID(wiki)
    #     return self.getFromQuery(f"/wiki/{wikiID}/values")

    # def getCurrentUser(self):
    #     self.currentUser = self.getFromQuery("/users/currentUser").json()["data"]["_id"]

    # def getWorkPackages(self):

    #     params = {
    #         # "contract": "5f71b7395ad3ad0015241cbd",
    #         "contract": "60bfb704d3f15e00168649ad",
    #     }

    #     r = self.s.get(
    #         f"{self.url}/alf/workPackages",
    #         headers=self.BearerHeaders,
    #         params=params,
    #         # cert=()
    #         verify=verify,
    #         proxies=proxies
    #     )

    #     return r

    # def postTicket(self, t: dict, ordertype: str):
    #     r = self.postQuery(f"/alf/tickets/{ordertype}", t)
    #     return r

    # def getTickets(self, contract: str):
    #     query = f"/alf/tickets/csv/{contract}?objectId=true"
    #     headers = self.BearerHeaders
    #     headers["accept"] = "text/csv"
    #     return self.getFromQuery(query, headers)

    # def getTickets2(self):
    #     query = "/alf/tickets"
    #     return self.getFromQuery(query)
