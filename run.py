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
        from common.auth import AuthByJWT
        print("Run Authorize by JWT")
        AuthByJWT(args)
    elif args.t == 'oauth':
        from common.auth import AuthByOAuth
        print("Run Authorize by OAuth")
        AuthByOAuth(args)

def callUserManage(args):
    print(args)
    token = getToken(args.t)
    
    from works.UserManage import UserManage
    App = UserManage(token)
    if args.operationType == 'QUERY':
        continueYN = "Y"
        coursor = args.c
        while continueYN == "Y":
            result = App.queryUser(args.m, args.d, args.n, coursor)
            pprint.pprint(result, indent = 2)
            if 'responseMetaData' in result:
                if 'nextCursor' in result['responseMetaData'] :
                    print("Show Next Page ? [y/n] : ")
                    continueYN = input()
                    continueYN = continueYN.upper()
                    print("Response : " + continueYN)
                    coursor = result['responseMetaData']['nextCursor']
            else:
                continueYN = "N"

def callOrgManage(args):
    print(args)
    token = getToken(args.t)
    
    from works.OrgManage import OrgManage
    App = OrgManage(token)
    if args.operationType == 'QUERY':
        continueYN = "Y"
        coursor = args.c
        while continueYN == "Y":
            result = App.queryOrg(args.o, args.d, args.n, coursor)
            pprint.pprint(result, indent = 2)
            if 'responseMetaData' in result:
                if 'nextCursor' in result['responseMetaData'] :
                    print("Show Next Page ? [y/n] : ")
                    continueYN = input()
                    continueYN = continueYN.upper()
                    print("Response : " + continueYN)
                    coursor = result['responseMetaData']['nextCursor']
            else:
                continueYN = "N"

def callCalManage(args):
    print(args)
    token = getToken(args.t)
    
    from works.CalManage import CalManage
    App = CalManage(token)
    if args.operationType == 'QUERY':
        continueYN = "Y"
        coursor = args.c
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
    print(args)
    token = getToken(args.t)
    
    from works.PlanManage import PlanManage
    App = PlanManage(token)
    if args.operationType == 'QUERY':
        continueYN = "Y"
        while continueYN == "Y":
            result = App.queryPlan(args.m, args.cid, args.e, args.targetym)
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

parser = argparse.ArgumentParser(description = "WORKS | WORKSPLACE API Management Program V2")
subparsers = parser.add_subparsers(help="Description", required=True)

# Auth
parserAuth = subparsers.add_parser('auth', help="Authrization Step")
parserAuth.add_argument('-t', help="Auth type. Required", choices=["oauth","jwt"], required=True)
parserAuth.add_argument('-c', help="Required oauth|jwt Both.",type=str, required=True, metavar="Client ID")
parserAuth.add_argument('-s', help="Required oauth|jwt Both", type=str, required=True, metavar="Secret Key")
parserAuth.add_argument('-o', help="Required oauth|jwt Both", nargs="*", required=True, metavar="priv")
parserAuth.add_argument('-f', help="Required oauth|jwt Both. Default 'ak.token'.", type=str, default="ak.token", metavar="filename")
parserAuth.add_argument('-k', help="Required jwt", type=str, metavar="Private key file")
parserAuth.add_argument('-a', help="Required jwt", type=str, metavar="Service account")
parserAuth.add_argument('-d', help="Required oauth.", type=str, metavar="Domain")
parserAuth.add_argument('-r', help="Required oauth", type=str, metavar="Redirect URL for auth")
parserAuth.set_defaults(func=callAuthorizationStep)

# UserMangement
parserUser = subparsers.add_parser('user', help="User Management")
parserUser.set_defaults(func=callUserManage)
subparsersUser = parserUser.add_subparsers(help="Description")
# UserManagement - Query
subparsersUserQuery = subparsersUser.add_parser('query', help="Query User(s)")
subparsersUserQuery.add_argument('-t', help="Access token file. default ak.token", type=str, metavar="Filename", default="ak.token")
subparsersUserQuery.add_argument('-m', help="Members Email or ID", type=str, metavar="Email|Id")
subparsersUserQuery.add_argument('-d', help="Domain Id", type=int, metavar="domain")
subparsersUserQuery.add_argument('-n', help="Number of print, Default 100", type=int, default=100, metavar="number")
subparsersUserQuery.add_argument('-c', help="Next page cursor", type=str, metavar="cursor")
subparsersUserQuery.set_defaults(operationType="QUERY")
# UserManagement - add
subparsersUserAdd = subparsersUser.add_parser('add', help="Add User")
subparsersUserAdd.set_defaults(operationType="ADD")
# UserManagement - Query
subparsersUserDelete = subparsersUser.add_parser('delete', help="Delete User")
subparsersUserDelete.set_defaults(operationType="DELETE")
# UserManagement - Query
subparsersUserUpdate = subparsersUser.add_parser('update', help="Update Users")
subparsersUserUpdate.set_defaults(operationType="UPDATE")


# OrgManagement
parserOrg = subparsers.add_parser('org', help="Organization Management")
parserOrg.set_defaults(func=callOrgManage)
subparsersOrg = parserOrg.add_subparsers(help="Description")
# OrgManagement - Query
subparsersOrgQuery = subparsersOrg.add_parser('query', help="Query Orgs")
subparsersOrgQuery.add_argument('-t', help="Access token file. default ak.token", type=str, metavar="Filename", default="ak.token")
subparsersOrgQuery.add_argument('-o', help="Org unit Id", type=str, metavar="Org Unit ID")
subparsersOrgQuery.add_argument('-d', help="Domain Id", type=int, metavar="domain")
subparsersOrgQuery.add_argument('-n', help="Number of print, Default 100", type=int, default=100, metavar="number")
subparsersOrgQuery.add_argument('-c', help="Next page cursor", type=str, metavar="cursor")
subparsersOrgQuery.set_defaults(operationType="QUERY")
# OrgManagement - add
subparsersOrgAdd = subparsersOrg.add_parser('add', help="Add User")
subparsersOrgAdd.set_defaults(operationType="ADD")
# OrgManagement - Query
subparsersOrgDelete = subparsersOrg.add_parser('delete', help="Delete User")
subparsersOrgDelete.set_defaults(operationType="DELETE")
# OrgManagement - Query
subparsersOrgUpdate = subparsersOrg.add_parser('update', help="Update Users")
subparsersOrgUpdate.set_defaults(operationType="UPDATE")

# CalendarManagement
parserCal = subparsers.add_parser('cal', help="Calendar Management")
parserCal.set_defaults(func=callCalManage)
subparsersCal = parserCal.add_subparsers(help="Description")
subparsersCalQuery = subparsersCal.add_parser('query', help="Calendar List Query")
subparsersCalQueryMain = subparsersCalQuery.add_argument_group('Choose Personal or Shared Calendar')
subparsersCalQueryExGroup = subparsersCalQueryMain.add_mutually_exclusive_group(required=True)
subparsersCalQueryExGroup.add_argument('-p', help="Personal Calendar.", action="store_true")
subparsersCalQueryExGroup.add_argument('-s', help="Share Calendar.", action="store_true")
subparsersCalQueryMain = subparsersCalQuery.add_argument_group("Commonly Use Options")
subparsersCalQueryMain.add_argument('-t', help="Access token file. default ak.token", type=str, metavar="Filename", default="ak.token")
subparsersCalQueryMain.add_argument('-m', help="member's Email or ID", type=str, metavar="Email|ID")
subparsersCalQueryMain.add_argument('-cid', help="Calendar ID", type=str, metavar="Calendar ID")
subparsersCalQueryMain.add_argument('-c', help="cusrsor ID", type=str, metavar="Coursor ID")
subparsersCalQuery.set_defaults(operationType="QUERY")

# Plan Management
parserPlan = subparsers.add_parser('plan', help="Plan Management")
parserPlan.set_defaults(func=callPlanManage)
subparsersPlan = parserPlan.add_subparsers(help="Description")
subparsersPlanQuery = subparsersPlan.add_parser('query', help="Plan Query")
subparsersPlanQueryMain = subparsersPlanQuery.add_argument_group("Common Options")
subparsersPlanQueryMain.add_argument('-m', help="member's Email or ID", type=str, metavar="Email|ID", required=True)
subparsersPlanQueryMain = subparsersPlanQuery.add_argument_group("Options")
subparsersPlanQueryMain.add_argument('-t', help="Access token file. default ak.token", type=str, metavar="Filename", default="ak.token")
subparsersPlanQueryMain.add_argument('-cid', help="Calendar ID. If ommit, Query member's default calendar", type=str, metavar="Calendar ID")
subparsersPlanQueryMain.add_argument('-e', help="Event ID. If ommit, List Plans.", type=str, metavar="Event ID")
subparsersPlanQueryMain.add_argument('-targetym', help="Query Year Month. Ex) YYYY-MM. Set when -e ommitted.", type=str, metavar="YYYY-MM")
subparsersPlanQuery.set_defaults(operationType="QUERY")


if len(sys.argv) < 2:
    parser.parse_args(['-h'])   # Argparse Bug
else:
    args=parser.parse_args()
    args.func(args)

# args=parser.parse_args()
# if not vars(args):
#     parser.print_usage()
# else:
#     args.func(args)