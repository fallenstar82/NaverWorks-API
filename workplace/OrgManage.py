import requests
import sys, os

class OrgManage:
    accessKey = str
    secretKey = str
    companyId = str
    timeStamp = str
    baseUrl   = "https://workplace.apigw.ntruss.com"
    extUrl    = "/organization/apigw/v2/company/"
    
    def __init__(self, accessKey : str, secretKey : str, companyId : str):
        sys.path.append(os.path.dirname(__file__))
        from auth import Auth
        self.accessKey = accessKey
        self.secretKey = secretKey
        self.companyId = companyId
        self.extUrl    = self.extUrl + companyId
        self.authApp = Auth()

    def modOrganization(self, orgExternalKey : str, orgName : str, order : str, parentOrgExtKey : str = "#", 
                        deptNo : str = None, parentDeptNo :str = None, orgEmail : str = None, receiveExternalMail : bool = False):
        self.timeStamp = self.authApp.getTimeStamp()
        extUrl = self.extUrl + "/department/" + orgExternalKey

        params = {
            "name" : orgName,
            "deptExternalKey" : orgExternalKey,
            "deptNo" : deptNo,
            "dispOrd" : order,
            "deptEmailAddress" : orgEmail,
            "externalEmailReceiveYN" : receiveExternalMail,
            "parentDeptExternalKey" : parentOrgExtKey,
            "parentDeptNo" : parentDeptNo
        }

        baseUrl = self.baseUrl + extUrl

        signature = self.authApp.getSignature("PUT", self.accessKey, self.secretKey, extUrl, self.timeStamp)

        headers = {
            "x-ncp-apigw-timestamp" : self.timeStamp,
            "x-ncp-iam-access-key" : self.accessKey,
            "x-ncp-apigw-signature-v2" : signature,
            "Content-Type" : "application/json"
        }
        
        return requests.put(baseUrl, headers=headers, json=params).json()

    def addOrganization(self, orgExternalKey : str, orgName : str, order : str, parentOrgExtKey : str = "#", 
                        orgEmail : str = None, receiveExternalMail : bool = False):
        self.timeStamp = self.authApp.getTimeStamp()
        
        extUrl = self.extUrl + "/department/" + orgExternalKey
        
        params = {
            "name" : orgName,
            "deptExternalKey" : orgExternalKey,
            "dispOrd" : order,
            "deptEmailAddress" : orgEmail,
            "externalEmailReceiveYN" : receiveExternalMail,
            "parentDeptExternalKey" : parentOrgExtKey
        }

        baseUrl = self.baseUrl + extUrl
        signature = self.authApp.getSignature("POST", self.accessKey, self.secretKey, extUrl, self.timeStamp)

        headers = {
            "x-ncp-apigw-timestamp" : self.timeStamp,
            "x-ncp-iam-access-key" : self.accessKey,
            "x-ncp-apigw-signature-v2" : signature
        }

        return requests.post(baseUrl, headers=headers, json=params).json()

    def queryOrganization(self, orgExternalKey : str, offset : int, limit : int):
        self.timeStamp = self.authApp.getTimeStamp()
        # external Key 가 없으면 조직 전체 리스트, 없으면 특정 조직 정보
        isList = True if orgExternalKey == None else False
        params = {}

        # URL 조합하기
        # 리스트 : https://workplace.apigw.ntruss.com/organization/apigw/v2/company/{companyId}/department
        # 특정   : https://workplace.apigw.ntruss.com/organization/apigw/v2/company/{companyId}/department/{externalKey}
        extUrl = self.extUrl + "/department" + (("/" + orgExternalKey) if not isList else "")
        
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
        baseUrl = self.baseUrl + extUrl
        
        signature = self.authApp.getSignature('GET', self.accessKey, self.secretKey, extUrl, self.timeStamp)

        headers = {
            "x-ncp-apigw-timestamp" : self.timeStamp,
            "x-ncp-iam-access-key" : self.accessKey,
            "x-ncp-apigw-signature-v2" : signature
        }

        return requests.get(baseUrl, headers=headers, json=params).json()




