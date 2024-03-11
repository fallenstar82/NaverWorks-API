import requests
import pprint
class CalManage:

    accessToken  : str
    __url = ""
        
    def __init__(self, token : str):
        self.accessToken = token

    def queryCalendar(self, isPersonal : bool, isShare : bool, memberId : str, calId : str, cursor : str):
        headers = {
            "Authorization": "Bearer " + self.accessToken
        }

        if isPersonal:
            if calId == None and memberId != None:
                self.__url="https://www.worksapis.com/v1.0/users/"+memberId+"/calendar-personals"
            elif calId != None and memberId != None:
                self.__url="https://www.worksapis.com/v1.0/users/"+memberId+"/calendar-personals/"+calId
            else:
                print("Personal Calendar Must set member ID. Calendar ID is Optional.")
                exit(1)
        elif isShare:
            if calId == None and memberId != None:
                self.__url="https://www.worksapis.com/v1.0/users/"+memberId+"/calendar"
            elif calId != None and memberId == None:
                self.__url="https://www.worksapis.com/v1.0/calendars/"+calId
            else:
                print("Share Calendar needs only one of Member ID or Calendar ID")
                exit(1)
        else:
            print("You should have designate Personal or Shared calendar")
            exit(1)

        params = {
            "cursor" : cursor
        }

        result = requests.get(self.__url, headers = headers, params = params).json()

        if 'code' in result:
            pprint.pprint(result, indent=2)
            exit(1)

        return result

