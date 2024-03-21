# Works
# Overview

## 개요

- Naver Works 를 관리하기 위한 API 를 활용하여 Works 를 다루기 위함
- 최초 교육부 대량 데이터를 넣기 위해 기본 틀 생성
- 해당 API 프로그램을 기준으로 반복 작업용 프로그램을 별도로 생성하여 활용한다.
- 프로그램의 실행명은 `[worksapi.py](http://worksapi.py)` 이며, 각 파라메터를 통해 Works API 를 호출하여 활용한다.
- 해당 프로그램에서 Import 한 모듈은 아래와 같다. 만약 실행에 필요한 모듈이 없을 시 해당 모듈을 설치한다.
    
    ```
    jwt   // Java Web Token 을 위해 사용
    requests   // Rest API 사용을 위한 HTTP Call
    unicodedata  // 한글이 포함된 콘솔 화면 출력을 위한 유니코드 처리
    json   // 데이터를 Json 형식으로 처리
    pprint  // Json 형식을 가독성을 높여 출력
    argparse  // 아규먼트를 받아 처리
    time   // Unix Time 을 위해 사용
    ```
    
- 명령 수행은 주 명령어, 보조 명령어, 옵션 세가지로 나뉜다.
    - 주 명령어는 관리할 카테고리를 의미한다. (ex: 일정, 그룹, 사용자, ..)
    - 보조 명령어는 해당 카테고리에서 어떤 작업을 할지 정의한다.
        - 추가, 삭제, 조회 등등
    
    ```
    **worksapi.py** MainCommand SubCommand *[Option]*
    
    ex)
    worksapi.py user query
    ```
    
- 도움말이 필요할 경우 `-h` 를 사용하며 각 커맨드에 따른 도움 화면이 표출된다.
    
    ```
    **worksapi.py -h**
    
    WORKS | WORKSPLACE API Management Program V2
    
    positional arguments:
      {auth,user,org,cal,plan}
                            Description
        auth                Authrization Step
        user                User Management
        org                 Organization Management
        cal                 Calendar Management
        plan                Plan Management
    
    optional arguments:
      -h, --help            show this help message and exit
    
    ---------------------------------------------------------------
    
    ```
## 서브 커맨드

인증을 제외한 모든 메인 커맨드는 서브 커맨드를 필요로 하며 아래 명령으로 한정된다.

`query`

조회의 목적으로 사용한다. 사원 목록, 혹은 특정 사원, 또는 각 일정, 캘린더, 조직 등 조회의 목적으로 사용된다.

## 도움말

각 단계에서 `-h` 옵션을 통해 도움말을 확인 할 수 있다.

```
**worksapi.py user -h**
usage: run.py user [-h] {query,add,delete,update} ...

positional arguments:
  {query,add,delete,update}
                        Description
    query               Query User(s)
    add                 Add User
    delete              Delete User
    update              Update Users

optional arguments:
  -h, --help            show this help message and exit
```

```
**worksapi.py user query -h**
usage: run.py user query [-h] [-t Filename] [-m Email|Id] [-d domain] [-n number] [-c cursor]

optional arguments:
  -h, --help   show this help message and exit
  -t Filename  Access token file. default ak.token
  -m Email|Id  Members Email or ID
  -d domain    Domain Id
  -n number    Number of print, Default 100
  -c cursor    Next page cursor
```
# 인증

**MainCommand : `auth`**

인증은 JWT 방식 및 OAuth 방식을 사용하며, 이로 인해 생성된 Access Token 을 활용한다.

## Syntax

```bash
worksapi.py auth [-h] -t {oauth,jwt} -c Client ID -s Secret Key -o [priv ...] [-f filename] [-k Private key file] [-a Service account] [-d Domain] [-r Redirect URL for auth]
```

**필수 옵션**

`-t` {jwt | oauth}

oauth 또는 jwt 가 올 수 있다.

**그외 옵션**

`-c` ClientId
  (jwt, oauth) Naver Console 페이지에서 발급받은 Client ID 값

`-s` Secret Key
  (jwt, oauth) Naver Console 페이지에서 발급받은 Client Secret 키

`-o` privilege [privilege [..]]
  (jwt, oauth) 받을 권한의 범위(scope) 를 나열한다.

`-f` file name (기본값 : ak.token)
  (jwt, ouath) 생성된 Access Token을 저장할 파일을 지정한다.

`-k` keyfile
  (jwt) 네이버에서 받은 Private Key 파일

`-a` service Account
  (jwt) 사용할 서비스 어카운트. 네이버 개발자 페이지에서 미리 발급.

`-d` Domain
  (oauth) 도메인 명

`-r` redirect URL
  (oauth) 네이버 개발자 페이지에 등록된 Redirect URL

## Using JWT

네이버 웍스 개발자 페이지에서 확인한 Client ID, Secret Key, Service Account 를 확인하고 private key 를 받는다.

### Syntax

```bash
worksapi.py auth \
-t jwt \
-s aa98d8FGd \
-c suijfNmdfuI8dk \
-o user group calendar orgunit directory file \
-k private_gyo.key \
-a jssjfym@goodusdata.by-works.com
```

```bash
####################################
# Access Token Generate Info       #
####################################
Parameter Using: 
 - Service Account: jssjfym@goodusdata.by-works.com
 - Client ID      : suijfNmdfuI8dk
 - Client Secret  : aa98d8FGd
 - Private Key    : Secured. 
 - OAuth Scope    : user group calendar orgunit directory file 
 - Token output   : ak.token
```
## Using OAUTH

OAuth 를 이용하기 위해서는 개발자 콘솔에 미리 Redirect URL 을 설정하며, 해당 URL로 인증코드를 전송한다. 해당 인증코드를 이용하여 Access Token 을 발급받게 된다.

### Syntax

기본적인 정보를 가지로 인증 절차를 시작한다.

```
**worksapi.py** auth \
-t oauth \
-c df1vPzpc6IOmc6WOYySg \
-s bCUu3CSfRk \
-d goodusdata.by-works.com \
-r https://db.goodusdata.com/imsi \
-o user group calendar orgunit directory file \
-f imsiauth.token
```

수행하게 되면 아래와같이 코드를 입력받기 위해 대기를 수행한다.

```
| Attention 
+---------------------
Log in Works site and Check Access Code.
And type access code at here :
```

동시에 열린 웹 브라우저를 통해 네이버 웍스에 권한있는 사용자로 로그인 하면, 지정된 Redirect URL 로 이동하며, 코드를 발급 받을 수 있다.
이후 해당 코드를 입력하면 정상적으로 지정한 파일에 access token이 생성된다.

```bash
| Attention 
+---------------------
Log in Works site and Check Access Code.
And type access code at here : 
**kr1YXFhVVdLUlBvVFVWb0Zxbw==**
####################################
# OAuth Info                       #
####################################
 - OAuth Scope    : user,group,calendar,orgunit,directory,file
 - Expires in     : 86400
 - Token File     : imsiauth.token
```

# 조직

**Main Command** : `org`
## 조회

### Syntax

```bash
**worksapi.py org query** [-h] [-t Filename] [-o Org Unit ID] [-d domain] [-n number] [-c cursor]

optional arguments:
  -h, --help      show this help message and exit
  -t Filename     Access token file. default ak.token
  -o Org Unit ID  Org unit Id
  -d domain       Domain Id
  -n number       Number of print, Default 100
  -c cursor       Next page cursor
```

### Options

| PARAMETER | REQUIRED | VALUE | DESCRIPTION |
| --- | --- | --- | --- |
| -t | N | file name | Access Token 파일. 기본값 ak.token |
| -o | N | Org ID | 특정 조직에 대한 정보 조회 시 조직 아이디 |
| -d | N | Domain ID | 특정 도메인으로 조회 시 선언 |
| -n | N | int | 출력할 조직의 수. 해당 수 보다 많은 조직이 있을 경우 Cursor 제공 기본값 100 |
| -c | N | cursor | 커서를 알고 있을 경우 해당 커서를 통해 해당 페이지부터 보여준다. |

### Example

```
**# 전체 조직 조회**
worksapi.py org query

**# 한번에 10개씩 조회**
worksapi.py org query -n 10

**# 특정 페이지 커서부터 조회**
worksapi.py org query -n 10 -c xxxxxxxxxxxxxxxxxxx

**# 특정 조직 조회**
worksapi.py org query -o xxxxx-xxx-xx-xxx-xxx
```
# 사용자

**Main Command :** `user` 

## 조회

### Syntax

```
**worksapi.py org query** [-h] [-h] [-t Filename] [-m Email|Id] [-d domain] [-n number] [-c cursor]

optional arguments:
  -h, --help   show this help message and exit
  -t Filename  Access token file. default ak.token
  -m Email|Id  Members Email or ID
  -d domain    Domain Id
  -n number    Number of print, Default 100
  -c cursor    Next page cursor
```

### Options

| PARAMETER | REQUIRED | VALUE | DESCRIPTION |
| --- | --- | --- | --- |
| -t | N | file name | Access Token 파일. 기본값 ak.token |
| -m | N | Email or Id | 특정 사용자에 대한 정보 조회 시 설정 |
| -d | N | Domain ID | 특정 도메인으로 조회 시 선언 |
| -n | N | int | 한번에 출력할 개수. 제공 기본값 100 |
| -c | N | cursor | 페이징 커서 정보 |

### Example

```
**# 전체 사용자 조회**
worksapi.py user query

**# 한번에 10개씩 조회**
worksapi.py user query -n 10

**# 특정 페이지 커서부터 조회**
worksapi.py user query -n 10 -c xxxxxxxxxxxxxxxxxxx

**# 특정 사용자 조회**
worksapi.py user query -o xxxxx-xxx-xx-xxx-xxx
```
# 일정

**Main Command : `plan`**

## 조회

### Syntax

```
**worksapi.py plan query** [-h] -m Email|ID [-f filename] [--cid Calendar ID] [--eid Event ID] [--targetym YYYY-MM]

optional arguments:
  -h, --help          show this help message and exit

default Options:
  -m Email|ID         member's Email or ID
  -f filename         Access Token file. Default 'ak.token'.

Optional:
  --cid Calendar ID   Calendar ID. If ommit, Query member's default calendar
  --eid Event ID      Event ID. If ommit, List Plans.
  --targetym YYYY-MM  Query Year Month. Ex) YYYY-MM. Set when -e ommitted.
```

### Options

| PARAMETER | REQUIRED | VALUE | DESCRIPTION |
| --- | --- | --- | --- |
| -f | N | file name | Access Token 파일. 기본값 ak.token |
| -m | Y | member Id | 일정을 조회할 사용자의 아이디 |
| --cid | N | Calendar Id | 사용자가 접근 가능한 캘린더의 아이디.<br>제공하지 않을 경우 기본 캘린더의 일정 표출 |
| --eid | N | Event Id | 특정 이벤트 아이디.<br>제공하지 않을 경우 전체 일정 출력 |
| --targetym | N | YYYY-MM | --eid 를 제공하지 않을 경우 반드시 필요.<br>조회하고자 하는 년-월. |

### Example

```
**# 기본 캘린더의 일정 조회**
worksapi.py plan query -m xxxxxxxxxxx --targetym 2023-03

**# 개인이 접근 가능한 특정 캘린더의 일정 조회**
worksapi.py plan query -m xxxxxxxxxxx --cid xxxx-xxx-xx --targetym 2023-03

**# 특정 이벤트 조회**
worksapi.py plan query -m xxxxxxxxxxx --cid xxx-xx-x --eid xxx-xx-xxx
```

## 생성

### Syntax

```
**worksapi.py plan add** [-h] [-f filename] -m Email|ID --summary Summary [--cid Calendar ID] --type {day,time} --start
                            YYYY-MM-DD|YYYY-MM-DDTHH:mm:ss [--end YYYY-MM-DD|YYYY-MM-DDTHH:mm:ss] [--tz Region/City] [--oid Id|Email] [--odpname name]
                            [--attid email or Id] [--attdpname name] [--partstat {need-action,accepted,tentative,declined}] [--recfreq Frequency]
                            [--recuntil YYYY-MM-DDTHH:mm:ss] [--recint Interval] [--recbt Interval] [--recbtv Interval]
                            [--reex [YYYYMMDDThhmmssZ ...]] [--vurl url] [--vrid url] [--almethod {display,email}] [--altrigger trigger]
                            [--mtype MapType] [--geo Geolocation] [--murl url] [--mimg Map Image] [--eid Event ID] [--category category ID]
                            [--visibility {public,private}] [--sequence SequenceNumber] [--transparency {opaque,transparent}] [--location LOCATION]
                            [--description DESCRIPTION]

optional arguments:
  -h, --help            show this help message and exit

Access Token Options:
  -f filename           Access Token file. Default 'ak.token'.

Default Options:
  -m Email|ID           member's Email or ID
  --summary Summary     Summary of Plan. (Title)
  --cid Calendar ID     Calendar ID. If ommit, add plan to member default calendar.

Date and Time Zone Option:
  --type {day,time}     Plan Type. All day plan or Time plan. (Title)
  --start YYYY-MM-DD|YYYY-MM-DDTHH:mm:ss
                        Plan Start Time. All day plan : YYYY-MM-DD, Time plan : YYYY-MM-DDTHH:mm:ss.
  --end YYYY-MM-DD|YYYY-MM-DDTHH:mm:ss
                        Plan End Time. All day plan : YYYY-MM-DD (End date is exclusive), Time plan : YYYY-MM-DDTHH:mm:ss.
  --tz Region/City      Timezone. Set this parameter when plan type(--type) is "time". ex)Asia/Seoul. default Asia/Seoul

Organizer Option:
  --oid Id|Email        Organizer's Id or Email
  --odpname name        Organizer display Name

Attendee Info:
  If you want to set attendee, Set parameter below all. Don't ommit any parameters. There is more than one attendes, repeat parameters as attendees

  --attid email or Id   email or Id
  --attdpname name      Attendees display name
  --partstat {need-action,accepted,tentative,declined}
                        partstat

Recurrency option:
  Day Name : SU/MO/TU/WE/TH/FR/SA

  --recfreq Frequency   Repeat frequency.
  --recuntil YYYY-MM-DDTHH:mm:ss
                        Repeat Until.
  --recint Interval     Repeat interval. default 1.
  --recbt Interval      Set by types.
  --recbtv Interval     By types value.

Recurrency Exception:
  --reex [YYYYMMDDThhmmssZ ...]
                        Exception day. ex)20240301T000000Z

Video Meeeting Options:
  --vurl url            Video meeting url
  --vrid url            Video meeting resource Id

Reminder Option:
  If you want to alarm more than once, repeat parameters.

  --almethod {display,email}
                        Alarm Method
  --altrigger trigger   Alarm Trigger. ex)PT0S, PT15M, PT12H, P1D"

Map Option:
  --mtype MapType       Map type. ex)NAVER, google
  --geo Geolocation     Geolocation. ex) "40.7486484;-73.98400699999999"

Map Url Option:
  --murl url            Map URL
  --mimg Map Image      map Image

Etc Options:
  --eid Event ID        User defined Event ID.
  --category category ID
                        Category Id
  --visibility {public,private}
                        Visibility. default public.
  --sequence SequenceNumber
                        Plan sequece
  --transparency {opaque,transparent}
                        Set Transparency. default opaque.
  --location LOCATION   location
  --description DESCRIPTION
                        Description
```

### Options

**Required Option - Default**

| PARAMETER | REQUIRED | VALUE | DESCRIPTION |
| --- | --- | --- | --- |
| -f | N | file name | Access Token 파일. 기본값 ak.token |
| -m | Y | member Id | 일정을 조회할 사용자의 아이디 |
| --cid | N | Calendar Id | 사용자가 접근 가능한 캘린더의 아이디.<br>제공하지 않을 경우 기본 캘린더에 추가 |
| --summary | Y | Summary | 일정 요약. 주로 제목으로 사용된다. |

**Required Option - Date**

| PARAMETER | REQUIRED | VALUE | DESCRIPTION |
| --- | --- | --- | --- |
| --type | Y | all|time | all<br>  하루 종일 일정<br>time<br>  특정 시간 일정 |
| --start | Y | 날짜&시간 | 일정의 시작 시점<br> 하루 종일 일정<br>  yyyy-mm-dd<br> 시간 일정<br>  yyyy-mm-ddThh:mm:ss |
| --end | N | 날짜&시간 | 일정의 종료 시점<br> 하루 종일 일정<br>  yyyy-mm-dd<br>  종일 일정은 종료 날짜는 일정에 포함되지 않음<br> 시간 일정<br>  yyyy-mm-ddThh:mm:ss |
| --tz | N | Timezone | 타임존. 기본적으로 Asia/Seoul |

**Optional - Attendee**

참석자가 여러명일 경우 아래 파라메터를 반복적으로 기입한다. 모든 파라메터가 동일한 개수로 지정 되어야 하며 빠지는 파라메터가 있어서는 않된다.

| PARAMETER | REQUIRED | VALUE | DESCRIPTION |
| --- | --- | --- | --- |
| --attid | N | attendee Id | 참석자의 ID 혹은 Email |
| --attdpname | N | 표시 이름 | 참석자의 표시 이름 |
| --partstat | N | 참석자 상태 | need-action 응답 대기<br>accepted    참석<br>tentative   미정<br>declined    거절 |
**Optional - Recurrency (반복)**

| PARAMETER | REQUIRED | VALUE | DESCRIPTION |
| --- | --- | --- | --- |
| --recfreq | N | 반복 주기 | WEEKLY, MONTHLY 등 iCal format 참조 |
| --recuntil | N | 반복 종료일 | YYYYMMDDTHHmmssZ 형식<br> ex)20250101T000000Z |
| --recint | N | 반복 간격 | 반복의 간격을 지정한다.<br>--recfreq 가 weekly 일 때 해당 값을 3 으로 설정 시 3주에 한번이 된다. |
| --recbt | N | BY형식 | BYDAY, BYMONTH 등의 값을 갖는다.<br>iCal format 참조 |
| --recbtv | N | BY형식의 값 | --recbt 가 BYDAY 이며, --recbtv 가 MO 이고 --recfreq 가 WEEKLY 일 경우 매주 월요일이 된다. |

**Optinal - Recurrency Exception(반복 중 제외)**

| PARAMETER | REQUIRED | VALUE | DESCRIPTION |
| --- | --- | --- | --- |
| --reex | N | 날짜 | 반복중 제외 일자를 선언<br>ex)20240301T000000Z |

**Optional - Video Meeting**

화상회의 URL 이 있다면 아래 파라메터를 추가

| PARAMETER | REQUIRED | VALUE | DESCRIPTION |
| --- | --- | --- | --- |
| --vurl | N | 주소 | 화상회의 주소 |
| --vrid | N | 리소스 아이디 | 리소스 아이디 |

**Optional - Reminder**

일정 미리 알림 기능

| PARAMETER | REQUIRED | VALUE | DESCRIPTION |
| --- | --- | --- | --- |
| --almethod | N | display or email | display<br> 앱 푸시 화면으로 알람을 전달<br>email<br> 등록된 이메일로 알람 전달 |
| --altrigger | N | 트리거 | PT0s, PT15M 등 ical 포멧에 맞는 트리거를 설정하며 앞의 -는 제외한다.<br>원래 -PT15M 이어야 하나 편의상 - 제거 |

**Optional - Map**

일정 미리 알림 기능

| PARAMETER | REQUIRED | VALUE | DESCRIPTION |
| --- | --- | --- | --- |
| --mtype | N | Map 제공자 | 맵 제공자에 대한 정보<br>ex) google, naver |
| --geo | N | 위경도 | 위경도를 표현한다.<br>ex) “40.7486484;-73.98400699999999" |

**Optional - Map Url**

| PARAMETER | REQUIRED | VALUE | DESCRIPTION |
| --- | --- | --- | --- |
| --murl | N | Map URL | 맵에 대한 URL |
| --mimg | N | Map Image | 맵 이미지 |

**Optional - Etc**

| PARAMETER | REQUIRED | VALUE | DESCRIPTION |
| --- | --- | --- | --- |
| --eid | N | Event Id | 이벤트 아이디 (사용자 정의) |
| --category | N | Id | 사용자 정의 카테고리 아이디 |
| --visibility | N | pubilc | private | 기본값 public<br>다른 사용자에게 표출될지 여부를 설정. |
| --sequence | N | int | 변경 시퀀스 번호 |
| --transparency | N | opaque | transparent | 일정의 상태 정보.<br>기본값 opaque(바쁨) 으로 설정 |
| --location | N | Location | 위치 정보. 일반적인 텍스트. |
| --description | N | description | 주석 |

See iCal reference : [iCal Format](https://www.notion.so/iCal-Format-8feedd41e90d417fb76fa13f6980696b?pvs=21) 

## Example

```bash
**python3 ./worksapi.py plan** **add** \
-m bbe234f2-5a1f-4a07-1a6e-03bbb2146ad1 \
--summary "This is New API Program 2" \
--type time \
--start 2024-03-21T10:00:00 \
--end 2024-03-21T11:00:00 \
--attid taeseok.seo@goodusdata.by-works.com --attdpname ts --partstat need-action \ 
--attid sungwook.kim@goodusdata.by-works.com --attdpname sw --partstat need-action \
--recfreq monthly --recuntil 20250101T000000Z --recint 1 \
--reex 20240623T000000Z \
--almethod email --altrigger PT15M \
--description "Hello"
```
