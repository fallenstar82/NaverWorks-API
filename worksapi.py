import jwt
import requests
import unicodedata
import json
import pprint
import csv
import argparse
from time import time

# East Ansian Character Width
def charAlign(inputs_s, max_size, fill_char=" "):
    l = 0
    if inputs_s == None:
        return fill_char*max_size        
    for c in inputs_s:
        if unicodedata.east_asian_width(c) in ['F','W']:
            l+=2
        else:
            l+=1
    return (inputs_s+(fill_char*(max_size-l)))

# Generate Access Token using Json Web Token
def getToken(clientId, clientSecret, serviceAccount, privKey, scope, outputFile):
    header = {
        "alg":"RS256", 
        "typ":"JWT"
    }

    payload = {
        "iss": clientId,
        "sub": serviceAccount,
        "iat": int(time()),
        "exp": int(time())+3600
    }

    signed_jwt = jwt.encode(payload=payload, key=privKey, headers=header)

    params = {
        "assertion": signed_jwt,
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "client_id": clientId,
        "client_secret": clientSecret,
        "scope": scope
    }

    url = "https://auth.worksmobile.com/oauth2/v2.0/token"
    result = requests.post(url, params=params, headers=header).json()
    print(result)
    print("####################################")
    print("# Access Token Generate Info       #")
    print("####################################")
    print("Parameter Using: ")
    print(" - Service Account: " + serviceAccount)
    print(" - Client ID      : " + clientId)
    print(" - Client Secret  : " + clientSecret)
    print(" - Private Key    : Secured. " )
    print(" - OAuth Scope    : " + scope)
    print(" - Token output   : " + outputFile)
    with open(outputFile, 'w') as f:
        f.write(result["access_token"])

# Get user Info using Email
def getUserInfo(userId, domainId, count, cursor, showDeleted, AccToken, jsonFormat=False):
    header = {
        "Authorization": "Bearer " + AccToken
    } 

    url = "https://www.worksapis.com/v1.0/users"

    if userId != None:
        url = url+"/"+userId
        result = requests.get(url, headers=header).json()
    else:
        params = {
            "domainId": domainId,
            "count": count,
            "cursor": cursor,
            "orderBy": "NAME",
            "sortOrder": "ASCENDING"
        }
        result = requests.get(url, headers=header, params=params).json()
    
    if "code" in result:
        print('CODE: ' + result['code'])
        print('DESC: ' + result['description'])
    else:
        if userId != None:
            if __name__ != "__main__":
                return result
            if jsonFormat:
                pprint.pprint(result)
            else:
                print(charAlign("User ID",50) + charAlign("Email",40) + charAlign("Name",10) + charAlign("Cell Phone",30) +
                      charAlign("Pending",15) + charAlign("Suspended",15) + charAlign("Deleted",15))
                print("-"*175)
                print(charAlign(result["userId"],50) + 
                      charAlign(result["email"],40) +
                      charAlign(result["userName"]["lastName"],10) +
                      charAlign(result["cellPhone"],30) +
                      charAlign("True" if result["isPending"] == True else "False",15 ) + 
                      charAlign("True" if result["isSuspended"] == True else "Fasle",15) +
                      charAlign("True" if result["isDeleted"] == True else "False" ,15)
                      )
                # print("%-50s %-40s %-10s %-30s" % (result["userId"], result["email"], result["userName"]["lastName"], result["cellPhone"]))
                print(charAlign("---Organization Info",175,"-"))
                for orgInfo in range(0, len(result["organizations"])):
                    print("ORGANIZATION: " + result["organizations"][orgInfo]["organizationName"])
                    for orgUnitInfo in range(0, len(result["organizations"][orgInfo]["orgUnits"])): 
                        print("  ORGANIZATION UNIT    : " + result["organizations"][orgInfo]["orgUnits"][orgUnitInfo]["orgUnitName"] + (" / Main" if result["organizations"][orgInfo]["orgUnits"][orgUnitInfo]["primary"] == True else ""))
                        print("     ORGANIZATION POSITION: " + result["organizations"][orgInfo]["orgUnits"][orgUnitInfo]["positionName"])
                        print("     ORGANIZATION UNIT ID : " + result["organizations"][orgInfo]["orgUnits"][orgUnitInfo]["orgUnitId"])
        else:
            if __name__ != "__main__":
                return result
            if jsonFormat:
                print(result)
            else:
                print(charAlign("User ID", 50) +
                      charAlign("Email", 40) +
                      charAlign("User Name", 25) +
                      charAlign("Pending", 15) +
                      charAlign("Suspended", 15) +
                      charAlign("Deleted", 15))
                print("-"*160)
                for userCount in range(0,len(result["users"])):
                    
                    if result["users"][userCount]["isDeleted"] == True:
                        if showDeleted == True:
                            None
                        else:
                            continue
                    if result["users"][userCount]["userName"]["lastName"] == None and result["users"][userCount]["userName"]["firstName"] != None:
                        memberName = result["users"][userCount]["userName"]["firstName"]
                    elif result["users"][userCount]["userName"]["lastName"] != None and result["users"][userCount]["userName"]["firstName"] == None:
                        memberName = result["users"][userCount]["userName"]["lastName"]
                    else:
                        memberName = result["users"][userCount]["userName"]["lastName"] + result["users"][userCount]["userName"]["firstName"]
                    print(charAlign(result["users"][userCount]["userId"],50) +
                          charAlign(result["users"][userCount]["email"],40) +
                          charAlign(memberName, 25) +
                        #   charAlign(result["users"][userCount]["userName"]["lastName"] + result["users"][userCount]["userName"]["firstName"],25) +
                          charAlign("True" if result["users"][userCount]["isPending"] == True else "False",15) +
                          charAlign("True" if result["users"][userCount]["isSuspended"] == True else "False", 15) +
                          charAlign("True" if result["users"][userCount]["isDeleted"] == True else "False", 15)
                    )
                if result["responseMetaData"]["nextCursor"] != None:
                    print("-"*160)
                    print(" Next Cursor: " + result["responseMetaData"]["nextCursor"])

def postUserInfo(execType: str, domainId: int, extKey: str, email: str, 
                 pemail: str, firstName: str, lastName: str, cellPhone: str,
                 domainLists: list, orgUnitLists: list, isSSO: bool, 
                 passWordPolicy: str, passWord: str, AccToken: str): 
    
    header = {
        "Authorization": "Bearer " + AccToken,
        "Content-Type": "application/json"
    }

    params = {
        "domainId": domainId,
        "userExternalKey": extKey,
        "email": email,
        "privateEmail": pemail,
        "cellPhone" : cellPhone,
        "userName": {
            "lastName": lastName,
            "firstName": firstName
        }
    }

    params["organizations"] = []

    if domainLists == None:
        domainLists = [domainId]
    
    for domainList in range(0,len(domainLists)):
        if domainList == 0:
            isPrimary = True
        else:
            isPrimary = False
        params["organizations"].append(
            {
                "domainId": domainLists[domainList],
                "primary": isPrimary,
                "orgUnits": []
            }
        )

        if domainList+1 > len(orgUnitLists):
            continue

        for unitId in range(0,len(orgUnitLists[domainList])):
            params["organizations"][domainList]["orgUnits"].append(
                {
                    "orgUnitId": orgUnitLists[domainList][unitId],
                    "primary": True if unitId == 0 else False
                }
            )

    if isSSO == False: 
        if passWordPolicy == 'ADMIN':
            params["passwordConfig"] = {
                "passwordCreationType": "ADMIN",
                "password": passWord
            }
        elif passWordPolicy == 'MEMBER':
            params["passwordConfig"] = {
                "passwordCreationType": "MEMBER",
            }
        else:
            print("Password Policy not defined.")
            print("Check pasword Policy and password parameters")
            quit()
    if execType == "post":
        url = "https://www.worksapis.com/v1.0/users"
        result = requests.post(url,headers=header,json=params).json()
    elif execType == "put":
        url = "https://www.worksapis.com/v1.0/users/"+email
        result = requests.put(url,headers=header,json=params).json()
    
    if __name__ != "__main__":
        return result
    else:
        pprint.pprint(result, indent=2)

def deleteUser(userId, AccToken):
    header = {
        "Authorization": "Bearer " + AccToken
    }

    if userId == None:
        print("User Id Not defined")
    else:
        url = "https://www.worksapis.com/v1.0/users/" + userId
        result = requests.delete(url, headers=header)
        if __name__ != "__main__":
            return result.text
        else:
            print(result.text)

# Employees Type
def getEmployeesType(domainId, count, cursor, jsonFormat, AccToken):
    header = {
        "Authorization": "Bearer " + AccToken
    }

    params = {
        "domainId": domainId,
        "count" : count,
        "cursor": cursor
    }

    url = "https://www.worksapis.com/v1.0/directory/employment-types"

    result = requests.get(url, headers=header, params=params).json()
    if __name__ != "__main__":
        return result
    if jsonFormat:
        print(result)
    else:
        print(charAlign("Domain Id",20) +
              charAlign("Type Id",40) + 
              charAlign("Display Order",20) +
              charAlign("Type Name",25))
        print("-"*105)
        for empType in range(0, len(result["employmentTypes"])):
            print(charAlign(str(result["employmentTypes"][empType]["domainId"]),20) +
                  charAlign(result["employmentTypes"][empType]["employmentTypeId"],40) +
                  charAlign(str(result["employmentTypes"][empType]["displayOrder"]),20) +
                  charAlign(result["employmentTypes"][empType]["employmentTypeName"],20)
                  )
        if result["responseMetaData"]["nextCursor"] != None:
            print(charAlign("-",105))
            print("Next Cusror: " + result["responseMetaData"]["nextCursor"])
    
def postEmployeesType(domainId, displayOrder, employementTypeName, empTypeExternalKey, AccToken):
    header = {
        "Authorization": "Bearer " + AccToken,
        "Content-Type": "application/json"
    }

    params = {
        "domainId": domainId,
        "displayOrder": displayOrder,
        "employmentTypeName": employementTypeName,
        "employmentTypeExternalKey": empTypeExternalKey
    }

    url = "https://www.worksapis.com/v1.0/directory/employment-types"

    result = requests.post(url, headers=header, json=params)
    print(result.text)

# User Calendar
def getUserCalendarLists(userId, jsonFormat, nextCursor, calendarId, AccToken):
    header = {
        "Authorization": "Bearer " + AccToken
    }

    if calendarId != None:
        url = "https://www.worksapis.com/v1.0/users/" + userId + "/calendar-personals/" + calendarId
    else:
        url = "https://www.worksapis.com/v1.0/users/" + userId + "/calendar-personals"
    param=list()
    if nextCursor != None:
        param={ "cursor" : nextCursor }

    result = requests.get(url, params=param, headers=header).json()

    if __name__ != "__main__":
        return result
    
    if jsonFormat:
        pprint.pprint(result, indent=2)
    else:
        if 'code' in result:
            pprint.pprint(result, indent=2)
        else:
            if calendarId != None:
                pprint.pprint(result, indent=2)
            else:
                for calList in result["calendarPersonals"]:
                    print("%-50s : %-45s" % (calList["calendarId"], calList["calendarName"]))
                if result["responseMetaData"]["nextCursor"] != None:
                    print("Next Cursor : " + result["responseMetaData"]["nextCursor"])

def postCalendar(calendarName, members, CalindarDescription, isPublic, AccToken):
    header = {
        "Authorization": "Bearer " + AccToken,
        "Content-Type" : "application/json"
    }

    params = {
        "calendarName" : calendarName,
        "members" : [],
        "description" : CalindarDescription,
        "isPublic" : isPublic
    }

    for member in members:
        if str(member[2]).upper() not in ['CALENDAR_EVENT_READ_WRITE',
                             'EVENT_READ_WRITE',
                             'EVENT_READ',
                             'EVENT_READ_FREE_BUSY']:
            print("Calendar Role only alow one of .. " + member[2])
            print(" 'CALENDAR_EVENT_READ_WRITE','EVENT_READ_WRITE', 'EVENT_READ', 'EVENT_READ_FREE_BUSY'")
            print("Input value : " + str(member[2]).upper())
            quit()
        
        if member[1].upper() not in ['USER','GROUP','ORGUNIT']:
            print("Member Type only allow one of 'USER/GROUP/ORGUNIT'")
            print("Input value : " + str(member[1]).upper())
            quit()
        params["members"].append(
            {
                "id" : member[0],
                "type" : member[1].upper(),
                "role" : member[2].upper()
            }
        )

    url = "https://www.worksapis.com/v1.0/calendars"
    result = requests.post(url,headers=header, json=params).json()
    if __name__ != "__main__":
        return result
    pprint.pprint(result)

def deleteCalendar(calendarId, AccToken):
    header = {
        "Authorization": "Bearer " + AccToken,
    }

    url = "https://www.worksapis.com/v1.0/calendars/" + calendarId
    result = requests.delete(url,headers=header)
    if __name__ != "__main__":
        return result
    print(result)

def getCalendarInfo(calendarId, AccToken):
    header = {
        "Authorization": "Bearer " + AccToken,
    }

    url = "https://www.worksapis.com/v1.0/calendars/"+ calendarId

    result = requests.get(url,headers=header).json()
    
    if __name__ != "__main__":
        return result
    pprint.pprint(result, indent=2)

def modifyUserCalendar(userId:str, calendarId:str, isShow:bool, members:list, isPublic:bool, calDescription:str, AccToken):
    header = {
        "Authorization": "Bearer " + AccToken,
        "Content-Type" : "application/json"
    }

    if userId == None and isShow == None and members == None and isPublic == None and calDescription == None:
        print("No Change")
        quit()
    
    if userId != None:
        url = "https://www.worksapis.com/v1.0/users/" + userId + "/calendar-personals/" + calendarId
    else:
        url = "https://www.worksapis.com/v1.0/calendars/" + calendarId
    
    param = dict()
    if isShow != None:
        param["isShowOnLNBList"] = isShow
    
    if members != None:
        param["members"]=list()
        for cnt in range(0,len(members)):
            param["members"].append(
                {
                    "id" : members[cnt][0],
                    "type" : members[cnt][1],
                    "role" : members[cnt][2]
                }
            )
    if isPublic != None:
        param["isPublic"] = isPublic
    
    if calDescription != None:
        param["descripton"] = calDescription
  
    
    result=requests.patch(url, json=param, headers=header).json()
    
    if __name__ != '__main__':
        return result
    else:
        pprint.pprint(result, indent=2)

# Plan Management
def getPlanCalendar(userId, calendarId, fromDateTime, untilDateTime, jsonFormat, AccToken):
    header = {
        "Authorization": "Bearer " + AccToken
    }

    url = "https://www.worksapis.com/v1.0/users/" + userId + "/calendars/" + calendarId + "/events"

    params = {
        "fromDateTime" : fromDateTime.replace('+','%2B'),
        "untilDateTime" : untilDateTime.replace('+','%2B')
    }

    result = requests.get(url, headers=header, params=params).json()
    if __name__ != "__main__":
        return result
    pprint.pprint(result, indent=2)

def postPlanCalendar(userId:str, calendarId:str, planSummary:str, planDescription:str, eventLocation:str, planType:str, 
                     startDate:str, endDate:str, timeZone:str, attendeeList:list,
                     isRepeat:bool, repeatInterval:int, repeatFrequency:str, repeatDay:str, repeatMonth:str,
                     repeatUntil:str, repeatException:str, AccToken):
    header = {
        "Authorization" : "Bearer " + AccToken,
        "Content-Type" : "application/json"
    }

    attendees = list()
    recurrency=list()
    if isRepeat:
        repeatRule = "RRULE:"
        positionCount = 1
        if repeatInterval:
            repeatRule = repeatRule + "INTERVAL="+str(repeatInterval)
            positionCount = positionCount + 1
        if repeatFrequency:
            if positionCount > 1:
                repeatRule = repeatRule + ";"
            repeatRule = repeatRule + "FREQ=" + repeatFrequency.upper()
            positionCount = positionCount + 1
        if repeatDay:
            if positionCount > 1:
                repeatRule = repeatRule + ";"
            repeatRule = repeatRule + "BYDAY="+repeatDay.upper()
            positionCount = positionCount + 1
        if repeatMonth:
            if positionCount > 1:
                repeatRule = repeatRule + ";"
            repeatRule = repeatRule + "BYMONTH=" + repeatMonth
        if repeatUntil:
            if positionCount > 1:
                repeatRule = repeatRule + ";"
            recurrency.append(repeatRule + "UNTIL=" + repeatUntil)
        if repeatException != None and len(repeatException) > 0:
            if planType == "DATETIME":
                exceptionRule = "EXDATE;TZID=" + timeZone + ":"
            else:
                exceptionRule = "EXDATE;VALUE=DATE:"
            for x in range(0,len(repeatException)):
                exceptionRule = exceptionRule + repeatException[x]
                if x < len(repeatException) - 1:
                    exceptionRule = exceptionRule + ","
            recurrency.append(exceptionRule)

    attendees = list()
    if attendeeList:
        for attendeeNum in range(0,len(attendeeList)):
            attendees.append({
                "email": attendeeList[attendeeNum][0],
                "partstat": attendeeList[attendeeNum][1]
            }
            )

    if planType.upper() == "DATE":
        start = { "date" : startDate}
        end = {"date" : endDate}
    else:
        start = {"dateTime" : startDate, "timeZone" : timeZone}
        end = {"dateTime" : endDate, "timeZone" : timeZone}

    eventComponents = [
        {
            "summary" : planSummary,
            "description" : planDescription,
            "start" : start,
            "end" : end,
            "recurrence" : recurrency,
            "reminders" : [
                {
                    "method" : "DISPLAY",
                    "trigger" : "-P1D"
                }
            ],
            "attendees" : attendees
        }
    ]

    if eventLocation != None:
        eventComponents[0]["location"] = eventLocation

    params = {
        "eventComponents" : eventComponents
    }
    
    url = "https://www.worksapis.com/v1.0/users/" + userId + "/calendars/" + calendarId + "/events"
    # print(url)
    # pprint.pprint(params)

    result = requests.post(url,headers=header,json=params).json()
    if __name__ != "__main__":
        return result
    pprint.pprint(result, indent=2)

# Organization
def getOrganizationInfo(domainId, orgId, jsonFormat, AccToken):
    header = {
        "Authorization": "Bearer " + AccToken
    }

    url = "https://www.worksapis.com/v1.0/orgunits/" + orgId

    result = requests.get(url,headers=header).json()

    if jsonFormat:
        if 'code' in result:
            print("CODE : " + result['code'])
            print("DESC : " + result['description'])
        else:
            pprint.pprint(result, indent=2)
    else:
        print(charAlign("Organization ID", 40) +
                  charAlign("Organization Email", 50) +
                  charAlign("Organization Name", 30) +
                  charAlign("Parents Organization Id", 40)
                  )
        print("-"*160)
        print(
            charAlign(result["orgUnitId"], 40) +
            charAlign(result["email"], 50) +
            charAlign(result["orgUnitName"], 30) +
            charAlign(result["parentOrgUnitId"], 40)
        )
        

def getOraganizationLists(domainId, count, cursor, jsonFormat, AccToken):
    header = {
        "Authorization": "Bearer " + AccToken
    }

    params = {
        "domainId": domainId,
        "count": count
    }

    if cursor != None:
        params["cursor"] = cursor
    
    url = "https://www.worksapis.com/v1.0/orgunits"
    
    result = requests.get(url, headers=header, params=params).json()
    if __name__ != "__main__":
        return result
    
    if jsonFormat:
        pprint.pprint(result, indent=2)
    else:
        if 'code' in result:
            print("CODE: " + result['code'])
            print("DESC: " + result['description'])
        else:
            print(charAlign("Organization ID",40) +
                charAlign("Organization Email",50) +
                charAlign("Organization Name",30) +
                charAlign("Parents Organization ID",40) +
                charAlign("Organization Ext Key",40))
            print("-"*160)
            for orgInfo in result["orgUnits"]:
                print(charAlign(orgInfo["orgUnitId"],40) +
                    charAlign(orgInfo["email"],50) +
                    charAlign(orgInfo["orgUnitName"],30) +
                    charAlign(orgInfo["parentOrgUnitId"],40) +
                    charAlign(orgInfo["orgUnitExternalKey"],40))
            if (result["responseMetaData"]["nextCursor"] != None): 
                print("-"*160)
                print("Next Cursor Option: " + result["responseMetaData"]["nextCursor"])

def postOrganization(domainId, orgUnitName, orgEmail, externalKey, parentOrgId, displayLevel, jsonFormat, AccToken):
    header = {
        "Authorization": "Bearer " + AccToken,
        "Content-Type" : "application/json"
    }

    params = {
        "domainId": domainId,
        "orgUnitName": orgUnitName,
        "email": orgEmail,
        "parentOrgUnitId": parentOrgId,
        "displayOrder": 1,
        "orgUnitExternalKey": externalKey,
        "displayLevel": displayLevel
    }

    url = "https://www.worksapis.com/v1.0/orgunits"

    result = requests.post(url, headers=header, json=params).json()
    if __name__ != "__main__":
        return result
    
    pprint.pprint(result)

def deleteOrgnization(orgUnitId, AccToken):
    header = {
        "Authorization": "Bearer " + AccToken
    }

    url = "https://www.worksapis.com/v1.0/orgunits/" + orgUnitId

    result = requests.delete(url, headers=header)
    if __name__ != "__main__":
        return result.text
    print(result.text)
    
# Group Management
def getGroupLists(domainId :int, count :int, cursor :str, groupId :int, jsonFormat :bool, AccToken):
    header = {
        "Authorization": "Bearer " + AccToken
    }

    params = {
        "domainId": domainId,
        "count": count
    }

    if cursor != None:
        params["cursor"] = cursor

    if groupId != None: 
        url = "https://www.worksapis.com/v1.0/groups/" + groupId
    else : 
        url = "https://www.worksapis.com/v1.0/groups"

    result = requests.get(url, headers=header, params=params).json()
    
    if __name__ != "__main__":
        return result
    if 'code' not in result:
        if jsonFormat:
            pprint.pprint(result)
        else:
            if groupId == None:
                print("%-40s %-30s" % ("Group ID", "Group Name"))
                print("------------------------------------------------------------------")
                for groupInfo in result["groups"]:
                    print("%-40s %-30s" % (groupInfo["groupId"], groupInfo["groupName"]))
                if (result["responseMetaData"]["nextCursor"] != None): 
                    print("------------------------------------------------------------------")
                    print("Next Cursor Option: " + result["responseMetaData"]["nextCursor"])
            else:
                print(result["groupName"] + " (" + result["groupId"] + ")")
                print("="*50)
                print("Group Email : " + "No Emails" if result["groupEmail"] == None else result["groupEmail"]) 
                print("Group Functions : ")
                print((" Message" if result["useMessage"] else "") + 
                    (" Calendar" if result["useCalendar"] else "") +
                    (" Folder" if result["useFolder"] else "") +
                    (" Mail" if result["useMail"] else "") +
                    (" Note" if result["useNote"] else "") +
                    (" Task" if result["useTask"] else "") )
                print("Group Administrators : ")
                for admin in (result["administrators"]):
                    print("  %-40s" % (admin["userId"]))
                print("Grpup Descripton")
                print(" %s" % result["description"])
                print("---Group Members"+ "-"*40)
                for members in (result["members"]):
                    print("  %-40s - %10s" % (members["id"], members["type"]))
    else:
        print("CODE : " + result["code"])
        print("DESC : " + result["description"])

def postGroup(operationType :str, groupId :str, domainId :int, groupName :str, description :str, serviceNotification :bool,
              serviceManagement :bool, externalKey :str, administrators :list,
              useMessage :bool, useNote :bool, useCalendar :bool, useTask :bool, useFolder :bool,
              useMail :bool, groupEmail :str, members :list, jsonFormat :bool, AccToken :str ):
    
    # um 이 False 인데도 아래 Feature 를 사용하려고 하면 에러를 출력하고 종료한다.
    #  useNote, useCalendar, useTask, useFolder
    if useMessage == False:
        errCode = 0
        errFeature = ''
        if useNote == True:
            errFeature = 'useNote(--un)'
            errFeature = errFeature + 1
        if useCalendar == True:
            if errCode > 0:
                errFeature = errFeature + ', '
            errFeature = errFeature + 'useCalendar(--uc)'
            errFeature = errFeature + 1
        if useTask == True:
            if errCode > 0:
                errFeature = errFeature + ', '
            errFeature = errFeature + 'useTask(--uc)'
            errFeature = errFeature + 1            
        if useFolder == True:
            if errCode > 0:
                errFeature = errFeature + ', '
            errFeature = errFeature + 'useFolder(--uf)'
            errFeature = errFeature + 1       
        
        if errCode > 0:
            print('useMessage(--um) is Disabled. But ' + errFeature + ' feature(s) enabled.')
            print('Use --um if you want to use following features.')
            print(errFeature)
            quit()
    
    header = {
        "Authorization": "Bearer " + AccToken,
        "Content-Type" : "application/json"
    }
    
    params = {
        "domainId" : domainId,
        "groupName" : groupName,
        "description" : description,
        "useServiceNotifiction" : serviceNotification,
        "serviceManagement" : serviceManagement,
        "groupExternalKey" : externalKey,
        "administrators" : [],
        "members" : [],
        "useMessage" : useMessage,
        "useNote" : useNote,
        "useCalendar" : useCalendar,
        "useTask" : useTask,
        "useFolder" : useFolder,
        "useMail" : useMail,
        "groupEmail" : groupEmail
    }

    for adminSeq in range(0,len(administrators)):
        params["administrators"].append(
            {
                "userId" : administrators[adminSeq]
            }
        )

    for memberSeq in range(0,len(members)):
        params["members"].append(
            {
                "id" : members[memberSeq][0],
                "type" :members[memberSeq][1]
            }
        )

    result=''

    if operationType == 'Post':
        url = "https://www.worksapis.com/v1.0/groups"
        result=requests.post(url,headers=header,json=params).json()
    elif operationType == 'Adjust':
        url = "https://www.worksapis.com/v1.0/groups/" + groupId
        result=requests.put(url, headers=header, json=params).json()
    else:
        print("Unknown opartion type")
        quit()
    
    if __name__ != "__main__":
        return result
    
    if jsonFormat:
        pprint.pprint(result, indent=2)
    else:
        if 'code' in result:
            pprint.pprint(result, indent=2)
        else:
            print("Group : " + result["groupName"] + " ("+ result["groupId"] + ")")
            print('-'*150)
            print("No descriptions of this group" if result["description"] == None else result["description"])
            print('-'*150)
            print('__Administrators__')
            for cnt in range(0, len(result["administrators"])):
                print("  " + result["administrators"][cnt]["userId"])
            print("__Members__")
            for cnt in range(0, len(result["members"]), 3):
                for hcnt in range(cnt, cnt+3 if cnt+3 < len(result["members"]) else len(result["members"])):
                    print(end="  ")
                    print(charAlign(result["members"][hcnt]["id"] + "(" + result["members"][hcnt]["type"] + ")",50), end="")
                print()

def modifyGroup(domainId :int, groupId :str,  groupName :str, description :str, serviceNotification :bool,
              serviceManagement :bool, administrators :list,
              useMessage :bool, useNote :bool, useCalendar :bool, useTask :bool, useFolder :bool,
              useMail :bool, groupEmail :str, members :list, jsonFormat :bool, AccToken :str ):
    
    header = {
        "Authorization": "Bearer " + AccToken,
        "Content-Type" : "application/json"
    }

    url = "https://www.worksapis.com/v1.0/groups/" + groupId

    param = dict()

    param["domainId"] = domainId

    if groupName != None:
        param["groupname"] = groupName
    
    if description != None:
        param["description"] = description
    
    if serviceNotification != None:
        param["useServiceNotification"] = serviceNotification
    
    if administrators != None:
        param["administrators"] = list()
        for adminSeq in range(0,len(administrators)):
            param["administrators"].append(
            {
                "userId" : administrators[adminSeq]
            }
        )
            
    if members != None:
        param["members"] = list()
        for memberSeq in range(0,len(members)):
            param["members"].append(
                {
                    "id" : members[memberSeq][0],
                    "type" :members[memberSeq][1]
                }
            )

    if groupEmail != None:
        param["groupEmail"] = groupEmail

    if useMail != None:
        param["useMail"] = useMail

    if serviceManagement != None:
        param["serviceManagement"] = serviceManagement

    if useMessage != None:
        param["useMessage"] = useMessage

    if useNote != None:
        param["useNote"] = useNote

    if useCalendar != None:
        param["useCalendar"] = useCalendar

    if useTask != None:
        param["useTask"] = useTask
    
    if useFolder != None:
        param["useFolder"] = useFolder

    # pprint.pprint(param, indent=2)

    result = requests.patch(url,headers=header, json=param).json()

    if __name__ != "__main__":
        return result
    
    if jsonFormat or 'code' in result:
        pprint.pprint(result, indent=2)
    else:
        print("Group : " + result["groupName"] + " ("+ result["groupId"] + ")")
        print('-'*150)
        print("No descriptions of this group" if result["description"] == None else result["description"])
        print('-'*150)
        print('__Administrators__')
        for cnt in range(0, len(result["administrators"])):
            print("  " + result["administrators"][cnt]["userId"])
        print("__Members__")
        for cnt in range(0, len(result["members"]), 3):
            for hcnt in range(cnt, cnt+3 if cnt+3 < len(result["members"]) else len(result["members"])):
                print(end="  ")
                print(charAlign(result["members"][hcnt]["id"] + "(" + result["members"][hcnt]["type"] + ")",50), end="")
            print()

def deleteGroup(groupId, AccToken):
    header = {
        "Authorization" : "Bearer " + AccToken
    }

    url = "https://www.worksapis.com/v1.0/groups/" + groupId

    result = requests.delete(url, headers=header)
    if __name__ != "__main__":
        return result.text
    print(result.text)

def getGroupInfo(groupId, jsonFormat, AccToken):
    header = {
        "Authorization": "Bearer " + AccToken
    }

    url = "https://www.worksapis.com/v1.0/groups/" + groupId

    result = requests.get(url, headers=header).json()

    if __name__ != "__main__":
        return result

    if jsonFormat:
        pprint.pprint(result, indent=2)
    else:
        if 'code' in result:
            pprint.pprint(result, indent=2)
        else:
            print("Group : " + result["groupName"] + " ("+ result["groupId"] + ")")
            print('-'*150)
            print("No descriptions of this group" if result["description"] == None else result["description"])
            print('-'*150)
            print('__Administrators__')
            for cnt in range(0, len(result["administrators"])):
                print("  " + result["administrators"][cnt]["userId"])
            print()
            print("__Members__")
            for cnt in range(0, len(result["members"]), 3):
                for hcnt in range(cnt, cnt+3 if cnt+3 < len(result["members"]) else len(result["members"])):
                    print(end="  ")
                    print(charAlign(result["members"][hcnt]["id"] + "(" + result["members"][hcnt]["type"] + ")",50), end="")
                print()
            print()
            if result["useMessage"]:
                print("__Group Message(--um) Enabled__")
                print("   " + charAlign("Group Note     (--un) : ", 24), end="")
                print(charAlign("ENABLED" if result["useNote"] else "DISABLED", 10), end="")
                print("   " + charAlign("Group Foler    (--uf) : ", 24), end="")
                print("ENABLED" if result["useFolder"] else "DISABLED")
                print("   " + charAlign("Group Calendar (--uc) : ", 24), end="")
                print(charAlign("ENABLED" if result["useCalendar"] else "DISABLED", 10), end="")
                print("   " + charAlign("Group Task     (--ut) : ", 24), end="")
                print("ENABLED" if result["useFolder"] else "DISABLED")
            else:
                print("__Group message(--um) Disabled__")
                # useNote, useCalendar, useTask, useFolder, 

def postShareDrive(driveMasters, driveName, driveDescription, AccToken):
    header = {
        "Authorization" : "Bearer " + AccToken
    }

    url = "https://www.worksapis.com/v1.0/sharedrives"

    master = list()

    for masterCnt in range(0, len(driveMasters)):
        master.append({ "id" : driveMasters[masterCnt] })

    params = {
        "description" : driveDescription,
        "masters" : master,
        "name" : driveName
    }

    pprint.pprint(params, indent=2)

    # result = requests.post(url, headers=header, params=params).json()
    result = requests.post(url, headers=header, ).json()
    if __name__ != "__main__":
        return result
    pprint.pprint(result, indent=2)

def getShareDrive(AccToken):
    header = {
        "Authorization" : "Bearer " + AccToken
    }

    url = "https://www.worksapis.com/v1.0/sharedrives"

    result = requests.get(url,headers=header).json()
    
    if __name__ != "__main__":
        return result
    pprint.pprint(result, indent=2)

def getShareDriveList(AccToken):
    header = {
        "Authorization" : "Bearer " + AccToken
    }

    url = "https://www.worksapis.com/v1.0/sharedrives"

    result = requests.get(url, headers=header).json()

    pprint.pprint(result, indent=2)

def manageShareDriveObject(driveId :str, operationType :str, fileId :str, objectName :str, fileProperties :bool, cursor :str, jsonFormat :bool, AccToken):
    # Query / Modify 에 따른 Header 종류 추가
    # Create 는 Folder 에 한함.
    # fileId 은 fileId 와 매핑됨.
    
    header = {
        "Authorization" : "Bearer " + AccToken,
    }

    result=''
    url = "https://www.worksapis.com/v1.0/sharedrives/" + driveId + "/files"

    ## 목록 조회
    if operationType.upper() == "QUERY":
        params = {
            "orderby" : "createdTime%20desc",
            "count" : 200
        }

        if cursor != None:
            params["cursor"] = cursor

        # 루트폴더 조회
        if fileId == None:
            result = requests.get(url, headers=header, params=params).json()
        else:
            # 특정 파일에 대한 속성 조회
            if fileProperties:
                url = url + "/" + fileId
                result = requests.get(url, headers=header).json()
            # 특정 폴더에 대한 목록조회
            else:
                url = url + "/" + fileId + "/children"
                result = requests.get(url, headers=header, params=params).json()
    ## Folder 생성
    elif operationType.upper() == "CREATE":
        header["Content-Type"] =  "application/json"

        params = {
            "fileName" : objectName
        }

        # 루트 폴더에 생성
        if fileId == None:
            url = url + "/createfolder"
            result = requests.post(url, headers=header,  json=params).json()
        # 특정 폴더에 생성
        else:
            url = url + "/" + fileId + "/createfolder"
            result = requests.post(url, headers=header, json=params).json()
    ## File / Folder 삭제
    elif operationType.upper() == "REMOVE":
        url = url + "/" + fileId
        result = requests.delete(url, headers=header)
        pprint.pprint(result, indent=2)


    if __name__ != "__main__":
        return result
    
    if jsonFormat or 'code' in result:
        pprint.pprint(result, indent=2)
    elif operationType.upper() == "QUERY": # 목록 조회
        if fileProperties == None or fileProperties == False:
            print(charAlign("File Path & Name", 60), end="  ")
            print(charAlign("File Type", 10), end=" ")
            print(charAlign("File Size", 20), end=" ")
            print(charAlign("File ID", 55))
            print("-"*150)
            for cnt in range(0, len(result["files"])):
                print(charAlign(result["files"][cnt]["filePath"], 60), end="  ")
                print(charAlign(result["files"][cnt]["fileType"], 10), end=" ")
                print(charAlign(str(result["files"][cnt]["fileSize"]), 20), end=" ")
                print(charAlign(result["files"][cnt]["fileId"], 55))
            if result["responseMetaData"]["nextCursor"] != None:
                print("Next Cursor : " + result["responseMetaData"]["nextCursor"])
        else: # 파일 속성 조회
            print(charAlign("File Path & Name", 80), end="  ")
            print(charAlign("File Type", 10), end=" ")
            print(charAlign("Parent Id", 55))
            print("-"*175)
            print(charAlign(result["filePath"] + ("" if result["fileType"] == 'FOLDER' else result["fileName"]), 80), end="  ")
            print(charAlign(result["fileType"], 10), end=" ")
            print(charAlign(result["parentFileId"], 55))
    elif operationType.upper() == "CREATE":
        pprint.pprint(result, indent=2)
                

def manageShareDrivePrivs(driveId :str, operationType :str, fileId :str, permId :str, jsonFormat :bool, userId :str, privType :str, AccToken):
    # 권한이 하나의 객체로서 취급.
    # 권한 목록 조회, 특정 권한 목록 세부 조회, 권한 생성, 수정, 해제, 전부 해제, 허용, 미허용,  
    # 권한 목록 조회
    header = {
        "Authorization" : "Bearer " + AccToken,
    }

    url = "https://www.worksapis.com/v1.0/sharedrives/" + driveId + "/files/" + fileId + "/permissions"

    if operationType.upper() == "QUERY":
        if permId != None:
            url = url + "/" + permId
        result = requests.get(url, headers=header).json()
    elif operationType.upper() == "CREATE":
        header["Content-Type"] = "application/json"
        
        param = {
            "userId" : userId,
            "type" : privType.upper()
        }

        result = requests.post(url, headers=header, json=param).json()
    elif operationType.upper() == "MODIFY":
        header["Content-Type"] = "application/json"
        url = url + "/" + permId
        param = {
            "type" : privType.upper()
        }

        result = requests.patch(url, headers=header, json=param).json()
    elif operationType.upper() in ["DELETE", "DELETEALL"]:
        header["Content-Type"] = "application/json"
        if operationType.upper() == "DELETE":
            url = url + "/" + permId

        result = requests.delete(url,headers=header)
    elif operationType.upper() in ["ENABLE", "DISABLE"]:
        url = url + "/" + operationType
        result = requests.post(url, headers=header).json()
    else:
        print("Unknown Command.")
        quit()

    # 결과 출력
    # 콘솔에서 직접 수행한 것이 아니면 해당 프로그램으로 리턴
    if __name__ != "__main__":
        return result
    
    if jsonFormat or 'code' in result:
        pprint.pprint(result, indent=2)
    elif operationType.upper() in ["ENABLE","DISABLE"]:
        print(charAlign("File Path & Name", 60), end="  ")
        print(charAlign("File Type", 10), end=" ")
        print(charAlign("File Size", 20), end=" ")
        print(charAlign("File ID", 55))
        print("-"*150)
        print(charAlign(result["filePath"], 60), end="  ")
        print(charAlign(result["fileType"], 10), end=" ")
        print(charAlign(str(result["fileSize"]), 20), end=" ")
        print(charAlign(result["fileId"], 55))
    else:
        if operationType.upper() in ["DELETE","DELETEALL"]:
            print(result)
        else:
            print(charAlign("Permission",70), end="   ")
            print(charAlign("User Name", 20), end="   ")
            print(charAlign("Priv Type", 15), end="   ")
            print(charAlign("User Id", 35), end="   ")
            print(charAlign("User Type", 10))
            print("-"*190)
            if operationType.upper() in ["QUERY", "MODIFY", "CREATE"]:                           # 권한 조회/변경 결과
                if permId != None:
                    print(charAlign(result["permissionId"],70), end="   ")
                    print(charAlign(result["userName"], 20), end="   ")
                    print(charAlign(result["type"], 15), end="   ")
                    print(charAlign(result["userId"], 35), end="   ")
                    print(charAlign(result["userType"], 10))
                else:
                    for cnt in range(0, len(result["permissions"])):
                        print(charAlign(result["permissions"][cnt]["permissionId"],70), end="   ")
                        print(charAlign(result["permissions"][cnt]["userName"], 20), end="   ")
                        print(charAlign(result["permissions"][cnt]["type"], 15), end="   ")
                        print(charAlign(result["permissions"][cnt]["userId"], 35), end="   ")
                        print(charAlign(result["permissions"][cnt]["userType"], 10))
            # elif operationType.upper() == "CREATE":                          # 권한 생성 결과
            #     for cnt in range(0, len(result["permissions"])):
            #             print(charAlign(result["permissions"][cnt]["permissionId"],70), end="   ")
            #             print(charAlign(result["permissions"][cnt]["userName"], 20), end="   ")
            #             print(charAlign(result["permissions"][cnt]["type"], 15), end="   ")
            #             print(charAlign(result["permissions"][cnt]["userId"], 35), end="   ")
            #             print(charAlign(result["permissions"][cnt]["userType"], 10))
    


    
    


def usageView(mainArticle, subArticle):
    helpDict = {
        "adml" : mainArticle + " Administrator lists. Space separated.",
        "C" : "Client ID",
        "c" : "Client Secret",
        "cellphone" : "Cell Phone. XXX-XXXX-XXXX.",
        "cid" : "Calendar ID", 
        "d" : "Domain Id",
        "dlv" : "Display Level",
        "domain-list" : "Domain lists",
        "des" : "Descriptions. Use double quota",
        "driveid" : "Share drive ID. Required",
        "e" : "Service Id. xxxxserviceaccount@xxxxxx.com",
        "edate" : "End date. YYYY-MM-DD[THH:mm:ss]",
        "ek" : mainArticle + " External Key",
        "fdate" : "From Date time. YYYY-MM-DDThh:mm:ssTZD Type. Ex) 2023-05-02T15:26:00+09:00",
        "fileid" : "File(Folder)'s Unique ID",
        "first-name" : "First Name",
        "fp" : "File(Folder) Properties.",
        "gid" : "Group Id",
        "k" : "Private Key File",
        "last-name" : "Last Name",
        "loc" : "Event Location. Could be any string. ex)My Home",
        "m" : mainArticle + " ID (Email or Key)",
        "mem" : "Attendee member. --mem id type. type could be NEEDS-ACTION, ACCEPTED, DECLINED, TENTATIVE" if mainArticle == "Plan Post" else "Members. ( Usage : --mem MEMID TYPE ROLE --mem MEMID TYPE ROLE ). ROLE used in Calendar",
        "mst" : "Shared Drive Master's ID. One or more can be master. Space separated.",
        "n" : mainArticle + " Name",
        "operation" : "File / Folder manage command. Could be one of [query] [create] [remove]. Required.",
        "fileid" : "Specific file id. Ommit then Querying root folder",
        "filenm" : "When you create file or folder, It's name",
        "password-config" : "Password Config. Do not set if you use SSO. ADMIN or MANUAL",
        "password" : "Password when usin ADMIN password-config.",
        "permid" : "Permission ID. When privoper is deleteall you don't need permid. If you want query specific permission, use this option",
        "pid" : "Parents Organization Unit Id",
        "private-email" : "Private Email",
        "privoper" : "Privilege Operation. Could be one of 'query/create/modify/delete/deleteall/enable/disable'",
        "privtype" : "Privilege Type. Could be one of 'read/write'",
        "pt"  : "Plan Type. DATE - All day schedule, DATE / DATETIME - Time Schedule",
        "pt" : "Plan Type. DAY|DATETIME. DAY is all day schedule. Daytime has a time",
        "pub" : "If you Set, " + mainArticle + " will be public.",
        "rd" : "Repeat Days : SU,MO,TU,WE,TH,FR,SA. You can choose multiple days.(comma seperated)",
        "rf" : "Repeat Frequency. DAILY | WEEKLY | MONTHLY | YEARLY",
        "ri" : "Repeat Interval. Int value",
        "rs" : "Repeat Schedule.",
        "rm" : "Repeat Months. 1~12. Comma seperated",
        "s" : "Authorization Scope. space separated",
        "sdate" : "Start date. YYYY-MM-DD[THH:mm:ss]",
        "sn" : "Set parameter to use Service Notification",
        "sm" : "Set parameter to allow group administrator service manageable.",
        "sso" : "Use Single Sign On",
        "summary" : "Summary of All",
        "udate" : "Until Date Time. YYYYMMDDTHHmmssZ. ex) 20230701T000000Z" if mainArticle == "Plan" else "Until Date time. YYYY-MM-DDThh:mm:ssTZD Type. Ex) 2023-05-02T15:26:00+09:00",
        "uid" : "Organization Unit ID",
        "uid-list" : "Organization Unit Lists. First will be primary. space separated.",
        "um" : "Set parameter to use Group Messages.",
        "un" : "Set parameter to use Group Nots",
        "uc" : "Set parameter to use Group Calendar.",
        "ut" : "Set parameter to use Group Task",
        "uf" : "Set parameter to use Group Folder",
        "uM" : "Set parameter to use Group Mail. Should be set --m"
    }

    print(mainArticle + " Options")
    print("-"*20)
    for params in subArticle:
        if params in helpDict.keys():
            print("%-15s : %-150s" % (params, helpDict[params]))
    quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'NCP API Management Program', add_help=True)

    # GetAccessToken: Main
    group = parser.add_argument_group("Creating Access Token")
    group.add_argument('-g',help='get token', action='store_true')

    # GetAccessToken: Additional Options
    group = parser.add_argument_group("Required Options for -g")
    group.add_argument('-k',help='Private Key, Required', metavar="file_name",nargs=1,type=str)
    group.add_argument('-C',help='Client Id, Required', metavar="NCP Client ID",nargs=1)
    group.add_argument('-c',help='Client Secret, Required', metavar="NCP Client Secreat ID")
    group.add_argument('-e',help='Service Account Email, Required', metavar="xxxx.serviceacount@xxxx.xxx", nargs=1)
    group.add_argument('-s',help='OAuth Scope, Required', nargs='*', metavar="OAuth Privileges")
    # group.add_argument('-h',help='Help', action="store_true")

    # Get Info: Main
    # group = parser.add_argument_group("Getting Information")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-ca', help='Calendar Management', action='store_true')
    group.add_argument('-et', help='Employees Type Management', action='store_true')
    group.add_argument('-G',  help='Group Management', action='store_true')
    group.add_argument('-o',  help='Organization Managmenet', action='store_true')
    group.add_argument('-u',  help='User Management', action='store_true')
    group.add_argument('-P',  help='Plan Management', action='store_true')
    group.add_argument('-D',  help='Share Drive Management', action='store_true')
    group.add_argument('-Dp', help='Share Drive File/Folder Permission Management', action='store_true')
   
    # Other options
    # group = parser.add_argument_group("Sub-main Arguments")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--a','--adjust',help='Adjust Info', action="store_true")
    group.add_argument('--p','--post', help='Post data to Server', action='store_true')
    group.add_argument('--r','--remove',help='Remove Data', action='store_true')
    group.add_argument('--M','--modify', help='Modify(Patch) Data', action='store_true')
    
    group = parser.add_argument_group("Common Options")
    group.add_argument('--d','--domain-id', help='Domain Id', metavar="Domain_Id", type=int)
    group.add_argument('--j','--json', help='Print Josn raw format.', action='store_true', default=False)
    group.add_argument('--m','--user-id', help='User Email or Email Id. ', metavar="Email_or_Id", default=None)
    group.add_argument('--n','--name', help="Name of organization, group and etc (Not user name)", metavar="name", type=str)
    group.add_argument('--t','--toekn-file', help='Token File',metavar="default ak.token",default="ak.token")
    group.add_argument('--U','--user-key-id', help='User Key Id', metavar='user_key_id')
    group.add_argument('--cnt','--count', help='Count. default 100', metavar='Count', type=int, default=100)
    group.add_argument('--cur','--cursor', help='Cursor value when you need.', metavar='cursor', default=None)
    group.add_argument('--dlv','--display-level', help='Display Level', metavar="Level(int)", type=int)
    group.add_argument('--ek','--external',help='External Key', type=str)
    group.add_argument('--showall', help="Display Deleted useres.", action = 'store_true')
    
    group = parser.add_argument_group("User Options")
    group.add_argument('--first-name', help='First name', metavar="firstname")
    group.add_argument('--last-name', help='Last name', metavar="lastname")
    group.add_argument('--private-email', help='User Private Email', metavar="PrivateEmail")
    group.add_argument('--employee-type-id', help="User Employee Type Id", metavar="Employee Type Id")
    group.add_argument('--cellphone', help="User Cell Phone", metavar="xxx-xxx-xxxx")
    group.add_argument('--sso', help="Set parameter if using SSO", action='store_true', default=False)
    group.add_argument('--password-config', help='Password Configuration Type. Do not set if you using SSO.', choices=['ADMIN', 'MEMBER'])
    group.add_argument('--password', help="User Password when password policy is ADMIN", metavar="password")

    group = parser.add_argument_group("Organization, Oraganization Unit Options")
    group.add_argument('--primary', help="Set parameter to Primary Organization", action="store_true")
    group.add_argument('--params', help="Free parameter set",metavar="{ key:value, [key:value, ...]",type=json.loads)
    group.add_argument('--uid','--org-unit-id', help='Organization Unit Id', metavar="Organization Id", type=str)
    group.add_argument('--pid','--parents-org', help='Parents Organization Id', metavar="Parents Organization ID", type=str)
    group.add_argument('--domain-list', help="Oraganization Domain Lists. First Domain Organizaition will be Primary. if you ommit, --d will be Pirmary", metavar="domainId", nargs="*")
    group.add_argument('--uid-list', help="Organization Unit ID Lists. First OrgUnitId is primary.\n" +
                                          "You can separate org unit ID using this parameter --oid-list aa bb --oid-list yy zz.\n" +
                                          "First 2 aa bb will be involved first organization domain ID, and yy zz will be involed second organization domain ID"
                       ,metavar="uid", nargs="*", action="append")
    
    group = parser.add_argument_group("Group Options")    
    group.add_argument('--sm', '--service_manage', help="Use Service Management.", action='store_true', default=False)
    group.add_argument('--uM', '--use-mail', help="Use Group Mail. --m need.", action="store_true", default=False)

    group = parser.add_argument_group("Calendar Options")
    group.add_argument('--cid','--calendar-id', help='calendar ID', metavar="calendar_Id", type=str)
    group.add_argument('--show', help='Show calendar in calendar lists. Default is false. Set parameter to True', action="store_true")

    group = parser.add_argument_group("Organization / Group Common Options")
    group.add_argument('--adml', '--admin-list', help="administrators lists", metavar="User Id or Email", nargs="*")
    group.add_argument('--des', '--description', help="Organization Unit / Group Description. Wrap using double-quota(\")", type=str)
    group.add_argument('--gid','--group-id', help='Group Id', metavar="Group_Id", type=str)
    group.add_argument('--mem', '--member', help="Members Lists. member_id member_type. Type can be only one of USER, ORGUNIT, GROUP. On Calendar Plan allows NEEDS-ACTION, ACCEPTED, DECLINED TENTATIVE.  You can append this parameter to add more than one member.",metavar="MemberId MemberType", nargs="*", action="append")
    group.add_argument('--pub','--publc', help ="Set Organization unit/Group to public.", action='store_true')
    group.add_argument('--sn', '--service-noti', help="Use Service Notifiaction.", action='store_true')
    group.add_argument('--um', '--use-message', help="Use Organization Unit/Group Message.", action="store_true")
    group.add_argument('--un', '--use-note', help="Use Organization Unit/Group Notes. In group, --um need.", action="store_true")
    group.add_argument('--uc', '--use-calendar', help="Use Organization Unit/Group Calendar. In group, --um need.", action="store_true")
    group.add_argument('--ut', '--use-task', help="Use Organization Unit/Group Task. In group, --um need.", action="store_true")
    group.add_argument('--uf', '--use-folder', help="Use Organization Unit/Group Folder. In group, --um need.", action="store_true")
    
    group = parser.add_argument_group("Plan Options")
    group.add_argument('--fdate','--from-date-time',help="From Date Time. (YYYY-MM-DDThh:mm:ssTZD)", metavar="YYYY-MM-DDThh:mm:ssTZD", type=str)
    group.add_argument('--udate','--until-date-time',help="Until Date Time. (YYYY-MM-DDThh:mm:ssTZD)", metavar="YYYY-MM-DDThh:mm:ssTZD", type=str)
    group.add_argument('--pt','--plan-type',help="Plan Type. [DATE/DATETIME]", choices=["DATE","DATETIME"])
    group.add_argument('--sdate','--start-date', help="Plan Start date",metavar="YYYY-MM-DD[THH:mm:ss]")
    group.add_argument('--edate','--end-date', help="Plan End date",metavar="YYYY-MM-DD[THH:mm:ss]")
    group.add_argument('--summary',help="Summary", metavar="summary", type=str)
    group.add_argument('--loc',help="Location")
    group.add_argument('--rs','--repeat-schedule', help="Is Repeat", action='store_true', default=False)
    group.add_argument('--ri', '--repeat-interval',help="Repeat Interval", metavar="Repeat Interval. Number", type=str)
    group.add_argument('--rf', '--repeat-frequency',help="Repeat Frequency", choices=["DAILY","WEEKLY","MONTHLY","YEARLY"])
    group.add_argument('--rd', '--repeat-day', help="Repeat Day. SU,MO,TU,WE,TH,FR,SA")
    group.add_argument('--rm', '--repeat-month', help="Repeat Month. 1~12", type=str)
    group.add_argument('--re', '--repeat-exception', help="Repeat Exception Date.", nargs="*", metavar='YYYYMMDD')
    group.add_argument('--tz', '--time-zone', help="Timezone", default="Asia/Seoul")

    group = parser.add_argument_group("Shared Drive Option")
    group.add_argument('--driveid', help="Share drive Id", metavar="driveId")
    group.add_argument('--operation', help="Operation Type. One of 'query / create (folder) / remove", choices=['query','create', 'remove'])
    group.add_argument('--fileid', help="File or Folder's Id" )
    group.add_argument('--filenm', help="File or Folder's Name")
    group.add_argument('--fp', help="File properties", action='store_true')
    
    group = parser.add_argument_group("Drive Privilege Operation Option")
    group.add_argument('--privoper', help="Privilege Operation type. One of 'query / create / modify / delete / deleteall / enable / disable'.", choices=['query', 'create', 'modify', 'delete', 'deleteall', 'enable', 'disable'])
    group.add_argument('--privtype', help="Privilege Type. One of 'read / write'", choices=['read','write'])
    group.add_argument('--permid', help="Permission ID")


    args=parser.parse_args()
    # print(args)

    if args.g == False:
        with open (args.t,'r') as f:
            AccToken = f.read()

    if args.g:
        mainArticle = "Generate AccessToken"
        subArticle = ["k","C","c","e","s"]
        if args.k == None or args.C == None or args.c == None or args.e == None or args.s == None:
            usageView(mainArticle,subArticle)
            quit()
        else:
            with open(args.k[0], 'r') as f:
                privKey = f.read()
        
            clientId = args.C[0]
            clientSecret = args.c
            serviceAccount = args.e[0]
            scope=""
            for x in range(0,len(args.s)):
                scope += args.s[x]+' '
            getToken(clientId, clientSecret, serviceAccount, privKey, scope, args.t)
    elif args.u:
        mainArticle = "User"
        if args.p:
            mainArticle += " Post"
            subArticle = ["d","ek","m","private-email","first-name","last-name",
                        "domain-list","uid-list", "sso", "password-config", "password"]
            if args.d == None or args.m == None:
                usageView(mainArticle, subArticle)
            else:
                postUserInfo('post', args.d, args.ek, args.m, 
                             args.private_email, args.first_name, args.last_name, args.cellphone,
                             args.domain_list, args.uid_list, args.sso, args.password_config,
                             args.password, AccToken)
        elif args.r:
            mainArticle += " Remove"
            subArticle = ["m"]
            if args.m == None:
                usageView(mainArticle, subArticle)
            else:
                deleteUser(args.m, AccToken)
        elif args.a:
            mainArticle += " Adjust"
            subArticle = ["d","ek","m","private-email","first-name","last-name",
                        "domain-list","uid-list", "sso", "password-config", "password"]
            if args.d == None or args.m == None:
                usageView(mainArticle,subArticle)
            else:
                postUserInfo('put', args.d, args.ek, args.m, args.private_email,
                            args.first_name, args.last_name, 
                            args.cellphone, args.domain_list,
                            args.uid_list, args.sso, args.password_config,
                            args.password, AccToken)
        else:
            subArticle = ["m","d","cnt","cur","showall"]
            getUserInfo(args.m, args.d, args.cnt, args.cur, args.showall, AccToken, args.j)
    elif args.ca:
        mainArticle = "Calendar"
        if args.p:
            mainArticle += " Post"
            subArticle = ["n","mem","des","pub"]
            if args.n == None:
                usageView(mainArticle, subArticle)
            else: 
                postCalendar(args.n, args.mem, args.des, args.pub, AccToken)
        elif args.r:
            mainArticle += " Remove"
            subArticle = ["cid"]
            if args.cid == None:
                usageView(mainArticle, subArticle)
            else:
                deleteCalendar(args.cid, AccToken)
        elif args.m and args.a == False:
            mainArticle += " List for specific User"
            subArticle = ["m"]
            if args.m == None:
                usageView(mainArticle, subArticle)
            else:
                getUserCalendarLists(args.m, args.j, args.cur, args.cid, AccToken)
        elif args.a:
            mainArticle += " Adjust"
            subArticle = ["cid", "m", "mem", "show", "pub", "des"]
            if args.cid == None:
                usageView(mainArticle, subArticle)
            else:
                modifyUserCalendar(args.m, args.cid, args.show, args.mem, args.pub, args.des, AccToken)
        else:
            mainArticle += " Info"
            subArticle = ["cid"]
            if args.cid == None:
                usageView(mainArticle, subArticle)
            else:
                getCalendarInfo(args.cid, AccToken)
    elif args.o:
        mainArticle = "Organization"
        # 필요 옵션: domainid, count default 100, cursor default null
        if args.p == True:
            mainArticle += " Post"
            subArticle = ["n", "m", "d", "ek", "pid", "dlv" ]
            if args.n == None or args.d == None:
                usageView(mainArticle, subArticle)
            else:
                postOrganization(args.d, args.n, args.m, args.ek, args.pid, args.dlv, args.j, AccToken)
        elif args.r:
            mainArticle += " Remove"
            subArticle = ["uid"]
            if args.uid == None:
                usageView(mainArticle, subArticle)
            else:
                deleteOrgnization(args.uid, AccToken)
        else:
            if args.uid != None:
                getOrganizationInfo(args.d, args.uid, args.j, AccToken)
            else:
                getOraganizationLists(args.d, args.cnt, args.cur, args.j, AccToken)
    elif args.G:
        mainArticle = "Group"
        if args.p:
            mainArticle += " Post"
            subArticle = ["d","n","des","sn","sm","ek","adml","um","un",
                        "uc","ut","uf","uM","m","mem"]
            if args.d == None or args.n == None or args.adml == None or args.mem == None:
                usageView(mainArticle, subArticle)
            else:
                postGroup('Post', None, args.d, args.n, args.des, args.sn,
                        args.sm, args.ek, args.adml, 
                        args.um, args.un, args.uc, args.ut, args.uf,
                        args.uM, args.m, args.mem, args.j, AccToken)
        elif args.r:
            mainArticle += " Remove"
            subArticle = ["gid"]
            if args.gid == None:
                usageView(mainArticle, subArticle)
            else:
                deleteGroup(args.gid, AccToken)
        elif args.gid and args.a == False:
            mainArticle += " Info"
            subArticle = ["gid"]
            if args.gid == None:
                usageView(mainArticle, subArticle)
            else:
                getGroupInfo(args.gid, args.j, AccToken)
        elif args.a:
            mainArticle += " Adjust"
            subArticle = ["d","n","des","gid","sn","sm","ek","adml","um","un",
                        "uc","ut","uf","uM","m","mem"]
            if args.d == None or args.gid == None:
                usageView(mainArticle, subArticle)
            else:
                modifyGroup(args.d, args.gid, args.n, args.des, args.sn, args.sm, args.adml, args.um, args.un,
                            args.uc, args.ut, args.uf, args.uM, args.m, args.mem, args.j, AccToken)
        else :
            getGroupLists(args.d, args.cnt, args.cur, args.gid, args.j, AccToken)
    elif args.et:
        getEmployeesType(args.d, args.cnt, args.cur, args.j, AccToken)
    elif args.P:
        mainArticle = "Plan"    
        if args.p:
            mainArticle += " Post"
            subArticle = ["m", "cid", "summary", "des", "pt", "sdate", "edate", "rs",
                        "ri", "rf", "rd", "rm", "udate", "mem","loc"]
            if args.m == None or args.cid == None or args.summary == None or args.sdate == None or args.edate == None:
                usageView(mainArticle, subArticle)
            else:
                postPlanCalendar(args.m, args.cid, args.summary, args.des, args.loc, args.pt, args.sdate,
                                args.edate, args.tz, args.mem, args.rs, args.ri, args.rf, args.rd, args.rm,
                                args.udate, args.re, AccToken)
        else:
            mainArticle += " Query"
            subArticle = ["m","cid","fdate","udate"]
            if args.m == None or args.cid == None or args.fdate == None or args.udate == None:
                usageView(mainArticle, subArticle)
            else:
                getPlanCalendar(args.m, args.cid, args.fdate, args.udate, args.j, AccToken)
    elif args.D:
        mainArticle = "Shared Drive"
        if args.operation != None:
            subArticle = ["driveid", "operation", "fileid", "filenm", "fp"]
            if args.driveid == None or args.operation == None:
                usageView(mainArticle, subArticle)
            else:
                manageShareDriveObject(args.driveid, args.operation, args.fileid, args.filenm, args.fp, args.cur, args.j, AccToken)
        else:
            getShareDriveList(AccToken)
    elif args.Dp:
        mainArticle = "Drive File / Folder Privilege"
        subArticle = ["driveid", "privoper", "fileid", "permid"]
        if args.driveid == None or args.privoper == None or args.fileid == None:
            mainArticle = mainArticle + " Querying"
            usageView(mainArticle, subArticle)
        else:
            if args.privoper == "create":
                mainArticle = mainArticle + " Creation"
                subArticle.extend(["privtype","fileid","m"])
                if args.privtype == None or args.fileid == None or args.m == None:
                    usageView(mainArticle, subArticle)
                # else:
                #     manageShareDrivePrivs(args.driveid, args.privoper, args.fileid, args.permid, args.j, args.m, args.privtype, AccToken)
            elif args.privoper == "modify":
                mainArticle = mainArticle + " Modification"
                subArticle.extend(["privtype","permid"])
                if args.privtype == None:
                    usageView(mainArticle, subArticle)
                # else:
                #     manageShareDrivePrivs(args.driveid, args.privoper, args.fileid, args.permid, args.j, args.m, args.privtype, AccToken)
            elif args.privoper in ["delete", "deleteall"]:
                mainArticle = mainArticle + " Deletion"
                if args.privoper == ["delete"] and args.permid == None:
                    subArticle.append("permid")
                    usageView(mainArticle, subArticle)
                # else:
                #     manageShareDrivePrivs(args.driveid, args.privoper, args.fileid, args.permid, args.j, args.m, args.privtype, AccToken)
            elif args.privoper in ["enable", "disable"]:
                mainArticle = mainArticle + " Enable/Disable"              
            elif args.privoper == "query":
                None
            manageShareDrivePrivs(args.driveid, args.privoper, args.fileid, args.permid, args.j, args.m, args.privtype, AccToken)
                
                    


        

        # manageShareDrivePrivs(args.driveid, args.privoper, args.fileid, args.permid, args.j, args.m, args.privtype, AccToken)
        # if args.p:
        #     mainArticle += " Post"
        #     subArticle = ["mst","n","des"]
        #     if args.n == None or args.mst == None:
        #         usageView(mainArticle, subArticle)
        #     else:
        #         postShareDrive(args.mst, args.n, args.des, AccToken)
        # else:
        #     mainArticle += " Get"
        #     getShareDriveList(AccToken)







        # elif args.cid != None:
        #     subArticle = ["fdate","udate"]
        #     if args.fdate == None or args.udate == None:
        #         usageView(mainArticle, subArticle)
        #     else :
        #         getPlanCalendar(args.m, args.cid, args.fdate, args.udate, AccToken)-