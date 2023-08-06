import json
import requests
from base64 import b64encode


class ZoomClient:
    def __init__(self, accountID, clientID, secret):
        self.accountID = accountID
        self.clientID = clientID
        self.secret = secret
        self.baseUrl = "https://api.zoom.us/v2"

        authorizationBytes = bytes(f'{clientID}:{secret}', "utf-8")
        Base64Authorization = b64encode(authorizationBytes).decode("ascii")
        url = "https://zoom.us/oauth/token?grant_type=account_credentials&account_id=HDo_H5JWQAu25KIIQfo1EA"
        payload = ""
        headers = {
            'Authorization': f'Basic {Base64Authorization}',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            accessToken = response.json()['access_token']
            self.accessToken = accessToken
        else:
            raise Exception(f'{response.text}')

    def listPlanDetails(self):
        url = f"{self.baseUrl}/phone/plans"
        payload = {}
        headers = {
            'Authorization': f'Bearer {self.accessToken}'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()

    def getUser(self, userID):
        url = f"{self.baseUrl}/users/{userID}"
        payload = {}
        headers = {
            'Authorization': f'Bearer {self.accessToken}'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()

    def getPhoneUser(self, userID):
        url = f"{self.baseUrl}/phone/users/{userID}"
        payload = {}
        headers = {
            'Authorization': f'Bearer {self.accessToken}'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()

    def assignCallingPlan(self, userID, callingPlanType):
        url = f"{self.baseUrl}/phone/users/{userID}/calling_plans"
        payload = json.dumps({
            "calling_plans": [
                {
                    "type": callingPlanType
                }
            ]
        })
        headers = {
            'Authorization': f'Bearer {self.accessToken}',
            'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()

    def addBYOC(self, carrier, phoneNumbers, sipGroupID, siteID):
        """
        :param carrier: Carrier name within Zoom.
        :param phoneNumbers: List of DIDs in e164 format to add.
        :param sipGroupID: ID of Zoom SIP Group to assign numbers to.
        :param siteID: ID of site to assign numbers to.
        :type carrier: str
        :type phoneNumbers: list
        :type sipGroupID: str
        :type siteID: str
        :return:
        """
        url = f"{self.baseUrl}/phone/byoc_numbers"
        payload = json.dumps({
            "carrier": carrier,
            "phone_numbers": phoneNumbers,
            "sip_group_id": sipGroupID,
            "site_id": siteID
        })
        headers = {
            'Authorization': f'Bearer {self.accessToken}',
            'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()

    def updateUserExtension(self, userID, extension):
        url = f"{self.baseUrl}/phone/users/{userID}"

        payload = json.dumps({
            "extension_number": extension
        })
        headers = {
            'Authorization': f'Bearer {self.accessToken}',
            'Content-Type': 'application/json',
        }

        response = requests.request("PATCH", url, headers=headers, data=payload)
        return response.json()

    def assignPhoneNumber(self, userID, phoneNumber):
        """
        :param userID: ID of user to assign number to
        :param phoneNumber: DID to assign to user in e164 format. Ex: +14805551234
        :return:
        """
        url = f'{self.baseUrl}/phone/users/{userID}/phone_numbers'
        payload = json.dumps({
            "phone_numbers": [{
                "number": phoneNumber
            }]
        })

        headers = {
            'Authorization': f'Bearer {self.accessToken}',
            'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()


