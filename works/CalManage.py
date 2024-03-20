import requests
import pprint
class CalManage:

    accessToken  : str
    __url = "https://www.worksapis.com/v1.0"
        
    def __init__(self, token : str):
        self.accessToken = token

    def queryCalendar(self, isPersonal : bool, isShare : bool, memberId : str, calId : str, cursor : str):
        headers = {
            "Authorization": "Bearer " + self.accessToken
        }

        if isPersonal:
            if calId == None and memberId != None:
                url = self.__url + "/users/"+memberId+"/calendar-personals"
            elif calId != None and memberId != None:
                url = self.__url + "/users/" + memberId + "/calendar-personals/" + calId
            else:
                return {"error" : "Personal Calendar Must set member ID. Calendar ID is Optional."}
        elif isShare:
            if calId == None and memberId != None:
                url = self.__url + "/users/" + memberId + "/calendar"
            elif calId != None and memberId == None:
                url = self.__url + "/calendars/" + calId
            else:
                return {"error" : "Share Calendar needs only one of Member ID or Calendar ID"}
        else:
            return {"error": "You should have designate Personal or Shared calendar"}

        params = {
            "cursor" : cursor
        }

        result = requests.get(url, headers = headers, params = params).json()

        return result

