class HelpMessage: 
    
    helpMessage = {
        "Auth" : {
            "AuthByJWT" : {
                "c" : "Required - Client ID",
                "s" : "Required - Client Secret",
                "a" : "Required - Service Account",
                "k" : "Required - Private Key",
                "o" : "Required - Privilege Scope",
                "f" : "Optional - Token out file"
            },
            "AuthByOAuth" : {
                "c" : "Required - Client ID",
                "s" : "Required - Client Secret",
                "r" : "Required - Redirect URL",
                "o" : "Required - Privilege Scope",
                "d" : "Optional - Domain",
                "f" : "Optional - Token out file"
            }
        }
    }
    
    def __init__(self, mainCategory, operationCategory):
        for listOption in self.helpMessage[mainCategory][operationCategory].keys():
            print("%5s : %s" % (listOption, self.helpMessage[mainCategory][operationCategory][listOption]))
