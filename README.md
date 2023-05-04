# PyNCPWorks API

범주: NCP
상태: In progress
요약: Naver Works API 를 이용한 Python 프로그램
최종 편집 일시: May 4, 2023 4:06 PM
태그: api, python, script, works

# Overview

- Naver Works 를 관리하기 위한 API 를 활용하여 Works 를 다루기 위함
- 최초 교육부 대량 데이터를 넣기 위해 기본 틀 생성
- 해당 API 프로그램을 기준으로 반복 작업용 프로그램을 별도로 생성하여 활용한다.
- 프로그램의 실행명은 worksapi.py 이며, 각 파라메터를 통해 Works API 를 호출하여 활용한다.
- 해당 프로그램에서 Import 한 모듈은 아래와 같다.
  
    ```
    jwt   // Java Web Token 을 위해 사용
    requests   // Rest API 사용을 위한 HTTP Call
    unicodedata  // 한글이 포함된 콘솔 화면 출력을 위한 유니코드 처리
    json   // 데이터를 Json 형식으로 처리
    pprint  // Json 형식을 가독성을 높여 출력
    argparse  // 아규먼트를 받아 처리
    time   // Unix Time 을 위해 사용
    ```
    
- 메인 아규먼트의 경우 `-` 가 한개만 붙고 그 외 서브 및 옵션은 두개가 붙는다.
  
    ```
    아규먼트를 잘못 사용할 경우 아래와 같은 에러 발생
    
    **worksapi.py** -u --m e32cdfd2-9ae5-40c4-1233-035201fa5e37 -j 
    usage: worksapi.py [-h] [-g] [-k file_name] [-C NCP Client ID] [-c NCP Client Secreat ID] [-e xxxx.serviceacount@xxxx.xxx] [-s [OAuth Privileges ...]] [-u] [-ca] [-G] [-o] [-et] [--a] [--p] [--r]
                       [--d Domain_Id] [--j] [--m Email_or_Id] [--n name] [--t default ak.token] [--U user_key_id] [--cnt Count] [--cur cursor] [--dlv Levelint] [--ek EK] [--showall]
                       [--first-name firstname] [--last-name lastname] [--private-email PrivateEmail] [--employee-type-id Employee Type Id] [--cellphone xxx-xxx-xxxx] [--sso]
                       [--password-config {ADMIN,MANUAL}] [--password password] [--primary] [--params { key:value, [key:value, ...]] [--uid Organization Id] [--pid Parents Organization ID]
                       [--domain-list [domainId ...]] [--uid-list [uid ...]] [--sm] [--uM] [--adml [User Id or Email ...]] [--des DES] [--gid Group_Id] [--mem [MemberId MemberType ...]] [--sn] [--um] [--un]
                       [--uc] [--ut] [--uf]
    **worksapi.py: error: unrecognized arguments: -j**
    ```
    
- 도움말이 필요할 경우 `-h` 를 사용한다.
  
    ```
    worksapi.py -h
    ```
    

# Accesstoken 발급받기

## Accesstoken 발급

**ARGUMENT** : `-g`

> Naver works 의 API 를 활용하기 위해서는 JWT 를 사용하여야 하며 JWT 의 기초 가이드는  [JWT 사용 가이드 (Using Pyhton)](https://www.notion.so/JWT-Using-Pyhton-b3994d0416e549bb8cc317d9f5202187) 문서를 참고한다.
> 

### Syntax

```bash
worksapi.py -g (Options)
```

### Options

| PARAMETER | REQUIRED | VALUE | DESCRIPTION |
| --- | --- | --- | --- |
| -k | Y | privateKey_filename | SSH Private 키 파일을 지정한다. |
| -C | Y | Client_id | Developer Console 에서 확인할 수 있는 Client ID 값 |
| -c | Y | Client_secret | Developer Console 에서 확인할 수 있는 Client Secret 값 |
| -e | Y | Service Account 메일주소 | Developer Console 에서 서비스 계정을 발급 할 수 있으며, xxx.servcieaccount@xxx.xxx 형식을 가진다. |
| -s | Y | OAuth Scope | Developer Console 에서 확인할 수 있는 권한의 종류이며 각 권한의 구별은 공백으로 한다. |
| --t, --token-file | N | token file | 발급된 Accesstoken 을 저장할 파일.  기본값 ak.token |

### Sample

```bash
**worksapi.py -g -k private.key -C 338472 -c dkf7ka8 \
   -e test.serviceaccount@test.com \
   -s user calendar orgunit**
```

- dd정상적으로 토큰이 발급되었다면 `--t` 옵션으로 지정된 파일에 토큰값이 저장된다.

# 조직 관리

- **MAIN ARGUMENT** : `-o`

## 조직 조회

- **Argument** : None

### Syntax

```bash
worksapi.py -o [Required Options]
```

### Options

| PARAMETER | REQUIRED | VALUE | DESCRIPTION |
| --- | --- | --- | --- |
| --cnt | N | int value, 1 ~ 100 | 한번에 출력할 목록의 갯수를 지정한다. 기본값 100 |
| --cur | N | Cursor Name | 목록이 여러개라면 다음 페이지를 조회할 때 해당 커서를 입력하면 해당 다음 페이지부터 출력.<br>출력해야 할 데이터가 --cnt 보다 많을 경우 다음 출력에 대하여 참조할 수 있는 커서를 출력함  |
| --j, --json | N |  | 해당 옵션을 사용 할 경우 모든 정보를 json 형식으로 출력. 세부 정보까지 확인할 시 사용한다. |
| --t, --token-file | N | token file | Access Token 을 저장한 파일. 기본값 ak.token |

### Sample

```bash
**worksapi.py -o**

Organization ID                         Organization Email                                Organization Name             Parents Organization ID                 Organization Ext Key                    
----------------------------------------------------------------------------------------------------------------------------------------------------------------
1bf0cd21-5735-4bca-21e0-03c709960fb8    hello@goodusdata.by-works.com                     헬로우                                                                helloTest01_extkey                      
f1aa43e1-f878-4dad-2e72-030b1863b21b    hellosub@goodusdata.by-works.com                  헬로우서브                    1bf0cd21-5735-4bca-21e0-03c709960fb8    hellotest_ext_sub_001                   
eee81e01-bd51-4be5-291f-0317f8f5a1a1    t_303gh@goodusdata.by-works.com                   Naver Cloud 사업부                                                    f31b6909-a6ef-44ca-bef5-30d702e522c2
...
```

## 조직 생성

- **Sub Argument** : `--p`

### Syntax

```bash
worksapi.py -o --p [Required Options]
```

### Options

| PARAMETER | REQUIRED | VALUE | DESCRIPTION |
| --- | --- | --- | --- |
| --d | Y | Domain Id | Develoer Console 에서 확인 가능한 Domain Id |
| --n | Y | Name | 조직의 이름 |
| --m | Y | orgEmail | 조직의 대표 Email |
| --ek | N | External Key | 외부에서 사용 시 사용할 조직의 외부 키 |
| --pid | N | Parents Org Id | 조직의 상위 조직 |
| --dlv | N | DisplayLevel | 표출 디스플레이 레벨 |
| --j, --json | N |  | Json 형식으로 출력 |

### **Sample**

```
worksapi.py -o --p --d 229952 --n HelloOrg \
--m helloOrgUnit@goodusdata.works-by.com
```

# 사용자 관리

- **MAIN ARGUMENT** : `-u`

## 사용자 조회

- **Argument** : None

### Syntax

```
worksapi.py -u [options]
```

### Options

| PARAMETER | REQUIRED | VALUE | DESCRIPTION |
| --- | --- | --- | --- |
| --m | N | Email 주소 | 사용자 키 ID | 특정 사용자의 Email 주소 또는 User Key ID<br>미 제공 시 전체 사용자 정보 |
| --cnt | N | 최대 출력 개수 | 최대 출력 개수 (Default 100) |
| --cur | N | 커서명 | 출력 대상이 100개 이상일 경우 다음 페이지에 대한 커서 |
| --showall | N |  | 삭제된 사용자까지 전부 출력 |
| --j, --json | N |  | 전체 세부 정보 출력. Json 형식 |

## 신규 사용자 생성

- **Argument** : `--p`

### Syntax

```
worksapi.py -u --p [Required Options]
```

### Options

| PARAMETER | REQUIRED | VALUE | DESCRIPTION |
| --- | --- | --- | --- |
| -d | Y | domain Id | Developer Console 에서 확인 가능한 domain Id |
| --m | Y | Email 주소 | Domain 이 포함된 Email 주소<br>(ex : user.383@goodusdata.by-works.com |
| --private-email | N | 개인 Email | 개인 Email 주소 |
| --first-name | Y | 이름 | 사용자 이름 |
| --last-name | Y | 성 | 성 |
| --cellphone | N | xxx-xxxx-xxxx | 휴대폰 번호 |
| --domain-list | N | domain id [domain id [domain id [..]]] | 소속되어 있는 회사의 도메인.<br>2개 이상이 올 수 있으며, 가장 처음 나온 도메인이 Primary 가 된다. 해당 옵션을 선택하지 않으면 --d 옵션의 도메인이 Primary 도메인(회사) 가 된다. |
| ---uid-list | N | orgUnitId [orgUnitId ..] | 회사의 조직 고유 번호.<br>한 회사(도메인) 에는 여러개의 조직에 속할 수 있다.<br>만약 --domain-list 를 통해 두개 이상의 회사를 구성하였다면, <br>`--uid-list A_domain_orgid --uid-list B_domain_orgid`형식으로 각 회사의 조직을 지정할 수 있다. 마찬가지로 한 회에서 여러개의 조직을 설정할 수 있으며, 첫번째 나오는 orgId 가 Primary 가 된다.<br>`---uid-list A_domain_orgid1 A_domain_orgid2 ---uid-list B_domain_orgid1 B_domain_orgid2 B_domain_orgid3`<br>위 경우, A 도메인의 Primary 조직은 A_domain_orgid1 이 되고 B 도메인의 Primary 조직은 B_domain_orgid1 이 된다. |
| ---password_config | N | ADMIN \| MANUAL | --sso 를 선언하였다면 구성하지 않는다.<br>---sso 를 선언하지 않았을 경우 ADMIN / MANUAL 둘중 하나를 선택하여야 하며, ADMIN 으로 선언하면 --password 를 설정 하여야 한다.<br>MANUAL 의 경우 --private-email 을 반드시 설정 해 주어야 한다. |
| ---password | N | Password | ADMIN 으로 설정 시 암호를 설정.  |

### Sample

```
worksapi.py -u --p --d 229952 --m realTest@goodusdata.by-works.com \
--first-name jh \
--last-name lee \
--domain-list 229952 383732 958883 \
--uid-list d8459f15-ba00-48ce-2353-0361a28e8458 d8459f15-ba00-48ce-2353-0361a28e8458 \
--uid-list e8378sa2-ab81-8caf-3319-783001eff871 \
--password-config ADMIN \
--password HelloWorld
```

> 총 3개의 회사를 지정(`---uid-list` )
첫번째 회사(229952) 에서는 2개의 조직에 포함되며 두번째 회사(383732)는 하나의 조직을 갖는다.
단, 3번째 회사에서는 조직이 할당되지 않는다.
> 

```
**# ArgParse Info**
u=True, p=True, d=229952,
m='realTest@goodusdata.by-works.com', t='ak.token',
first_name='jh', last_name='lee', private_email=None, 
cellphone=None, sso=False, 
password_config='ADMIN', 
password='HelloWorld', 
domain_list=['229952', '383732', '958883'], 
uid_list=[['d8459f15-ba00-48ce-2353-0361a28e8458', 
           'd8459f15-ba00-48ce-2353-0361a28e8458'], 
          ['e8378sa2-ab81-8caf-3319-783001eff871']]
```

## 기존 사용자 수정

- **Argument** : `--a`

### Syntax

```
worksapi.py -u --a [Required Options]
```

### Options

| PARAMETER | REQUIRED | VALUE | DESCRIPTION |
| --- | --- | --- | --- |
| --d | Y | domain Id | Developer Console 에서 확인 가능한 domain Id |
| --m | Y | Email 주소 | Domain 이 포함된 Email 주소<br>(ex : user.383@goodusdata.by-works.com ) |
| --private-email | N | 개인 Email | 개인 Email 주소 |
| --first-name | Y | 이름 | 사용자 이름 |
| --last-name | Y | 성 | 성 |
| --domain-list | N | domain id [domain id [domain id [..]]] | 소속되어 있는 회사의 도메인.<br>2개 이상이 올 수 있으며, 가장 처음 나온 도메인이 Primary 가 된다. 해당 옵션을 선택하지 않으면 --d 옵션의 도메인이 Primary 도메인(회사) 가 된다. |
| --uid-list | N | orgUnitId [orgUnitId ..] | 회사의 조직 고유 번호. 한 회사(도메인) 에는 여러개의 조직에 속할 수 있다. <br>만약 --domain-list 를 통해 두개 이상의 회사를 구성하였다면,<br>`---uid-list A_domain_orgid --uid-list B_domain_orgid` 형식으로 각 회사의 조직을 지정할 수 있다. 마찬가지로 한 회에서 여러개의 조직을 설정할 수 있으며, 첫번째 나오는 orgId 가 Primary 가 된다.<br>`---uid-list A_domain_orgid1 A_domain_orgid2 ---uid-list B_domain_orgid1 B_domain_orgid2 B_domain_orgid3`<br>위 경우, A 도메인의 Primary 조직은 A_domain_orgid1 이 되고 B 도메인의 Primary 조직은 B_domain_orgid1 이 된다. |
| --password_config | N | ADMIN | MANUAL |
| --password | N | Password | ADMIN 으로 설정 시 암호를 설정.  |

### Sample

```
worksapi.py -u --a --d 229952 --m realTest@goodusdata.by-works.com \
--first-name jh \
--last-name lee \
--domain-list 229952 383732 958883 \
--uid-list d8459f15-ba00-48ce-2353-0361a28e8458 d8459f15-ba00-48ce-2353-0361a28e8458 \
--uid-list e8378sa2-ab81-8caf-3319-783001eff871 \
--password-config ADMIN \
--password HelloWorld
```

- 사용자 수정은 사용자 생성과 동일하다.
- 기존의 사용자 정보를 대체한다 라는 의미로 해석하면 된다.

# 그룹 관리

- **MAIN ARGUMENT** : `-G`

## 그룹 조회

- **Argument** : None

### Syntax

```
worksapi.py -G [options]
```

### Options

| PARAMETER | REQUIRED | VALUE | DESCRIPTION |
| --- | --- | --- | --- |
| --d | Y | Domain ID | 도메인 ID |
| --gid | N | GroupID | 특정 그룹에 대한 정보를 출력 |
| --m | N | GroupID | 그룹 ID 제공 시 특정 해당 그룹의 정보 |
| --cnt | N | 최대 출력 개수 | 최대 출력 개수 (Default 100) |
| --cur | N | 커서명 | 출력 대상이 100개 이상일 경우 다음 페이지에 대한 커서 |
| --j, --json | N |  | 전체 세부 정보 출력. Json 형식 |
| --tk | N |  | Access Token 파일 |

## 신규 그룹 생성

- **Argument** : `--p`

### Syntax

```
worksapi.py -G --p [Required Options]
```

### Options

| PARAMETER | REQ | VALUE | DESCRIPTION |
| --- | --- | --- | --- |
| --d | Y | domain Id | Developer Console 에서 확인 가능한 domain Id |
| --n | Y | Group Name | 그룹 명 |
| --des | N | Description | Description. 명령줄에 쌍따옴표(”) 로 감싸야 한다. |
| --sn | N | Set to True | 서비스 알림 발송 여부. 옵션 설정시 True 반환<br>Default : False |
| --sm | N | Set to True | 그룹 관지자가 서비스 사용 여부를 변경할 지 여부. 설정시 True 반환<br>Default : False |
| --ek | N | 참조 외부키 | 외부키 사용시 사용할 외부키 명 |
| --adml | Y | User_ID [User_ID …] | 관리자의 KEY ID 리스트. 공백으로 구분.<br>사용자_ID 또는 Email 도 가능함 |
| --um | N | Set to True | 그룹 대화방의 사용 여부<br>Default: False |
| --un | N | Set to True | 그룹 노트 사용 여부. 그룹 대화방 사용 시에만 가능<br>Default : False |
| --uc | N | Set to True | 그룹 일정 사용 여부. 그룹 대화방 사용 시에만 가능<br>Default : Fasle |
| --ut | N | Set to True | 그룹 할일 사용 여부. 그룹 대화방 사용 시에만 가능<br>Default : False |
| --uf | N | Set to True | 그룹 폴더 사용 여부. 그룹 대화방 사용 시에만 가능<br>Default : False |
| --uM | N | Set to True | 그룹 메일 사용 여부. True 일 시 groupEmail 항목 필수 (다음 옵션) |
| --m | N | Group Email | 그룹 메일을 사용하기 위해서는 해당 옵션을 통해 Group Email 지정 필수 |
| --mem, <br>--member | Y | 멤버키(또는 이메일) 멤버타입 | 해당 그룹의 멤버 리스트를 나타내며 해당 파라메터를 연속적으로 붙여 여러명의 멤버를 추가.<br>최소 1개의 멤버 필요.<br>멤버 타입<br> * USER<br> * ORGUNIT<br> * GROUP |
| --t | N | Access Token 파일 | 기본값 ak.token |

### Sample

```
**worksapi.py** -G --p --d 229952 --n HelloGroup \
--description "hello world boy" \
--m helloworld_group@goodusdata.by-works.com \
--admin-list bbe234f2-5a1f-4a07-1a6e-03bbb2146ad1 617e0a36-9a01-4c9f-1547-03cfa5eba194 \
--member e32cdfd2-9ae5-40c4-1233-035201fa5e37 USER \
--member 75f5313b-b265-4fbe-1c8c-034f61c7ca62 USER \
--um --uc
```

> `HelloGroup` 그룹을 생성하며 2명의 관리자 및 2명의 멤버를 설정.
그룹 메일은 `helloworld_group@goodusdata.by-works.com` 이며
`---um` 옵션을 통해 그룹 대화방을 사용하며 `--uc` 옵션을 통해 그룹 캘린더 사용
* `--uc` 사용 시 멤버로 등록 되어 있어야 그룹 캘린더가 보이며, 관리자도 멤버로 넣어야 그룹 캘린더가 표출됨
```
**# ArgParse Info**
G=True, p=True, d=229952, 
m='helloworld_group@goodusdata.by-works.com', n='HelloGroup', 
t='ak.token',
adml=['bbe234f2-5a1f-4a07-1a6e-03bbb2146ad1', 
      '617e0a36-9a01-4c9f-1547-03cfa5eba194'], 
des='hello world boy',
mem=[['e32cdfd2-9ae5-40c4-1233-035201fa5e37', 'USER'], 
     ['75f5313b-b265-4fbe-1c8c-034f61c7ca62', 'USER']]
```

**IMPORTANT**

- 그룹 캘린더 사용 시 웍스 모바일 페이지에서 캘린더 화면에 캘린더 표출에 대한 조건 확인 필요
  
  
    | ADMIN 리스트에 포함 | MEMBER 리스트에 포함 | 캘린더 표출 여부 |
    | --- | --- | --- |
    | TRUE | FALSE | FALSE |
    | TRUE | TRUE | TRUE |
    | FALSE | TRUE | TRUE |
- 따라서 **Admin List 에 포함 되었다 하더라도 Member List 에 포함되지 않으면** worksmobile.com 페이지의 **캘린더 화면에서 그룹 캘린더를 확인할 수 없음**

# 캘린더 관리

- **MAIN ARGUMENT : `-ca`**

## 사용자 캘린더 목록 조회

- **Argument** : None

**Syntax**

```
worksapi.py -ca --m [userId or Email]
```

- 캘린더 목록을 조회하기 위해서는 특정 사용자를 지정하여야 한다.

## 캘린더 생성

- **Sub Argument : `--p`**

**Syntax**

```
worksapi.py -ca --p [Options]
```

### Options

| PARAMETER | REQ | VALUE | DESCRIPTION |
| --- | --- | --- | --- |
| --n | Y | Calendar Name | 캘린더 이름 |
| --mem | N | Members | 캘린더 맴버 지정<br>--mem Id Type Role --mem Id Type Role 형식으로 여러 멤버 지정 가능.<br>* TYPE<br>  USER / GROUP / ORGUNIT<br>* ROLE<br>  CALENDAR_EVENT_READ_WRITE <br>     - 캘린더 및 일정관리<br>  EVENT_READ_WRITE<br>     - 일정 관리<br>  EVENT_READ<br>     - 일정 상세 정보 조회<br>  EVENT_READ_FREE_BUSY<br>     - 일정의 일시만 조회 |
| --pub | N | Set to Public | 설정시 Public 으로 설정 |

**Sample**

```
**worksapi.py** -ca --p --n HelloCalendar \
--mem 213c5eac-6bb9-456c-38c5-0328224df2cc GROUP EVENT_READ \
--mem 4fafe977-8f93-4d26-37a7-03141498abd6 GROUP CALENDAR_EVENT_READ_WRITE \
--pub \
--des "My Test Calendar"

# result
{'calendarEmail': '90e672ca-57e8-444d-a2e4-4a367af3e202@kr1-groups.calendar.worksmobile.com',
 'calendarId': '90e672ca-57e8-444d-a2e4-4a367af3e202',
 'calendarName': 'HelloCalendar',
 'description': 'My Test Calendar',
 'isPublic': True,
 'members': [{'id': '4fafe977-8f93-4d26-37a7-03141498abd6',
              'role': 'CALENDAR_EVENT_READ_WRITE',
              'type': 'GROUP'},
             {'id': '213c5eac-6bb9-456c-38c5-0328224df2cc',
              'role': 'EVENT_READ',
              'type': 'GROUP'}]}
```

```
**# ArgParse Info**
ca=True, p=True, n='HelloCalendar', t='ak.token',
des='My Test Calendar',
**mem=[['213c5eac-6bb9-456c-38c5-0328224df2cc', 'GROUP', 'EVENT_READ'], 
     ['4fafe977-8f93-4d26-37a7-03141498abd6', 'GROUP', 'CALENDAR_EVENT_READ_WRITE']],** 
pub=True
```

# 일정 관리

- **MAIN ARGUMENT : `-P`**

## 캘린더 일정 조회

- **Argument** : `--m`, `--cid`

**Syntax**

```
worksapi.py -P --m [userId] -cid [Calendar ID]
```

- 일정을 조회하기 위해서는 캘린더 및 해당 캘린더 소유자의  ID 를 알아야 한다.

## 일정 생성

- **Sub Argument : `--p`**

**Syntax**

```
worksapi.py -P --p [Options]
```

| PARAMETER | REQ | VALUE | DESCRIPTION |
| --- | --- | --- | --- |
| --m | Y | User_ID | 사용자 ID |
| --cid | Y | Calendar_ID | 캘린더 ID |
| --summary | Y | Summary | 일정 요약 |
| --des | N | description | 일정 메모 |
| --pt, --plan-type | Y | 일정형식 | DATE - 종일 일정<br>DATETIME - 시간 일정 |
| --sdate, --start-date | Y | 일정 시작일자 | --pt 가 DATE 일 경우<br>  YYYY-MM-DD<br>---pt 가 DATETIME 일 경우<br>  YYYY-MM-DDTHH:mm:ss |
| --edate, --end-date | Y | 일정 종료일자 | --pt 가 DATE 일 경우<br>  YYYY-MM-DD<br>---pt 가 DATETIME 일 경우<br>  YYYY-MM-DDTHH:mm:ss |
| --tz, --time-zone | N | Timezone | 기본값 : Asia/Seoul |
| --rs, --repeat-schedule | N | Set to True | 해당 일정이 반복 일정일 경우 선언 |
| --rf, --repeat-frequency | N | DAILY | WEEKLY | MONTHLY | YEARLY | 반복 일정 주지 |
| --rd, --repeat-day | N | SU, MO, TU, WE, TH, FR, SA | 반복 일정 시 해당 일정이 반복될 요일<br>콤마로 구분하며 붙여서 사용<br>ex) --rd MO,WE,FR |
| --rm, --repeat-month | N | 1 ~ 12 | 일정이 반복 수행될 월 지정<br>콤마로 구분하며, 붙여서 사용<br>ex) --rm 4,6,8 |
| --udate, --until-date-time | N | YYYYMMDDTHHmmssZ | 반복 일정의 종료 일자<br>ex) --udate 20230930T000000Z |

### Options

**Sample**

```
**worksapi.py -P --p --m** 617e0a36-9a01-4c9f-1547-03cfa5eba194 \
--cid b27caefa-ddb3-44aa-b1b8-2e61f30a2b67 \
--summary "Hello World" \
--des "This is hello World Test Plan" \
--pt DATETIME \
--sdate 2023-05-02T22:00:00 \
--edate 2023-05-02T23:00:00 \
--rs --ri 2 \
--rf WEEKLY \
--rd mo,we,fr \
--rm 5,7 \
--udate 20230930T000000Z
```

```
**# ArgParse Info**
cid='b27caefa-ddb3-44aa-b1b8-2e61f30a2b67', 
des='This is hello World Test Plan',
udate='20230930T000000Z',
pt='DATETIME', 
sdate='2023-05-02T22:00:00', 
edate='2023-05-02T23:00:00', 
summary='Hello World', 
rs=True, 
ri='2', 
rf='WEEKLY', 
rd='mo,we,fr', 
rm='5,7', 
tz='Asia/Seoul'
```
