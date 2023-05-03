import worksapi
import csv

# Access Token Open.
with open ('ak.token','r') as f:
        AccToken = f.read()

# 조직 추가 부분.
# TSV File
# 조직명 \t 상위조직KEY
with open ('orglist.txt','r') as t:
        tDocu = csv.reader(t, delimiter='\t')
        for row in tDocu:
                worksapi.postOrganization(domainId=229952, orgUnitName=row[0], parentOrgId=row[1],AccToken=AccToken, orgEmail=None, displayLevel=None, jsonFormat=True, externalKey=None)
                print(row)

# 사용자 추가 부분.
# TSV File
# 회사메일 개인메일 이름 성 회사조직 
with open ('userlist.txt','r') as t:
        tUser = csv.reader(t, delimiter='\t')
        for row in tUser:
                worksapi.postUserInfo('post',domainId=229952,extKey=None,
                                      email=row[0],
                                      pemail=row[1],
                                      firstName=row[2],
                                      lastName=row[3],
                                      domainLists=None,
                                      orgUnitLists=[[row[4]]],
                                      sso
                                      )
                        


                

# worksapi.getUserCalendarLists('jeongheon.lee@goodusdata.by-works.com', False, AccToken)