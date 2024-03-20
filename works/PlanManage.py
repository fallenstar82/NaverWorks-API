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
            return { "error" : "Out of range of date or wrong type. : ex) 2024-03" }, None
        
        startDateString = targetYearMonth+"-01"
        startDateTime   = datetime.datetime.strptime(startDateString, '%Y-%m-%d')
        endDateTime = startDateTime + relativedelta(months=1) - relativedelta(days=1)
        endDateString = endDateTime.strftime("%Y-%m-%d") + "T23:59:59%2B09:00"
        startDateString += "T00:00:00%2B09:00"
        return startDateString, endDateString

    def addPlan(self, memberId : str, summary : str, start : dict, end : dict, calendarId : str = None, eventId : str = None, location : str = None,
                map : dict = None, mapUrl : dict = None, categoryId : str = None, organizer : dict = None, recurrence : list = [],
                recurringEventId : str = None, transparency : str = "OPAQUE", visibility :str = "PUBLIC", sequence : int = 0, attendees : dict = None,
                videoMeeting : dict = None, reminders : list = None, description : str = None) :
        
        if calendarId == None:  # 기본 캘린더에 일정 등록
            url = self.__url + "/" + memberId + "/calendar/events"
        else: # 접근 가능한 캘린더 지정하여 일정 등록
            url = self.__url + "/" + memberId + "/calendars/" + calendarId + "/events"
        # https://www.worksapis.com/v1.0/users/{userId}/calendar/events 기본 캘린더
        # https://www.worksapis.com/v1.0/users/{userId}/calendars/{calendarId}/events 대상 사용자가 Access 할 수 있는 캘린더에 대하여
        
        eventComponents = {
            "eventId"          : eventId,
            "summary"          : summary,
            "description"      : description,
            "location"         : location,
            "categoryId"       : categoryId,
            "start"            : start,
            "end"              : end,
            "recurrence"       : recurrence,
            "recurringEventId" : recurringEventId,
            "trnasparency"     : transparency,
            "visibility"       : visibility,
            "sequence"         : sequence,
            "attendees"        : attendees,
            "videoMeeting"     : videoMeeting,
            "reminders"        : reminders
        }
        if organizer != None:
            eventComponents["organizer"] = organizer

        if map != None:
            eventComponents["map"]

        if mapUrl != None:
            eventComponents["mapUrl"] = mapUrl

        params = {
            "eventComponents" : [
                eventComponents
            ]
        }

        headers = {
            "Authorization": "Bearer " + self.accessToken,
            "Content-Type" : "application/json"
        }

        pprint.pprint(params, indent=2, sort_dicts=False)

        result = requests.post(url=url, headers=headers, json=params).json()
        return result

    def queryPlan(self, memberId : str, calendarId : str = None, eventId : str = None, targetym : str = None):
        url = self.__url
        params = {}

        headers = {
            "Authorization": "Bearer " + self.accessToken
        }

        url += "/"+memberId
        if calendarId != None:
            url += "/calendars/"+calendarId+"/events"
            if eventId != None:
                url += "/"+eventId
            else:
                if targetym == None:
                    return { "error" : "List plan query needs target year-month.(ex: 2024-03)" }
                else:
                    dateCompile = self.splitDate(targetym)
                    if 'error' in dateCompile[0]:
                        return dateCompile[0]
                    startDate, endDate = dateCompile[0], dateCompile[1]
                    params["fromDateTime"]  = startDate
                    params["untilDateTime"] = endDate
        else:
            url += "/calendar/events"
            if eventId != None:
                url += "/"+eventId
            else:
                if targetym == None:
                    return { "error" : "List plan query needs target year-month.(ex: 2024-03)" }
                else:
                    dateCompile = self.splitDate(targetym)
                    if 'error' in dateCompile[0]:
                        return dateCompile[0]
                    startDate, endDate = dateCompile[0], dateCompile[1]
                    params["fromDateTime"]  = startDate
                    params["untilDateTime"] = endDate

        result = requests.get(url, headers = headers, params = params).json()

        if 'code' in result:
            pprint.pprint(result, indent=2)
            exit(1)

        return result

