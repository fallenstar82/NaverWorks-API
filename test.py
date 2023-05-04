import worksapi
import csv
import pprint
import json
# Access Token Open.
with open ('ak.token','r') as f:
        AccToken = f.read()

# # 조직 추가 부분.
# # TSV File
# # 조직명 \t 상위조직KEY
# with open ('orglist.txt','r') as t:
#         tDocu = csv.reader(t, delimiter='\t')
#         for row in tDocu:
#                 worksapi.postOrganization(domainId=229952, orgUnitName=row[0], parentOrgId=row[1],AccToken=AccToken, orgEmail=None, displayLevel=None, jsonFormat=True, externalKey=None)


# # 사용자 추가 부분.
# # TSV File
# # 회사메일 개인메일 이름 성 전화번호 회사조직 
# with open ('userlist3.txt','r') as t:
#         tUser = csv.reader(t, delimiter='\t')
#         for row in tUser:
#                 result = worksapi.postUserInfo('post',domainId=229952,extKey=None,
#                                       email=row[0],
#                                       pemail=row[1],
#                                       firstName=row[2],
#                                       lastName=row[3],
#                                       cellPhone=row[4],
#                                       domainLists=None,
#                                       orgUnitLists=[[row[5]]],
#                                       isSSO=True,
#                                       passWordPolicy=None,
#                                       passWord=None,
#                                       AccToken=AccToken,
#                                       )
#                 if 'code' not in result:
#                        username = ("" if result["userName"]["lastName"] == None else result["userName"]["lastName"]) + ("" if result["userName"]["firstName"] == None else result["userName"]["firstName"])
#                        print("DATA : %-50s %-20s %-50s %-20s" % (result["userId"], 
#                                                                  username,
#                                                                  result["email"],
#                                                                  result["cellPhone"]))
#                 else:
#                    pprint.pprint(result)
                        
                
# Group 추가 분

result = worksapi.getUserCalendarLists('jeongheon.lee@goodusdata.by-works.com', False, AccToken)
pprint.pprint(result, indent=2)