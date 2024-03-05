import worksapi
import csv
import pprint
from time import sleep
import json
import time
# Access Token Open.

## Access Token
with open ('ak.token','r') as f:
        AccToken = f.read()

## Global Variables
domainId = 300097142

# # 조직 추가 부분.
# # TSV File
# # 조직명 \t 상위조직KEY
# with open ('orglist.txt','r') as t:
#         tDocu = csv.reader(t, delimiter='\t')
#         for row in tDocu:
#                 worksapi.postOrganization(domainId=domainId, orgUnitName=row[0], parentOrgId=row[1],AccToken=AccToken, orgEmail=None, displayLevel=None, jsonFormat=True, externalKey=None)


# 사용자 추가 부분.
# TSV File
# 회사메일 개인메일 이름 성 전화번호 회사조직 회사조직 회사조직...
# with open ('user_add_error_230831.txt', 'r', encoding='euc-kr') as t:
#         tUser = csv.reader(t, delimiter='\t')
#         for row in tUser:
#                 orgUList=list()
#                 for x in range(5,len(row)):
#                         if row[x] == "":
#                                 break
#                         else:
#                                 orgUList.append(row[x])
#                 result = worksapi.postUserInfo('post',domainId=domainId,extKey=None,
#                                       email=row[0]+"@korec.by-works.com",
#                                       pemail=row[1],
#                                       firstName=row[2],
#                                       lastName=row[3],
#                                       cellPhone=row[4],
#                                       domainLists=None,
#                                       orgUnitLists=[orgUList],
#                                       isSSO=False,
#                                       passWordPolicy='MEMBER',
#                                       passWord='eduart12@!',
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
#                 sleep(0.5)


# # 강사 캘린더 공유 권한 적용
# # cid member member member ...
# with open ('calendar_share_230831.txt', 'r') as t:
#         tCal = csv.reader(t, delimiter='\t')
#         member=list()
#         for row in tCal:
#                 cid = row[0]
#                 for cnt in range(1, len(row)):
#                         member.append(
#                                 [row[cnt], "USER","EVENT_READ"]
#                         )
#                 result=worksapi.modifyUserCalendar(
#                         None, row[0], None, member, None, None, AccToken
#                 )
#                 pprint.pprint(result, indent=2)
#                 sleep(0.3)

                
# Group 추가 분
# TSV File
# 그룹명 관리자리스트(,) 사용자 사용자 사용자 ...
# with open ('Test2.txt','r') as t:
#         group = csv.reader(t, delimiter='\t')
#         for row in group:
#                 adminList = row[1].replace(" ","").split(",")
#                 memList = []
#                 # Member (Col C to E)
#                 for memCnt in range(2,5):
#                         if row[memCnt] == "":
#                                 break
#                         else:
#                                 memList.append([row[memCnt].replace(" ", ""), 'USER'])
#                 # OrgUnit Member (Col F to J)
#                 for memCnt in range(5, len(row)):
#                         if row[memCnt] == "":
#                                 break
#                         else:
#                                 memList.append([row[memCnt].replace(" ",""), 'ORGUNIT'])

#                 result = worksapi.postGroup(
#                         domainId = domainId,
#                         groupName = row[0],
#                         description = None,
#                         serviceNotification = False,
#                         serviceManagement = False,
#                         externalKey = None,
#                         administrators = adminList,
#                         useMessage = True,
#                         useNote = False,
#                         useCalendar = True,
#                         useTask = False,
#                         useFolder = False,
#                         useMail = False,
#                         groupEmail = None,
#                         members = memList,
#                         AccToken = AccToken
#                 )
#                 pprint.pprint(result, indent=2)

# Group member 수정
# TSV File
# GID USER USER USER(admin) USER ...
# with open ('group_mem_modify_error.txt', 'r') as t:
#         group = csv.reader(t, delimiter='\t')
#         coolDownCount = 0
#         processingCount = 0
#         for row in group:
#                 processingCount = processingCount + 1
#                 coolDownCount = coolDownCount + 1
#                 if coolDownCount > 10:
#                         print("API Cooling down for 5 sec")
#                         sleep(5)
#                         coolDownCount = 0
                
#                 groupId = row[0]
#                 memList = list()
#                 for memCnt in range(1,len(row)):
#                         if row[memCnt] == "" or row[memCnt] == None:
#                                 continue
#                         else:
#                                 memList.append(
#                                         [row[memCnt].replace(" ",""), "USER"]
#                                 )
#                 print("PROCESSING " + str(processingCount) + " : " + groupId + " - RESULT :", end=" ")
#                 result = worksapi.modifyGroup(
#                         domainId,
#                         groupId,
#                         None,
#                         None,
#                         None,
#                         None,
#                         None,
#                         None,
#                         None,
#                         None,
#                         None,
#                         None,
#                         None,
#                         None,
#                         memList,
#                         None,
#                         AccToken
#                 )

#                 if 'code' in result:
#                         print("FAILED")
#                         print(" -- CODE : " + result['code'] + " / DESC : " + result['description'])
#                 else:
#                         print("SUCCEED")
#                 sleep(0.2)



                

# # 폴더 생성 및 권한 부여
# # 경로(파일아이디) 폴더명 아이디 아이디 아이디 ...
# #   요건 : 멤버 1 ~ 3 은 고정으로 해당 폴더에 대한 Write 권한. 그 외 모두 읽기
# with open ('folder_errors.txt', 'r', encoding='euc-kr') as t:
#         folder = csv.reader(t, delimiter='\t')
#         i = 0
#         for row in folder:
#                 if i == 5:
#                         print("INFO : API Cooling Down for 10 Seconds")
#                         sleep(10)
#                         i = 1
#                 else:
#                         i = i + 1

#                 # 우선 생성
#                 result = worksapi.manageShareDriveObject(
#                         '@2001000000338803',
#                         'create',
#                         row[0],
#                         row[1],
#                         False,
#                         None,
#                         None,
#                         AccToken
#                 )
#                 if 'code' in result:
#                         print("ERROR : Creating " + row[1] + " failer. code is " + result['code'])
#                         continue
#                 print("INFO : CREATED :   " + result["fileId"] + "   " + result["filePath"])
#                 fileId = result["fileId"]
#                 fileNm = result["filePath"]
                
#                 sleep(0.5)
#                 # WRITE 권한 부여 (1~3)
#                 print("INFO : Granting Write privileges on " + fileNm + "(" + fileId +")")
#                 for memCnt in range(2,5):
#                         result = worksapi.manageShareDrivePrivs(
#                                 '@2001000000338803',
#                                 'create',
#                                 fileId,
#                                 None,
#                                 False,
#                                 row[memCnt],
#                                 'write',
#                                 AccToken
#                         )

#                         if 'code' in result:
#                                 print("ERROR : " + row[memCnt] + "    " + fileId + "   while creating  Write Privs. code is " + result['code'])
#                         sleep(0.5)
                
#                 # READ 권한 부여 (4 ~)
#                 print("INFO : Granting Read privileges on " + fileNm + "(" + fileId +")")
#                 for memCnt in range(5,len(row)):
#                         if row[memCnt] == "":
#                                  break
#                         result = worksapi.manageShareDrivePrivs(
#                                 '@2001000000338803',
#                                 'create',
#                                 fileId,
#                                 None,
#                                 None,
#                                 row[memCnt],
#                                 'read',
#                                 AccToken
#                         )

#                         if 'code' in result:
#                                 print("ERROR : " + row[memCnt] + "\t" + fileId + "\twhile creating Read Privs. code is " + result['code'])
#                         sleep(0.5)
                
#                 # 권한 조회
#                 result = worksapi.manageShareDrivePrivs(
#                         '@2001000000338803',
#                         'query',
#                         fileId,
#                         None,
#                         False,
#                         None,
#                         None,
#                         AccToken
#                 )

#                 for memCnt in range(0,len(result["permissions"])):
#                         print(result["permissions"][memCnt]["type"] + " priv on '" + fileNm + "(" + fileId +")' TO " + result["permissions"][memCnt]["userName"] + "(" + result["permissions"][memCnt]["userType"] + ")")
                        
#                 sleep(2)


# 폴더 권한 변경
with open ('driv_privs_modify.txt', 'r') as t:
        sch = csv.reader(t, delimiter='\t')
        for row in sch:
                fileId = row[0]
                for writerCnt in range(2, len(row)):
                        if row[writerCnt] == "" or row[writerCnt] == None:
                                continue
                        if writerCnt < 32:
                                privType = 'write'
                        else:
                                privType = 'read'

                        print("PROCESSING : GRANTING " + fileId + " " + privType)
                        result = worksapi.manageShareDrivePrivs(
                                '@2001000000338803',
                                'create',
                                fileId,
                                None,
                                None,
                                row[writerCnt],
                                privType,
                                AccToken
                        )

                        if 'code' in result:
                                print("ERROR : " + row[writerCnt] + "\t" + fileId + "\twhile creating Read Privs. code is " + result['code'])
                        
                        sleep(0.05)
                
                result = worksapi.manageShareDrivePrivs(
                        '@2001000000338803',
                        'query',
                        fileId,
                        None,
                        False,
                        None,
                        None,
                        AccToken
                )
                pprint.pprint(result, indent=2)
                sleep(5)
                
# 일정 추가 부분
# # 교육부 포맷
# # 사용자ID(메인유저) 캘린더아이디 위치 일정명 시작일자 종료일자 초대맴버1 초대맴버2 반복요일 반복종료일 휴강일1, 휴강일2, .., 휴강일n
# with open ('schedule_error_retry_230831.txt','r',encoding='euc-kr') as t:
#         coolDown = 0
#         totalCnt = 0
#         attendees = list()
#         sch = csv.reader(t, delimiter='\t')
#         for row in sch:
#                 totalCnt = totalCnt + 1
#                 if coolDown == 10:
#                         print("API Cooling Down for 10 Sec")
#                         coolDown = 0
#                         sleep(10)
#                 planType = 'DATE'
#                 userId          = "admin@korec.by-works.com"
#                 calendarId      = row[0]
#                 planLocation    = row[1]
#                 planName        = row[2]
#                 planStartDate   = row[3]
#                 planEndDate     = row[4]
#                 attendeesRaw    = row[5].replace(' ','').split(',')
#                 attendees=list()
#                 for attendeesNum in range(len(attendeesRaw)):
#                         attendees.append ([
#                                 attendeesRaw[attendeesNum],
#                                 'ACCEPTED'
#                         ])
#                 repeatDays       = row[6].replace(' ','').replace("월","MO").replace("화","TU").replace("수","WE").replace("목","TH").replace("금","FR").replace("토","SA").replace("일","SU")
#                 repeatEnds       = row[7].replace(' ','').replace('-','') + 'T235959Z'
#                 planExcept       = list()
#                 for cnt in range(8, len(row)):
#                         if (row[8] == "" or row[8] == None):
#                                 planExcept == None
#                                 break
#                         elif (row[cnt] == ""):
#                                 break
#                         planExcept.append(row[cnt].replace('-',''))

#                 print("PROCESSING " + str(totalCnt) + ": " + calendarId + " - " + planName + " - " + planLocation +" :", end= " ")
#                 result = worksapi.postPlanCalendar(
#                         userId,
#                         calendarId,
#                         planName,
#                         None,
#                         planLocation,
#                         planType,
#                         planStartDate,
#                         planEndDate,
#                         "Asis/Seoul",
#                         attendees,
#                         True,
#                         1,
#                         "WEEKLY",
#                         repeatDays,
#                         None,
#                         repeatEnds,
#                         planExcept,
#                         AccToken
#                 )
#                 if 'code' in result:
#                         print("FAIL")
#                         print(" - CODE : " + result['code'] + " - " + result['description'])
#                 else:
#                         print("SUCCEED")
#                 coolDown = coolDown + 1
#                 sleep(0.4)


                # pprint.pprint(result, indent=2)


# result = worksapi.getUserCalendarLists('jeongheon.lee@goodusdata.by-works.com', False, AccToken)
# pprint.pprint(result, indent=2)