import requests
import pprint
import datetime
from dateutil.relativedelta import relativedelta
import re
class PlanManage:

    accessToken  : str
    __url = "https://www.worksapis.com/v1.0/users"
        
    def __init__(self, token : str):
        self.accessToken = token
        
    def splitDate(self, targetYearMonth):
        checkYearMonth = re.fullmatch(
            r'^[0-9][0-9][0-9][0-9]\-([0][0-9]|[1][0-2])$', targetYearMonth
        )
        if checkYearMonth == None:
            print("Out of range of date or wrong type. : ex) 2024-03")
            exit(1)
        startDateString = targetYearMonth+"-01"
        startDateTime   = datetime.datetime.strptime(startDateString, '%Y-%m-%d')
        endDateTime = startDateTime + relativedelta(months=1) - relativedelta(days=1)
        endDateString = endDateTime.strftime("%Y-%m-%d") + "T23:59:59%2B09:00"
        startDateString += "T00:00:00%2B09:00"
        return startDateString, endDateString

    def queryPlan(self, memberId : str, calendarId : str, eventId : str, targetym : str):
        params = {}

        headers = {
            "Authorization": "Bearer " + self.accessToken
        }

        self.__url += "/"+memberId
        if calendarId != None:
            self.__url += "/calendars/"+calendarId+"/events"
            if eventId != None:
                self.__url += "/"+eventId
            else:
                if targetym == None:
                    print("List plan query needs target year-month.(ex: 2024-03)")
                    exit(1)
                else:
                    startDate, endDate = self.splitDate(targetym)
                    params["fromDateTime"]  = startDate
                    params["untilDateTime"] = endDate
        else:
            self.__url += "/calendar/events"
            if eventId != None:
                self.__url += "/"+eventId
            else:
                if targetym == None:
                    print("List plan query needs target year-month.(ex: 2024-03)")
                    exit(1)
                else:
                    startDate, endDate = self.splitDate(targetym)
                    params["fromDateTime"]  = startDate
                    params["untilDateTime"] = endDate
                    print(params)

        result = requests.get(self.__url, headers = headers, params = params).json()

        if 'code' in result:
            pprint.pprint(result, indent=2)
            exit(1)

        return result

