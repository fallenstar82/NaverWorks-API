import jwt
import requests
import json
import argparse
from time import time

def getToken() :
    header = {
        "alg":"RS256", 
        "typ":"JWT"
    }

    payload = {
        "iss" : "df1vPzpc6IOmc6WOYySg",
        "sub" : "x89pn.serviceaccount@goodusdata.by-works.com",
        "iat" : int(time()),
        "exp" : int(time())+3600
    }

    privkey = """MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCcoc8PNnJn0ZHx
gdj1YXxzx9aArCtFbiqpdRXy0xubSEIrkr5lU7r3B0dilYpXWNR5VaCMom13clIc
yluB/F7KlRv6PJwPZD2uTb+Qtc/kURbjujhTCMgV/s+ozTeUfTTq/o9HX6dt53Qb
2gh/f+edXB3oQyDaAHLam+k0yaZWdDfBef8c2BNQabuJpIPbrGVzHY5i3pzD3YHJ
WCdGQdK5w85Dewq7legjcIgt8b+u98TtHAbBaW3PW2YsL7c00a3RP0Jr9cwGJ5Y0
GH/LtW9xPQSADP46qiQZvcMVXi99biDfo8nrENAWVvSv9FQqxcPHmpanenescxtW
k6xppebvAgMBAAECggEBAImdcLrA74tfiYZSuzf8Sse+0CuFGQ+LV1hDUuFhsWOg
/OIjr7x+8EmRz5pCIKXVmfhwzvpAy0Si4JoDAJsYDICYuVgGYGb1f2vhS2ntE5ZZ
2G6EcnAhywnoMrLweuCvkQrWVTQ0Sno5XL4LtmOvEOQkxvIF6JsgwchoK2EBum9B
jidKZ3Rv2qzJMVZ1mj8ZBNWf3fsce0fpdFbIjIVREmboU3Rk7ST9tsbcq5zcgmlt
xHvwmALVgyFpntUHE8a3TEXs/GHvyo5xKLo4n80q1ePawlcorxq87Om+uHy0gCSI
ewFCxxM3DGHmIA1sc7avqWHHRjDmCDbnZf9K1tEO5mECgYEA8yBPpL5HCRWTytrr
HYIbBmKtoIir+bWFMASkS3aGHNIHKnxoUPaquQUx2u73BjiI1lTbCM1efWLi0Ocs
QASnqmgeEuodSU/6kNoNKbe6mGYdvL7ESlCpG7pTCuvUPUQAN1TAu6V+s3NuLafi
ILhrVrfhqvc2BpDLRrHotLihWgMCgYEApO0HgIVo59Cl96fGgOFjHZb4Pq9YZkA+
Vf/4+F07qtf8ZwrPfterBUUa8BJAkLYCmfiaP/hJTHptl21tj6ITDwkyiE6pqlwj
EMohajgkA5kbO8uxI0wr26bo9S56eGrdr7yoAvPKaurH52+W2K5lBmNkltu694hj
bfbqNzdZoaUCgYBV0z8qOd1bsJlGj/dVqFsf6u+97uE+ujx1Ef5pgUKgo+fRsK8m
fZ0QyWurDJZ5RLXRa40S02SawLCu7Bxr0PjbJ/wN00VZXvll7wOciXY+XDX9Lh6e
2VCJMEImZc+7fOjSn4GV/Dr44DOxvEUQJeoGZ80rDC+vK6gGocEzIsYavwKBgASp
wwWKQB4V0yt+belk9gV3KEu1b31soZaS5zo2gKJi+vr63kUK2gYLHyjci0DMNKSf
19SpM4FbENAwQuHFxl4td2VNPBTaCA/Id0tmjPYhFRkKuFZ0J+VNAdc02jefZec7
IVD8DaQaQU605AH6ZFba5pQxYEbxb0ZDrfmjsgAVAoGADKMC37kb7TmF/AlWgqxV
fUTPYNzmB5mc414UpIv5lpW8hP3cQh1ZNZX6MfFjP6T4EMeQR3bpQ8BFDwCnVQQp
CjYDyTzD4XRKM9+jq+ZLQtSxvVyKVBqP7D2C6NfLmEz4vNGYoNTX3sdVcdEt5MCx
DaQCb3kYWT8JqKOdVIzzRF4=
-----END PRIVATE KEY-----"""

    signed_jwt = jwt.encode(payload=payload, key=privkey, headers=header,algorithm='RS256')

    rparams = {
        "assertion" : signed_jwt,
        "grant_type" : "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "client_id" : "df1vPzpc6IOmc6WOYySg",
        "client_secret" : "bCUu3CSfRk",
        "scope" : "user calendar"
    }
    url = "https://auth.worksmobile.com/oauth2/v2.0/token"
    rheader = {
        "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8"
    }

    r = requests.post(url,params=rparams, headers=rheader).json()
    return r["access_token"]



def getUserInfo(userEmail, AccToken) :
    header = {
        "Authorization": "Bearer " + AccToken
    }

    url = "https://www.worksapis.com/v1.0/users/"+userEmail

    # Access token key : 'accessToken'
    return requests.get(url=url, headers=header).json()



def getUserCalendarPersonal(userId, AccToken) :
    header = {
        "Authorization": "Bearer " + AccToken
    }

    url = "https://www.worksapis.com/v1.0/users/" + userId + "/calendar-personals"

    # Retruning :: 'calendarPersonals' : [ 'calendarId','calendarName', 'isShowOnLNBList'(Boolean) ]
    return requests.get(url, headers=header).json()



def postCalendarPlan(userId, calendarId, eventComponents, AccToken) :
    header = {
        "Authorization" : "Bearer " + AccToken,
        "Content-Type" : "application/json"
    }

    url = "https://www.worksapis.com/v1.0/users/" + userId + "/calendars/" + calendarId + "/events"
    jeventComponents = json.dumps(eventComponents)
    
    return requests.post(url, headers=header, json=eventComponents)



def getCalendarPlan(userId, calendarId, param, AccToken) :
    header = {
        "Authorization" : "Bearer " + AccToken
    }

    url = "https://www.worksapis.com/v1.0/users/" + userId + "/calendars/" + calendarId + "/events"
    return requests.get(url, headers=header, params=param)

# AccToken = getToken()
# print(AccToken)




AccToken = "kr1AAABN9P8S2lERCc+q1opMblUIbzC27MLGKPs8PElOmH+vjVqutLfz37lgPAb+ItoiOqZXUbjpi2dlp1SfLyYnkthxLY/gnD6GCWhM3DXSYOXKbOE8pp7qsOvIclA/k04Whqmzltjy9oef2fwmBiMf2JreBWXxE/nwYSHou+FgL/4mVFDeB3c4UHhYWgSsUo2mw3iV0REOTa7evNkBM8RsPRZPcs7n0SKIu7Mj1cVfnYxOgJMh9jhYKThdL8/ovpkXSbB8maQR/dRzW7JjTuch8aizGxmmKRrgVi9jFv53vxXp3kMP77cjlxxMlZDzUrTuZpmPU0/Q4kD3B6cGCcrcTWmec/kOukWpQoEfv8MF39omI9lGjWvdYUetSt8DPlnYD8N2Sa/CY0STGQQy+WG7ey3LRpb4tETh6KTpaI4kx8cugCF"

# ## Getting UserId and Calendars ID
# userId = getUserInfo('jeongheon.lee@goodusdata.by-works.com', AccToken)["userId"]
# # CalId = getUserCalendarPersonal(userId, AccToken)
# # print(userId)
# # # Calendar Listup
# # for i in CalId['calendarPersonals'] :
# #     print("Calendar Name : " + i["calendarName"] + " // Calendar Id : " + i["calendarId"])

eventComponents = {
    "eventComponents" : [
        {
            "summary": "이게 제목인가?",
            "description" : "알아 뭐하게?",
            "location" : "밤새는 사무실",
            "start": {
                "dateTime" : "2023-04-21T20:00:00",
                "timeZone" : "Asia/Seoul"
            },
            "end": {
                "dateTime" : "2023-04-21T22:00:00",
                "timeZone" : "Asia/Seoul"
            },
            "transparency" : "OPAQUE",
            "visibility" : "PUBLIC",
            "categoryId" : "1",
            "sequence" : 1,
            "recurrence" : [
                "RRULE:FREQ=WEEKLY;INTERVAL=2;BYDAY=TH,FR;UNTIL=20230518T130000Z",
            ],
            "attendees" : [
                {
                    "email" : "sungwook.kim@goodusdata.by-works.com",
                    "displayName" : "킹왕짱",
                    "partstat" : "DECLINED",
                    "isOptional" : False,
                    "isResource" : False
                },
                {
                    "email" : "gyoungmin.gu@goodusdata.by-works.com",
                    "displayName" : "JWT 해메는자",
                    "partstat" : "NEEDS-ACTION",
                    "isOptional" : False,
                    "isResource" : False
                }
            ],
            "reminders" : [
                {
                    "method":"DISPLAY",
                    "trigger":"-PT1M"
                }
            ]
        }
    ]
}
userId = 'bbe234f2-5a1f-4a07-1a6e-03bbb2146ad1'
r = postCalendarPlan(userId, "27b4081f-4396-4c8b-bfce-1c810d2795da", eventComponents, AccToken)
print(r.text)

# # param = {
# #     "fromDateTime" : "2023-04-01T10:00:00%2B09:00",
# #     "untilDateTime" : "2023-04-30T00:00:00%2B09:00"
# # }

# # r = getCalendarPlan(userId, "27b4081f-4396-4c8b-bfce-1c810d2795da", param, AccToken)
# # print(r.text)





