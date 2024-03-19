import requests
import sys, os

class GrdManage:
    accessKey = str
    secretKey = str
    companyId = str
    timeStamp = str
    baseUrl   = "https://workplace.apigw.ntruss.com"
    extUrl    = "/organization/apigw/v2/company/"
    
    def __init__(self, accessKey : str, secretKey : str, companyId : str):
        if os.path.dirname(__file__) not in sys.path:
            sys.path.append(os.path.dirname(__file__))
        from auth import Auth
        self.accessKey = accessKey
        self.secretKey = secretKey
        self.companyId = companyId
        self.extUrl    = self.extUrl + companyId
        self.authApp = Auth()

    def queryGrade(self, externalKey : str, offset : int, limit : int):
        self.timeStamp = self.authApp.getTimeStamp()
        # external Key 가 없으면 조직 전체 리스트, 없으면 특정 조직 정보
        isList = True if externalKey == None else False
        params = {}

        # URL 조합하기
        # 리스트 : https://workplace.apigw.ntruss.com/organization/apigw/v2/company/{companyId}/grade
        # 특정   : https://workplace.apigw.ntruss.com/organization/apigw/v2/company/{companyId}/grade/{externalKey}
        # urlParam = "/organization/apigw/v2/company/" + self.companyId + "/employee" + (("/" + externalKey) if not isOrgList else "")
        extUrl = self.extUrl + "/grade" + (("/" + externalKey) if not isList else "")
        
        # Url Query Parameter 존재 확인
        if isList:
            if offset != None and limit != None:
                extUrl = extUrl + "?offset=" + str(offset) + "&limit=" + str(limit)
                params.update({ "offset" : offset, "limit" : limit})
            elif offset != None and limit == None:
                extUrl = extUrl + "?offset=" + str(offset)
                params.update({ "offset" : offset})
            elif offset == None and limit != None:
                extUrl = extUrl + "?limit=" + str(limit)
                params.update({ "limit" : limit})

        ## 병합
        self.baseUrl = self.baseUrl + self.extUrl
        
        signature = self.authApp.getSignature('GET', self.accessKey, self.secretKey, self.extUrl, self.timeStamp)

        headers = {
            "x-ncp-apigw-timestamp" : self.timeStamp,
            "x-ncp-iam-access-key" : self.accessKey,
            "x-ncp-apigw-signature-v2" : signature
        }

        return requests.get(self.baseUrl, headers=headers, json=params).json()




