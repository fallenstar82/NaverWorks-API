import jwt
import requests
import unicodedata
import json
import pprint
import csv
import argparse
import sys
from time import time

def getToken(tokenFile : str):
    try:
        with open(tokenFile, 'r') as f:
            token = f.read()
    except IOError:
        print("IOError on file \""+tokenFile+"\"")
        exit(1)
    return token
    
def callAuthorizationStep(args):
    if args.t == 'jwt':
        from works.auth import AuthByJWT
        print("Run Authorize by JWT")
        AuthByJWT(args)
    elif args.t == 'oauth':
        from works.auth import AuthByOAuth
        print("Run Authorize by OAuth")
        AuthByOAuth(args)

def callUserManage(args):
    token = getToken(args.f)
    
    from works.UserManage import UserManage
    App = UserManage(token)
    if args.operationType == 'QUERY':
        continueYN = "Y"
        coursor = args.cur
        while continueYN == "Y":
            result = App.queryUser(args.m, args.d, args.lim, coursor)
            pprint.pprint(result, indent = 2)
            if 'responseMetaData' in result:
                if 'nextCursor' in result['responseMetaData'] :
                    if result['responseMetaData']['nextCursor'] == None:
                        continueYN = "N"
                    else:
                        print("Show Next Page ? [y/n] : ")
                        continueYN = input()
                        continueYN = continueYN.upper()
                        print("Response : " + continueYN)
                        coursor = result['responseMetaData']['nextCursor']
            else:
                continueYN = "N"

def callOrgManage(args):
    token = getToken(args.f)
    
    from works.OrgManage import OrgManage
    App = OrgManage(token)
    if args.operationType == 'QUERY':
        continueYN = "Y"
        coursor = args.cur
        while continueYN == "Y":
            result = App.queryOrg(args.o, args.d, args.lim, coursor)
            pprint.pprint(result, indent = 2)
            if 'responseMetaData' in result:
                if 'nextCursor' in result['responseMetaData'] :
                    if result['responseMetaData']['nextCursor'] == None:
                        continueYN = "N"
                    else:
                        print("Show Next Page ? [y/n] : ")
                        continueYN = input()
                        continueYN = continueYN.upper()
                        print("Response : " + continueYN)
                        coursor = result['responseMetaData']['nextCursor']
            else:
                continueYN = "N"
    elif args.operationType == 'ADD':
        result = App.addOrg(
            args.d,
            args.n,
            args.sortorder,
            args.p,
            args.extkey,
            args.email,
            args.aemail,
            args.allow_sender,
            args.re,
            args.usemsg,
            args.usenote,
            args.usecal,
            args.usetask,
            args.usefolder,
            args.usenoti,
            False if args.novisible else True,
            args.description
        )
        pprint.pprint(result, indent=2)

def callCalManage(args):
    token = getToken(args.f)
    
    from works.CalManage import CalManage
    App = CalManage(token)
    if args.operationType == 'QUERY':
        continueYN = "Y"
        coursor = args.cur
        while continueYN == "Y":
            result = App.queryCalendar(args.p, args.s, args.m, args.cid, coursor)
            pprint.pprint(result, indent = 2)
            if 'responseMetaData' in result:
                if 'nextCursor' in result['responseMetaData'] :
                    if result['responseMetaData']['nextCursor'] == None:
                        continueYN = "N"
                    else:
                        print("Show Next Page ? [y/n] : ")
                        continueYN = input()
                        continueYN = continueYN.upper()
                        print("Response : " + continueYN)
                        coursor = result['responseMetaData']['nextCursor']
            else:
                continueYN = "N"

def callPlanManage(args):
    token = getToken(args.f)
    
    from works.PlanManage import PlanManage
    App = PlanManage(token)
    if args.operationType == 'QUERY':        
        result = App.queryPlan(args.m, args.cid, args.eid, args.targetym)
        pprint.pprint(result, indent = 2)
    elif args.operationType == "ADD":
        # Start Parsing
        if args.type == "day":
            startDate = { "date": args.start }
            endDate   = { "date" : args.end  }
        else:
            startDate = { "dateTime" : args.start, "timeZone" : args.tz }
            endDate   = { "dateTime" : args.end,   "timeZone" : args.tz }
        
        # Recurrence Parsing
        recurrenceData = list()
        if args.recfreq or args.recuntil or args.recint or args.recbt:
            rruleData = "RRULE:FREQ=" + (args.recfreq).upper() + ";INTERVAL=" + args.recint + (";" + ((args.recbt).upper() + "=" + args.recbtv) if args.recbt else "") + ((";UNTIL=" + args.recuntil) if args.recuntil else "")
            recurrenceData.append(rruleData)
            if args.reex:
                for exDay in args.reex:
                    recurrenceData.append(
                        "EXDATE;" + (("TZID=" + args.tz + ":" + exDay) if args.type == "time" else "VALUE=DATE:" + exDay)
                    )
        
        # Attendee Parsing
        attendeeList = list()
        if len(args.attid) == len(args.attdpname) == len(args.partstat) and len(args.attid) > 0:
            for attendeeCounter in range(0,len(args.attid)):
                attendeeList.append({
                    "email" : args.attid[attendeeCounter],
                    "displayName" : args.attdpname[attendeeCounter],
                    "partstat" : args.partstat[attendeeCounter]
                })

        # Reminder Parsing
        reminderList = list()
        if len(args.almethod) == len(args.altrigger) and len(args.almethod) > 0:
            for alarmCounter in range(0, len(args.almethod)):
                reminderList.append({
                    "method"  : (args.almethod[alarmCounter]).upper(),
                    "trigger" : "-" + (args.altrigger[alarmCounter]).upper()
                    })

        # Map Parsing        
        if args.mtype == None:
            map = None
        else:
            map = { "type" :  args.mtype, "geo" : args.geo }

        if args.murl == None:
            mapUrl = None
        else:
            mapUrl = { "mapUrl" :  args.mapUrl, "imageId" : args.mimg }
        
        # Organizer Info
        if args.oid == None and args.odpname == None:
            organizer = None
        elif args.oid == None and args.odpname != None:
            organizer = { "displayName" : args.odpname }
        elif args.oid != None and args.odpname == None:
            organizer = { "email" : args.oid }
        else:
            organizer = { "email" : args.oid, "displayName" : args.odpname }

        # Video Meeing Parasing
        if args.vurl == None and args.vrid == None:
            videoMeet = None
        elif args.vurl == None and args.vrid != None:
            videoMeet = { "resourceId" : args.vrid }
        elif args.vurl != None and args.vrid == None:
            videoMeet = { "url" : args.vurl }
        else:
            videoMeet = { "url" : args.vurl, "resourceId" : args.vrid }
                                      
        result = App.addPlan(
            args.m,
            args.summary,
            startDate, endDate,
            args.cid,
            args.eid,
            args.location,
            map,
            mapUrl,
            args.category,
            organizer,
            recurrenceData,
            None,
            args.transparency,
            args.visibility,
            args.sequence,
            attendeeList,
            videoMeet,
            reminderList,
            args.description
        )

        pprint.pprint(result, indent=2, sort_dicts=False)


parser = argparse.ArgumentParser(description = "WORKS | WORKSPLACE API Management Program V2")
subparsers = parser.add_subparsers(help="Description", required=True)
################################################################################
# Auth                                                                         #
################################################################################
parserAuth = subparsers.add_parser('auth', help="Authrization Step")
parserAuth.add_argument('-t', help="Auth type. Required", choices=["oauth","jwt"], required=True)
parserAuth.add_argument('-c', help="Required oauth|jwt Both.",type=str, required=True, metavar="Client ID")
parserAuth.add_argument('-s', help="Required oauth|jwt Both", type=str, required=True, metavar="Secret Key")
parserAuth.add_argument('-o', help="Required oauth|jwt Both. Privilege Scope", nargs="*", required=True, metavar="priv")
parserAuth.add_argument('-f', help="Required oauth|jwt Both. Default 'ak.token'.", type=str, default="ak.token", metavar="filename")
parserAuth.add_argument('-k', help="Required jwt", type=str, metavar="Private key file")
parserAuth.add_argument('-a', help="Required jwt", type=str, metavar="Service account")
parserAuth.add_argument('-d', help="Required oauth.", type=str, metavar="Domain")
parserAuth.add_argument('-r', help="Required oauth", type=str, metavar="Redirect URL for auth")
parserAuth.set_defaults(func=callAuthorizationStep)

################################################################################
# UserMangement                                                                #
################################################################################
parserUser = subparsers.add_parser('user', help="User Management")
parserUser.set_defaults(func=callUserManage)
subparsersUser = parserUser.add_subparsers(help="Description", dest="USER")
# UserManagement - Query
subparsersUserQuery = subparsersUser.add_parser('query', help="Query User(s)")
subparsersUserQuery.add_argument('-f', help="Access token file. default ak.token", type=str, metavar="Filename", default="ak.token")
subparsersUserQuery.add_argument('-m', help="Members Email or ID", type=str, metavar="Email|Id")
subparsersUserQuery.add_argument('-d', help="Domain Id", type=int, metavar="domain")
subparsersUserQuery.add_argument('--lim', help="Number of print, Default 100", type=int, default=100, metavar="number")
subparsersUserQuery.add_argument('--cur', help="Next page cursor", type=str, metavar="cursor")
subparsersUserQuery.set_defaults(operationType="QUERY")
# UserManagement - add
subparsersUserAdd = subparsersUser.add_parser('add', help="Add User")
subparsersUserAdd.add_argument('-t', help="Access token file. default ak.token", type=str, metavar="Filename", default="ak.token")
subparsersUserAdd.set_defaults(operationType="ADD")
# UserManagement - Query
subparsersUserDelete = subparsersUser.add_parser('delete', help="Delete User")
subparsersUserDelete.set_defaults(operationType="DELETE")
# UserManagement - Query
subparsersUserUpdate = subparsersUser.add_parser('update', help="Update Users")
subparsersUserUpdate.set_defaults(operationType="UPDATE")

################################################################################
# OrgManagement                                                                #
################################################################################
parserOrg = subparsers.add_parser('org', help="Organization Management")
parserOrg.set_defaults(func=callOrgManage)
subparsersOrg = parserOrg.add_subparsers(help="Description", dest="ORG")
# OrgManagement - Query
subparsersOrgQuery = subparsersOrg.add_parser('query', help="Query Orgs")
subparsersOrgQuery.add_argument('-f', help="Access token file. default ak.token", type=str, metavar="Filename", default="ak.token")
subparsersOrgQuery.add_argument('-o', help="Org unit Id", type=str, metavar="Org Unit ID")
subparsersOrgQuery.add_argument('-d', help="Domain Id", type=int, metavar="domain")
subparsersOrgQuery.add_argument('--lim', help="Display limit, Default 100", type=int, default=100, metavar="number")
subparsersOrgQuery.add_argument('--cur', help="Next page cursor", type=str, metavar="cursor")
subparsersOrgQuery.set_defaults(operationType="QUERY")
# OrgManagement - Add
subparsersOrgAdd = subparsersOrg.add_parser('add', help="Add User")
subparsersOrgAddReq = subparsersOrgAdd.add_argument_group("Required Options")
subparsersOrgAddReq.add_argument('-f', help="Access token file. default ak.token", type=str, metavar="Filename", default="ak.token")
subparsersOrgAddReq.add_argument('-d', help="DomainId", type=str, metavar="Domain Id", required=True)
subparsersOrgAddReq.add_argument('-n', help="Organization name", type=str, metavar="Name", required=True)
subparsersOrgAddReq.add_argument('-p', help="Parents Org Id. None to Top", type=str, metavar="ParentOrgId")
subparsersOrgAddOpt = subparsersOrgAdd.add_argument_group("Optional")
subparsersOrgAddOpt.add_argument('--sortorder', help="Sort Order", type=int, metavar="Order Number", default=1)
subparsersOrgAddOpt.add_argument('--extkey', help='External Key', type=str, metavar="extKey")
subparsersOrgAddOpt.add_argument('--email', help="Organization Email", type=str, metavar="Email")
subparsersOrgAddOpt.add_argument('--aemail', help="Email Alias. max 20 str", type=str, nargs="*", metavar="aEmail")
subparsersOrgAddOpt.add_argument('--allow-sender', help="Members allowed to use org unit email as recipient", type=str, nargs="*")
subparsersOrgAddOpt.add_argument('--re', help="Allow receive external mail", action="store_true", default=False)
subparsersOrgAddOpt.add_argument('--usemsg', help="Use Message", action="store_true", default=False)
subparsersOrgAddOpt.add_argument('--usenote', help="Use Note. Must be set --usemsg", action="store_true", default=False)
subparsersOrgAddOpt.add_argument('--usecal', help="Use Calendar. Must be set --usemsg", action="store_true", default=False)
subparsersOrgAddOpt.add_argument('--usetask', help="Use task. Must be set --usemsg", action="store_true", default=False)
subparsersOrgAddOpt.add_argument('--usefolder', help="Use task. Must be set --usemsg", action="store_true", default=False)
subparsersOrgAddOpt.add_argument('--usenoti', help="Use Service notification.", action="store_true", default=False)
subparsersOrgAddOpt.add_argument('--novisible', help="Set to not display", default=False, action="store_true")
subparsersOrgAddOpt.add_argument('--description', help="Description", type=str)
subparsersOrgAdd.set_defaults(operationType="ADD")
# OrgManagement - Delete
subparsersOrgDelete = subparsersOrg.add_parser('delete', help="Delete User")
subparsersOrgDelete.set_defaults(operationType="DELETE")
# OrgManagement - Update
subparsersOrgUpdate = subparsersOrg.add_parser('update', help="Update Users")
subparsersOrgUpdate.set_defaults(operationType="UPDATE")

################################################################################
# CalendarManagement                                                           #
################################################################################
parserCal = subparsers.add_parser('cal', help="Calendar Management")
parserCal.set_defaults(func=callCalManage)
subparsersCal = parserCal.add_subparsers(help="Description", dest="CAL")
# Calendar - Query
subparsersCalQuery = subparsersCal.add_parser('query', help="Calendar List Query")
subparsersCalQueryMain = subparsersCalQuery.add_argument_group('Choose Personal or Shared Calendar')
subparsersCalQueryExGroup = subparsersCalQueryMain.add_mutually_exclusive_group(required=True)
subparsersCalQueryExGroup.add_argument('-p', help="Display target's calendar attribue that can access.", action="store_true")
subparsersCalQueryExGroup.add_argument('-s', help="Display target's share attribute. if -m set, display user's default calendar.", action="store_true")
subparsersCalQueryMain = subparsersCalQuery.add_argument_group("Require Options")
subparsersCalQueryMain.add_argument('-f', help="Access token file. default ak.token", type=str, metavar="Filename", default="ak.token")
subparsersCalQueryMain.add_argument('-m', help="member's Email or ID", type=str, metavar="Email|ID")
subparsersCalQueryMain.add_argument('--cid', help="Calendar ID", type=str, metavar="Calendar ID")
subparsersCalQueryMain.add_argument('--cur', help="cusrsor ID", type=str, metavar="Coursor ID")
subparsersCalQuery.set_defaults(operationType="QUERY")

################################################################################
# Plan Management                                                              #
################################################################################
parserPlan = subparsers.add_parser('plan', help="Plan Management")
parserPlan.set_defaults(func=callPlanManage)
subparsersPlan = parserPlan.add_subparsers(help="Description", dest="PLAN")
# Plan - query
subparsersPlanQuery = subparsersPlan.add_parser('query', help="Query Plan")
subparsersPlanQueryMain = subparsersPlanQuery.add_argument_group("default Options")
subparsersPlanQueryMain.add_argument('-m', help="member's Email or ID", type=str, metavar="Email|ID", required=True)
subparsersPlanQueryMain.add_argument('-f', help="Access Token file. Default 'ak.token'.", type=str, default="ak.token", metavar="filename")
subparsersPlanQueryMain = subparsersPlanQuery.add_argument_group("Optional")
subparsersPlanQueryMain.add_argument('--cid', help="Calendar ID. If ommit, Query member's default calendar", type=str, metavar="Calendar ID")
subparsersPlanQueryMain.add_argument('--eid', help="Event ID. If ommit, List Plans.", type=str, metavar="Event ID")
subparsersPlanQueryMain.add_argument('--targetym', help="Query Year Month. Ex) YYYY-MM. Set when -e ommitted.", type=str, metavar="YYYY-MM")
subparsersPlanQuery.set_defaults(operationType="QUERY")
# Plan - Add
subparsersPlanAdd = subparsersPlan.add_parser('add', help="Add Plan")
subparsersPlanAddMain = subparsersPlanAdd.add_argument_group("Access Token Options")
subparsersPlanAddMain.add_argument('-f', help="Access Token file. Default 'ak.token'.", type=str, default="ak.token", metavar="filename")
subparsersPlanAddMain = subparsersPlanAdd.add_argument_group("Default Options")
subparsersPlanAddMain.add_argument('-m', help="member's Email or ID", type=str, metavar="Email|ID", required=True)
subparsersPlanAddMain.add_argument('--summary', help="Summary of Plan. (Title)", type=str, metavar="Summary", required=True)
subparsersPlanAddMain.add_argument('--cid', help="Calendar ID. If ommit, add plan to member default calendar.", type=str, metavar="Calendar ID")
subparsersPlanAddMain = subparsersPlanAdd.add_argument_group("Date and Time Zone Option")
subparsersPlanAddMain.add_argument('--type', help="Plan Type. All day plan or Time plan. (Title)", choices=["day","time"], required=True)
subparsersPlanAddMain.add_argument('--start', help="Plan Start Time. All day plan : YYYY-MM-DD, Time plan : YYYY-MM-DDTHH:mm:ss.",metavar="YYYY-MM-DD|YYYY-MM-DDTHH:mm:ss", required=True)
subparsersPlanAddMain.add_argument('--end', help="Plan End Time. All day plan : YYYY-MM-DD (End date is exclusive), Time plan : YYYY-MM-DDTHH:mm:ss. ",metavar="YYYY-MM-DD|YYYY-MM-DDTHH:mm:ss")
subparsersPlanAddMain.add_argument('--tz', help="Timezone. Set this parameter when plan type(--type) is \"time\". ex)Asia/Seoul. default Asia/Seoul",metavar="Region/City", default="Asia/Seoul")
subparsersPlanAddMain = subparsersPlanAdd.add_argument_group("Organizer Option")
subparsersPlanAddMain.add_argument('--oid', help="Organizer's Id or Email", metavar="Id|Email", type=str)
subparsersPlanAddMain.add_argument('--odpname', help="Organizer display Name", metavar="name", type=str)
subparsersPlanAddMain = subparsersPlanAdd.add_argument_group("Attendee Info",description="If you want to set attendee, Set parameter below all. Don't ommit any parameters.\nThere is more than one attendes, repeat parameters as attendees")
subparsersPlanAddMain.add_argument('--attid', help="email or Id", metavar="email or Id", type=str, action="append")
subparsersPlanAddMain.add_argument('--attdpname', help="Attendees display name", metavar="name", type=str, action="append")
subparsersPlanAddMain.add_argument('--partstat', help="partstat", choices=["need-action","accepted","tentative","declined"], action="append")
subparsersPlanAddMain = subparsersPlanAdd.add_argument_group("Recurrency option",description="Day Name : SU/MO/TU/WE/TH/FR/SA")
subparsersPlanAddMain.add_argument('--recfreq', help="Repeat frequency.", choices=["secondly","minutely","hourly","daily","weekly","monthly","yearly"], metavar="Frequency")
subparsersPlanAddMain.add_argument('--recuntil', help="Repeat Until.", type=str, metavar="YYYY-MM-DDTHH:mm:ss")
subparsersPlanAddMain.add_argument('--recint', help="Repeat interval. default 1.", type=str, metavar="Interval", default="1")
subparsersPlanAddMain.add_argument('--recbt', help="Set by types.", choices=["bysecond","byminute","byhour","byday","bymonthday","byyearday","byweekno","bymonth"], metavar="Interval")
subparsersPlanAddMain.add_argument('--recbtv', help="By types value.",type=str, metavar="Interval")
subparsersPlanAddMain = subparsersPlanAdd.add_argument_group("Recurrency Exception")
subparsersPlanAddMain.add_argument('--reex', help="Exception day. ex)20240301T000000Z",type=str, nargs="*", metavar="YYYYMMDDThhmmssZ")
subparsersPlanAddMain = subparsersPlanAdd.add_argument_group("Video Meeeting Options")
subparsersPlanAddMain.add_argument('--vurl', help="Video meeting url", metavar="url", type=str)
subparsersPlanAddMain.add_argument('--vrid', help="Video meeting resource Id", metavar="url", type=str)
subparsersPlanAddMain = subparsersPlanAdd.add_argument_group("Reminder Option", description="If you want to alarm more than once, repeat parameters.")
subparsersPlanAddMain.add_argument('--almethod', help="Alarm Method", choices=["display","email"], action="append")
subparsersPlanAddMain.add_argument('--altrigger', help="Alarm Trigger. ex)PT0S, PT15M, PT12H, P1D\"", type=str, metavar="trigger", action="append")
subparsersPlanAddMain = subparsersPlanAdd.add_argument_group("Map Option")
subparsersPlanAddMain.add_argument('--mtype', help="Map type. ex)NAVER, google", type=str, metavar="MapType")
subparsersPlanAddMain.add_argument('--geo', help="Geolocation. ex) \"40.7486484;-73.98400699999999\" ", type=str, metavar="Geolocation")
subparsersPlanAddMain = subparsersPlanAdd.add_argument_group("Map Url Option")
subparsersPlanAddMain.add_argument('--murl', help="Map URL", type=str, metavar="url")
subparsersPlanAddMain.add_argument('--mimg', help="map Image", type=str, metavar="Map Image")
subparsersPlanAddMain = subparsersPlanAdd.add_argument_group("Etc Options")
subparsersPlanAddMain.add_argument('--eid', help="User defined Event ID.", type=str, metavar="Event ID")
subparsersPlanAddMain.add_argument('--category', help="Category Id", type=str, metavar="category ID")
subparsersPlanAddMain.add_argument('--visibility', help="Visibility. default public.", choices=["public","private"], default="public")
subparsersPlanAddMain.add_argument('--sequence', help="Plan sequece", type=int, default=0, metavar="SequenceNumber")
subparsersPlanAddMain.add_argument('--transparency', help="Set Transparency. default opaque.", choices=["opaque","transparent"], default="opaque")
subparsersPlanAddMain.add_argument('--location', help="location", type=str)
subparsersPlanAddMain.add_argument('--description', help="Description", type=str)
subparsersPlanAdd.set_defaults(operationType="ADD")

if len(sys.argv) < 2:
    parser.parse_args(['-h'])   # Argparse Bug
else:
    args=parser.parse_args()
    print(args)
    if "USER" in args:
        if args.USER == None:
            parserUser.parse_args(['-h'])
            exit(0)
    elif "ORG" in args:
        if args.ORG == None:
            parserOrg.parse_args(['-h'])
            exit(0)
    elif "CAL" in args:
        if args.CAL == None:
            parserCal.parse_args(['-h'])
            exit(0)
    elif "PLAN" in args:
        if args.PLAN == None:
            parserPlan.parse_args(['-h'])
            exit(0)
    args.func(args)

    
    # args=parser.parse_args()
    # args.func(args)

# args=parser.parse_args()
# if not vars(args):
#     parser.print_usage()
# else:
#     args.func(args)