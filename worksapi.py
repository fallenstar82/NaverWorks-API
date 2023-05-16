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

                    print(charAlign(result["users"][userCount]["userId"],50) +
                          charAlign(result["users"][userCount]["email"],40) +
                          charAlign(result["users"][userCount]["userName"]["lastName"] + result["users"][userCount]["userName"]["firstName"],25) +
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
        elif passWordPolicy == 'MANUAL':
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
def getUserCalendarLists(userId, jsonFormat, AccToken):
    header = {
        "Authorization": "Bearer " + AccToken
    }

    url = "https://www.worksapis.com/v1.0/users/" + userId + "/calendar-personals"

    result = requests.get(url, headers=header).json()

    if __name__ != "__main__":
        return result
    
    if jsonFormat:
        pprint.pprint(result, indent=2)
    else:
        for calList in result["calendarPersonals"]:
            print("%-50s : %-45s" % (calList["calendarId"], calList["calendarName"]))

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

def postPlanCalendar(userId, calendarId, planSummary, planDescription, planType, startDate, endDate, timeZone,
                     isRepeat, repeatInterval, repeatFrequency, repeatDay, repeatMonth,
                     repeatUntil, AccToken):
    header = {
        "Authorization" : "Bearer " + AccToken,
        "Content-Type" : "application/json"
    }

    if isRepeat:
        recurrency = "RRULE:"
        positionCount = 1
        if repeatInterval:
            recurrency = recurrency + "INTERVAL="+str(repeatInterval)
            positionCount = positionCount + 1
        if repeatFrequency:
            if positionCount > 1:
                recurrency = recurrency + ";"
            recurrency = recurrency + "FREQ=" + repeatFrequency.upper()
            positionCount = positionCount + 1
        if repeatDay:
            if positionCount > 1:
                recurrency = recurrency + ";"
            recurrency = recurrency + "BYDAY="+repeatDay.upper()
            positionCount = positionCount + 1
        if repeatMonth:
            if positionCount > 1:
                recurrency = recurrency + ";"
            recurrency = recurrency + "BYMONTH=" + repeatMonth
        if repeatUntil:
            if positionCount > 1:
                recurrency = recurrency + ";"
            recurrency = recurrency + "UNTIL=" + repeatUntil
    else:
        recurrency = None

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
            "recurrence" : [ recurrency ],
            "reminders" : [
                {
                    "method" : "DISPLAY",
                    "trigger" : "-PT15M"
                }
            ]
        }
    ]
    params = {
        "eventComponents" : eventComponents
    }
    
    url = "https://www.worksapis.com/v1.0/users/" + userId + "/calendars/" + calendarId + "/events"
    print(url)
    pprint.pprint(params)

    result = requests.post(url,headers=header,json=params).json()
    if __name__ != "__main__":
        return result
    pprint.pprint(result, indent=2)

# Organization
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
def getGroupLists(domainId, count, cursor, groupId, jsonFormat, AccToken):
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

def postGroup(domainId :int, groupName :str, description :str, serviceNotification :bool,
              serviceManagement :bool, externalKey :str, administrators :list,
              useMessage :bool, useNote :bool, useCalendar :bool, useTask :bool, useFolder :bool,
              useMail :bool, groupEmail :str, members :list, AccToken :str ):
    if useMessage == False:
        if useNote == True or useCalendar == True or useTask == True or useFolder == True:
            print("Want to Use group Note, Calendar, Task or Folder,")
            print("You must set -um option.")
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
    url = "https://www.worksapis.com/v1.0/groups"

    result=requests.post(url,headers=header,json=params).json()
    if __name__ != "__main__":
        return result
   
    pprint.pprint(result, indent=2)

def deleteGroup(groupId, AccToken):
    header = {
        "Authorization" : "Bearer " + AccToken
    }

    url = "https://www.worksapis.com/v1.0/groups/" + groupId

    result = requests.delete(url, headers=header)
    if __name__ != "__main__":
        return result.text
    print(result.text)

def getGroupInfo(groupId, AccToken):
    header = {
        "Authorization" : "Bearer " + AccToken
    }

    url = "https://www.worksapis.com/v1.0/groups/" + groupId

    result = requests.get(url, headers=header).json()
    if __name__ != "__main__":
        return result.text
    pprint.pprint(result, indent=2)

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
        "e" : "Service Id. xxxxserviceaccount@xxxxxx.com",
        "edate" : "End date. YYYY-MM-DD[THH:mm:ss]",
        "ek" : mainArticle + " External Key",
        "first-name" : "First Name",
        "fdate" : "From Date time. YYYY-MM-DDThh:mm:ssTZD Type. Ex) 2023-05-02T15:26:00+09:00",
        "gid" : "Group Id",
        "k" : "Private Key File",
        "last-name" : "Last Name",
        "m" : mainArticle + " ID (Email or Key)",
        "mem" : "Members. ( Usage : --mem MEMID TYPE ROLE --mem MEMID TYPE ROLE ). ROLE used in Calendar",
        "n" : mainArticle + " Name",
        "password-config" : "Password Config. Do not set if you use SSO. ADMIN or MANUAL",
        "password" : "Password when usin ADMIN password-config.",
        "pid" : "Parents Organization Unit Id",
        "private-email" : "Private Email",
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
    group = parser.add_argument_group("Getting Information")
    group.add_argument('-ca', help='Calendar Management', action='store_true')
    group.add_argument('-et', help='Employees Type Management', action='store_true')
    group.add_argument('-G',  help='Group Management', action='store_true')
    group.add_argument('-o',  help='Organization Managmenet', action='store_true')
    group.add_argument('-u',  help='User Management', action='store_true')
    group.add_argument('-P',  help='Plan Management', action='store_true')
   
    # Other options
    group = parser.add_argument_group("Sub-main Arguments")
    group.add_argument('--a','--adjust',help='Adjust Info', action="store_true")
    group.add_argument('--p','--post', help='Post data to Server', action='store_true')
    group.add_argument('--r','--remove',help='Remove Data', action='store_true')
    
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
    group.add_argument('--password-config', help='Password Configuration Type. Do not set if you using SSO.', choices=['ADMIN', 'MANUAL'])
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

    group = parser.add_argument_group("Organization / Group Common Options")
    group.add_argument('--adml', '--admin-list', help="administrators lists", metavar="User Id or Email", nargs="*")
    group.add_argument('--cid','--calendar-id', help='calendar ID', metavar="calendar_Id", type=str)
    group.add_argument('--des', '--description', help="Organization Unit / Group Description. Wrap using double-quota(\")", type=str)
    group.add_argument('--gid','--group-id', help='Group Id', metavar="Group_Id", type=str)
    group.add_argument('--mem', '--member', help="Members Lists. member_id member_type. Type can be only one of USER, ORGUNIT, GROUP. You can append this parameter to add more than one member.",metavar="MemberId MemberType", nargs="*", action="append")
    group.add_argument('--pub','--publc', help ="Set Organization unit/Group to public.", action='store_true',default=False)
    group.add_argument('--sn', '--service-noti', help="Use Service Notifiaction.", action='store_true', default=False)
    group.add_argument('--um', '--use-message', help="Use Organization Unit/Group Message.", action="store_true", default=False)
    group.add_argument('--un', '--use-note', help="Use Organization Unit/Group Notes. In group, --um need.", action="store_true", default=False)
    group.add_argument('--uc', '--use-calendar', help="Use Organization Unit/Group Calendar. In group, --um need.", action="store_true", default=False)
    group.add_argument('--ut', '--use-task', help="Use Organization Unit/Group Task. In group, --um need.", action="store_true", default=False)
    group.add_argument('--uf', '--use-folder', help="Use Organization Unit/Group Folder. In group, --um need.", action="store_true", default=False)
    
    group = parser.add_argument_group("Plan Options")
    group.add_argument('--fdate','--from-date-time',help="From Date Time. (YYYY-MM-DDThh:mm:ssTZD)", metavar="YYYY-MM-DDThh:mm:ssTZD", type=str)
    group.add_argument('--udate','--until-date-time',help="Until Date Time. (YYYY-MM-DDThh:mm:ssTZD)", metavar="YYYY-MM-DDThh:mm:ssTZD", type=str)
    group.add_argument('--pt','--plan-type',help="Plan Type. [DATE/DATETIME]", choices=["DATE","DATETIME"])
    group.add_argument('--sdate','--start-date', help="Plan Start date",metavar="YYYY-MM-DD[THH:mm:ss]")
    group.add_argument('--edate','--end-date', help="Plan End date",metavar="YYYY-MM-DD[THH:mm:ss]")
    group.add_argument('--summary',help="Summary", metavar="summary", type=str)
    group.add_argument('--rs','--repeat-schedule', help="Is Repeat", action='store_true', default=False)
    group.add_argument('--ri', '--repeat-interval',help="Repeat Interval", metavar="Repeat Interval. Number", type=str)
    group.add_argument('--rf', '--repeat-frequency',help="Repeat Frequency", choices=["DAILY","WEEKLY","MONTHLY","YEARLY"])
    group.add_argument('--rd', '--repeat-day', help="Repeat Day. SU,MO,TU,WE,TH,FR,SA")
    group.add_argument('--rm', '--repeat-month', help="Repeat Month. 1~12", type=str)
    group.add_argument('--tz', '--time-zone', help="Timezone", default="Asia/Seoul")

    args=parser.parse_args()
    print("="*30)
    print(args)
    print("="*30)

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
        elif args.m:
            mainArticle += " List User"
            subArticle = ["m"]
            if args.m == None:
                usageView(mainArticle, subArticle)
            else:
                getUserCalendarLists(args.m, args.j, AccToken)
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
                postGroup(args.d, args.n, args.des, args.sn,
                        args.sm, args.ek, args.adml, 
                        args.um, args.un, args.uc, args.ut, args.uf,
                        args.uM, args.m, args.mem, AccToken)
        elif args.r:
            mainArticle += " Remove"
            subArticle = ["gid"]
            if args.gid == None:
                usageView(mainArticle, subArticle)
            else:
                deleteGroup(args.gid, AccToken)
        elif args.gid:
            mainArticle += " Info"
            subArticle = ["gid"]
            if args.gid == None:
                usageView(mainArticle, subArticle)
            else:
                getGroupInfo(args.gid, AccToken)
        else :
            getGroupLists(args.d, args.cnt, args.cur, args.gid, args.j, AccToken)
    elif args.et:
        getEmployeesType(args.d, args.cnt, args.cur, args.j, AccToken)
    elif args.P:
        mainArticle = "Plan"    
        if args.p:
            mainArticle += " Post"
            subArticle = ["m", "cid", "summary", "des", "pt", "sdate", "edate", "rs",
                        "ri", "rf", "rd", "rm", "udate"]
            if args.m == None or args.cid == None or args.summary == None or args.sdate == None or args.edate == None:
                usageView(mainArticle, subArticle)
            else:
                postPlanCalendar(args.m, args.cid, args.summary, args.des, args.pt, args.sdate,
                                args.edate, args.tz, args.rs, args.ri, args.rf, args.rd, args.rm,
                                args.udate, AccToken)
        else:
            mainArticle += " Query"
            subArticle = ["m","cid","fdate","udate"]
            if args.m == None or args.cid == None or args.fdate == None or args.udate == None:
                usageView(mainArticle, subArticle)
            else:
                getPlanCalendar(args.m, args.cid, args.fdate, args.udate, args.j, AccToken)






        # elif args.cid != None:
        #     subArticle = ["fdate","udate"]
        #     if args.fdate == None or args.udate == None:
        #         usageView(mainArticle, subArticle)
        #     else :
        #         getPlanCalendar(args.m, args.cid, args.fdate, args.udate, AccToken)-