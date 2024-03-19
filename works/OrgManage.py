import requests
import pprint
class OrgManage:

    accessToken  : str
    __url = "https://www.worksapis.com/v1.0/orgunits"

    def __init__(self, token : str):
        self.accessToken = token

    def queryOrg(self, orgUnitId : str, domainId : int, displayCount : int, pageCursor : str):
        headers = {
            "Authorization": "Bearer " + self.accessToken
        }

        if orgUnitId != None:
            self.__url = self.__url + "/" + orgUnitId
            result = requests.get(self.__url, headers=headers).json()
        else:
            params = {
                "domainId" : domainId,
                "count" : displayCount,
                "cursor" : pageCursor
            }

            result = requests.get(self.__url, headers = headers, params = params).json()

            if 'code' in result:
                pprint.pprint(result, indent=2)
                exit(1)

        return result

    def addOrg(self, 
               domainId : str, 
               orgName : str, 
               sortOrder : int, 
               parentOrgId : str = None, 
               extKey : str = None, 
               orgMail : str = None, 
               aliasEmail : list = None, 
               allowSender : list = None, 
               receiveMail : bool = False, 
               useMessage : bool = False, 
               useNote : bool = False, 
               useCalendar : bool = False, 
               useTask :bool = False, 
               useFolder :bool = False, 
               useServerNotification :bool = False, 
               visibleOrg : bool = True, 
               orgDescription : str = None):
        
        headers = {
            "Authorization": "Bearer " + self.accessToken,
            "Content-Type" : "application/json"
        }

        params = {
            "domainId": domainId,
            "orgUnitName": orgName,
            "displayOrder" : sortOrder,
            "visible" : visibleOrg
        }

        # Optional Parameters Setting
        if parentOrgId:
            params["parentOrgUnitId"] = parentOrgId
        if extKey:
            params["orgUnitExternalKey"] = extKey
        if orgMail:
            params["email"] = orgMail
        if aliasEmail:
            params["aliasEmails"] = aliasEmail
        if allowSender:
            params["membersAllowedToUseOrgUnitEmailAsRecipient"] = allowSender
        if receiveMail:
            params["canReceiveExternalMail"] = receiveMail
        if useMessage:
            params["useMessage"] = True
            if useNote:
                params["useNote"] = True
            if useCalendar:
                params["useCalendar"] = True
            if useTask:
                params["useTask"] = True
            if useFolder:
                params["useFolder"] = True
        if useServerNotification:
            params["useServiceNotification"] = True
        if orgDescription:
            params["description"] = orgDescription
        
        result = requests.post(self.__url, headers=headers, json=params).json()
        return result

