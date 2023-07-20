import webbrowser
import requests
from urllib.parse import urlencode
import argparse
import pprint
import json

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "NCP OAuth API", add_help=True)

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', help='Get Token with web browser', action='store_true')
    group.add_argument('-t', help='Get AccessToken using code', action='store_true')

    group = parser.add_argument_group("Common Options")
    group.add_argument('--client', help='Client ID')
    group.add_argument('--redirect', help='Redirect URI')
    group.add_argument('--scope', help='Privielge Scope', nargs='*')
    group.add_argument('--code', help='code')
    group.add_argument('--secret', help='Client Secret')
    group.add_argument('--domain', help="Domain Name. Required if using SSO. Using Lite plan, then Group name")

    args = parser.parse_args()
    print(args)

    
    
    if args.c:
        if args.client == None or args.redirect == None or args.scope == None:
            print("Parameters not set")
        else:
            url = "https://auth.worksmobile.com/oauth2/v2.0/authorize"
            scopes = ''
            for x in range(0,len(args.scope)):
                scopes += args.scope[x] + " "
            scopes = scopes.rstrip(" ")
            url = url+"?client_id="+args.client+"&redirect_uri="+args.redirect+"&scope="+scopes+"&response_type=code&state=CSRF"
            if args.domain != None:
                url = url+"&domain="+args.domain
            webbrowser.open(url)
            
    elif args.t:
        if args.code is None or args.client is None or args.secret is None:
            print("Parameters not set")
        else:
            url = "https://auth.worksmobile.com/oauth2/v2.0/token"
            headers = {
                "Content-Type" : "application/x-www-form-urlencoded"
            }

            data = {
                "code" : args.code,
                "grant_type" : "authorization_code",
                "client_id" : args.client,
                "client_secret" : args.secret,
                "domain" : args.domain
            }
            
            encoded_data = urlencode(data)
            result = requests.post(url, headers=headers, data=data).json()

            if 'error' in result:
                print("Oauth Error")
                print(" | ERROR : " + result["error"])
                print(" | DESCRIPTION : " + result["error_description"])
            else:               
                with open ('ak.token', 'w') as f:
                    f.write(result["access_token"])
                
                print("####################################")
                print("# OAuth Info                       #")
                print("####################################")
                print(" - OAuth Scope    : " + result["scope"])
                print(" - Expires in     : " + result["expires_in"])
                print(" - Token File     : ak.token")


# params = {
#     "client_id" : "df1vPzpc6IOmc6WOYySg",
#     "redirect_uri" : "http://localhost",
#     "scope" : "file",
#     "response_type" : "code",
#     "state" : "CSRF",
#     "domain" : "goodusdata.com"
# }

# url = "https://auth.worksmobile.com/oauth2/v2.0/authorize?client_id=df1vPzpc6IOmc6WOYySg&redirect_uri=http://db.goodusdata.com/imsi&scope=file&response_type=code&state=CSRF&domain=goodusdata.by-works.com"


# webbrowser.open(url)
# data = 
# code = parse("")
# grant_type = 
# result = requests.post('https://auth.worksmobile.com/oauth2/v2.0/token',
#                        headers={ "Content-Type" : "https://auth.worksmobile.com/oauth2/v2.0/token"},
#                        data={
#                            "code" : ""
#                        }
#                        )