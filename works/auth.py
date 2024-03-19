import jwt
import requests
import webbrowser
from urllib.parse import urlencode
from works.HelpMessage import HelpMessage
from time import time

class AuthByJWT:
    mainCategroy = "Auth"
    operationCategory = "AuthByJWT"
    url = "https://auth.worksmobile.com/oauth2/v2.0/token"

    def __init__(self, args):
        if args.c == None or args.s == None or args.a == None or args.k == None or args.o == None:
            HelpMessage(self.mainCategroy, self.operationCategory)
        else:
            print(args)
            self.getToken(args.c, args.s, args.a, args.k, args.o, args.f if args.f != None else "ak.token")

    def getToken(self, clientId :str, clientSecret :str, serviceAccount :str, privKey :str, scope :str, outputFile = "ak.token"):
        # Private Key 
        with open(privKey, 'r') as f:
            loadPrivKey = f.read()
        
        # Scope Parsing
        loadScope = ""
        for x in range(0,len(scope)):
            loadScope += scope[x]+' '

        header = {
            "alg" : "RS256",
            "typ" : "JWT"
        }

        payload = {
        "iss": clientId,
        "sub": serviceAccount,
        "iat": int(time()),
        "exp": int(time())+3600
        }

        signed_jwt = jwt.encode(payload=payload, key=loadPrivKey, headers=header)        

        params = {
            "assertion": signed_jwt,
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "client_id": clientId,
            "client_secret": clientSecret,
            "scope": loadScope
        }

    
        result = requests.post(self.url, params=params, headers=header).json()
        if 'error_description' in result:
            print("ERROR DESCRIPTION : " + result["error_description"])
            print("ERROR : "+ result["error"])
        else:    
            print(result)
            print("####################################")
            print("# Access Token Generate Info       #")
            print("####################################")
            print("Parameter Using: ")
            print(" - Service Account: " + serviceAccount)
            print(" - Client ID      : " + clientId)
            print(" - Client Secret  : " + clientSecret)
            print(" - Private Key    : Secured. " )
            print(" - OAuth Scope    : " + loadScope)
            print(" - Token output   : " + outputFile)
            with open(outputFile, 'w') as f:
                f.write(result["access_token"])

class AuthByOAuth:
    mainCategory = "Auth"
    operationCategory = "AuthByOAuth"

    def __init__(self, args):
        if (args.c == None or args.r == None or args.o == None or args.s == None):
            HelpMessage(self.mainCategory, self.operationCategory)
        else:
            operationCategory = "AuthByWeb_Auth"
            url = "https://auth.worksmobile.com/oauth2/v2.0/authorize"
            if args.c == None or args.r == None or args.o == None:
                HelpMessage(self.mainCategory, operationCategory)
                exit(1)
            else:
                scopes = ''
                for x in range(0,len(args.o)):
                    scopes += args.o[x]+" "
                scopes = scopes.rstrip(" ")
                url = url+"?client_id="+args.c+"&redirect_uri="+args.r+"&scope="+scopes+"&response_type=code&state=CSRF"
                if args.d != None:
                    url = url+"&domain="+args.d
                webbrowser.open(url)
                print("| Attention ")
                print("+---------------------")
                print("Log in Works site and Check Access Code.")
                print("And type access code at here : ")
                authCode = input()

                url = "https://auth.worksmobile.com/oauth2/v2.0/token"
                headers = {
                    "Content-Type" : "application/x-www-form-urlencoded"
                }

                data = {
                    "code" : authCode,
                    "grant_type" : "authorization_code",
                    "client_id" : args.c,
                    "client_secret" : args.s,
                    "domain" : args.d if args.d != None else None
                }
                
                encoded_data = urlencode(data)
                result = requests.post(url, headers=headers, data=encoded_data).json()
                
                if 'error' in result:
                    print("Oauth Error")
                    print(" | ERROR : " + result["error"])
                    print(" | DESCRIPTION : " + result["error_description"])
                    exit(1)
                else:
                    outFile = args.f if args.f != None else 'ak.token'
                    
                    with open (outFile, 'w') as f:
                        f.write(result["access_token"])
                
                    print("####################################")
                    print("# OAuth Info                       #")
                    print("####################################")
                    print(" - OAuth Scope    : " + result["scope"])
                    print(" - Expires in     : " + result["expires_in"])
                    print(" - Token File     : " + outFile)