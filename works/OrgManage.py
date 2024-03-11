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

