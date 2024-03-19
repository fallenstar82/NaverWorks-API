import hashlib
import hmac
import base64
import time
import pprint
import requests

class Auth:
    accessKey : str
    secretKey : str
    url       : str
    timeStamp : str
    method    : str

    def __init__(self):
        pass

    def setMethod(self, method : str):
        self.method = method

    def setAccessKey(self, accessKey : str):
        self.accessKey = accessKey
    
    def setSecretKey(self, secretKey : str):
        self.secretKey = secretKey

    def setUrl(self, url : str):
        self.url = url

    def getTimeStamp(self):
        return str(int(time.time() * 1000))
	
    def	getSignature(self, method, accessKey : str, secretKey : str, uri : str, timeStamp : str):
        secretKey = bytes(secretKey, 'UTF-8')				# secret key (from portal or Sub Account)

        message = method + " " + uri + "\n" + timeStamp + "\n" + accessKey
        message = bytes(message, 'UTF-8')
        signingKey = base64.b64encode(hmac.new(secretKey, message, digestmod=hashlib.sha256).digest())
        
        return signingKey

# accessKey = '1M5SvLTWsq1JwQI0Pgsa'
# secretKey = 'bwNxqXXRVryork2uHTpU6ZEkIPypj16qQ994UURI'
# timeStamp = str(int(time.time() * 1000))
# companyId = 'c0dbf41b-2d10-4127-b90b-b90f096bad3f'

# url = 'https://workplace.apigw.ntruss.com'
# urlQuery = '/organization/apigw/v2/company/' + companyId + '/department'
# app = Auth()
# app.setUrl(urlQuery)
# app.setMethod('GET')
# app.setTimeStamp(timeStamp)
# app.setAccessKey(accessKey)
# app.setSecretKey(secretKey)

# headers = {
#     "x-ncp-apigw-timestamp" : timeStamp,
#     "x-ncp-iam-access-key"  : accessKey,
#     "x-ncp-apigw-signature-v2" : app.getSignature()
# }

# params = {
# }

# result = requests.get(headers=headers, url=url+urlQuery, json=params).json()
# pprint.pprint(result, indent=2)

