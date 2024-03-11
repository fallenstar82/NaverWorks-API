import requests
import pprint
class UserManage:

    # Default Variable
    # memberId     : str          # Match -m
    # domainId     : int          # Match -d
    # displayCount : int          # Match -n
    # pageCursor   : str          # Match -c
    # displayAll   : bool         # Match -all
    # jsonFormat   : bool         # Match -j

    accessToken  : str
    __url = "https://www.worksapis.com/v1.0/users"

    def __init__(self, token : str):
        self.accessToken = token

    def queryUser(self, memberId : str, domainId : int, displayCount : int, pageCursor : str):
        headers = {
            "Authorization": "Bearer " + self.accessToken
        }

        if memberId != None:
            self.__url = self.__url + "/" + memberId
            result = requests.get(self.__url, headers = headers).json()
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

