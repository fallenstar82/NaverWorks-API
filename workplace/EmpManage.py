import requests
import sys, os
import pprint

class EmpManage:
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

    def deleteEmployee(self, empExternalKey : str):
        self.timeStamp = self.authApp.getTimeStamp()
        extUrl = self.extUrl + "/employee" + "/" + empExternalKey

        baseUrl = self.baseUrl + extUrl

        signature = self.authApp.getSignature('DELETE', self.accessKey, self.secretKey, extUrl, self.timeStamp)

        headers = {
            "x-ncp-apigw-timestamp" : self.timeStamp,
            "x-ncp-iam-access-key" : self.accessKey,
            "x-ncp-apigw-signature-v2" : signature
        }

        return requests.delete(baseUrl, headers=headers).json()
    
    def modEmployee(self, empExternalKey : str, loginId : str, empEmail : str, joinYmd : str, empName : str, 
                    deptExtKey : str, cDeptExtKey : list, empType : str, passwordType : str, initPassword : str,
                    telePhone : str = None, cellPhone : str = None, birthYmd : str = None, genderCd : str = None,
                    empNick : str = None, locale : str = None, timeZone : str = None, zipCode :str = None,
                    address1 : str = None, address2 : str = None, grade : str = None, job : str = None):     
        self.timeStamp = self.authApp.getTimeStamp()
        self.extUrl = self.extUrl + "/employee" + "/" + empExternalKey
        params = {
            "loginId" : loginId,
            "emailAddress" : empEmail,
            "employYmd" : joinYmd,
            "name" : empName,
            "deptExternalKey" : deptExtKey,
            "concurrentDeptExternalKeys" : cDeptExtKey,
            "empTypeExternalKey" : empType,
            "passwordSettingType" : passwordType.upper(),
            "initializePassword" : initPassword
        }

        if telePhone:
            params["telephoneNo"] = telePhone
        if cellPhone:
            params["cellphoneNo"] = cellPhone
        if birthYmd:
            params["birthYmd"] = birthYmd
        if genderCd:
            params["genderCd"] = genderCd.upper()
        if empNick:
            params["empNick"] = empNick
        if locale:
            params["localeTypeCd"] = locale
        if timeZone:
            params["tmznTypeCd"] = timeZone
        if zipCode:
            params["zipCode"] = zipCode
        if address1:
            params["address"] = address1
        if address2:
            params["addressDetail"] = address2
        if grade:
            params["gradeCdExternalKey"] = grade
        if job:
            params["jobCdExternalKey"] = job

        self.baseUrl = self.baseUrl + self.extUrl

        signature = self.authApp.getSignature('PUT', self.accessKey, self.secretKey, self.extUrl, self.timeStamp)

        headers = {
            "x-ncp-apigw-timestamp" : self.timeStamp,
            "x-ncp-iam-access-key" : self.accessKey,
            "x-ncp-apigw-signature-v2" : signature
        }

        return requests.put(self.baseUrl, headers=headers, json=params).json()
        
    def addEmployee(self, empExternalKey : str, loginId : str, empEmail : str, joinYmd : str, empName : str, 
                    deptExtKey : str, cDeptExtKey : list, empType : str, passwordType : str, initPassword : str,
                    telePhone : str = None, cellPhone : str = None, birthYmd : str = None, genderCd : str = None,
                    empNick : str = None, locale : str = None, timeZone : str = None, zipCode :str = None,
                    address1 : str = None, address2 : str = None, grade : str = None, job : str = None):  
        self.timeStamp = self.authApp.getTimeStamp()
        extUrl = self.extUrl + "/employee" + "/" + empExternalKey
        params = {
            "loginId" : loginId,
            "emailAddress" : empEmail,
            "employYmd" : joinYmd,
            "name" : empName,
            "deptExternalKey" : deptExtKey,
            "concurrentDeptExternalKeys" : cDeptExtKey,
            "empTypeExternalKey" : empType,
            "passwordSettingType" : passwordType.upper(),
            "initializePassword" : initPassword
        }

        if telePhone:
            params["telephoneNo"] = telePhone
        if cellPhone:
            params["cellphoneNo"] = cellPhone
        if birthYmd:
            params["birthYmd"] = birthYmd
        if genderCd:
            params["genderCd"] = genderCd.upper()
        if empNick:
            params["empNick"] = empNick
        if locale:
            params["localeTypeCd"] = locale
        if timeZone:
            params["tmznTypeCd"] = timeZone
        if zipCode:
            params["zipCode"] = zipCode
        if address1:
            params["address"] = address1
        if address2:
            params["addressDetail"] = address2
        if grade:
            params["gradeCdExternalKey"] = grade
        if job:
            params["jobCdExternalKey"] = job

        baseUrl = self.baseUrl + extUrl

        signature = self.authApp.getSignature('POST', self.accessKey, self.secretKey, extUrl, self.timeStamp)

        headers = {
            "x-ncp-apigw-timestamp" : self.timeStamp,
            "x-ncp-iam-access-key" : self.accessKey,
            "x-ncp-apigw-signature-v2" : signature
        }
        pprint.pprint(params, indent=2)
        return requests.post(baseUrl, headers=headers, json=params).json()

    def queryEmployees(self, empExternalKey : str, offset : int, limit : int):
        self.timeStamp = self.authApp.getTimeStamp()
        # external Key 가 없으면 조직 전체 리스트, 없으면 특정 조직 정보
        isList = True if empExternalKey == None else False
        params = {}

        # URL 조합하기
        # 리스트 : https://workplace.apigw.ntruss.com/organization/apigw/v2/company/{companyId}/employee
        # 특정   : https://workplace.apigw.ntruss.com/organization/apigw/v2/company/{companyId}/employee/{externalKey}
        extUrl = self.extUrl + "/employee" + (("/" + empExternalKey) if not isList else "")
        
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




