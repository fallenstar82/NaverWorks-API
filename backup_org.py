from works.OrgManage import OrgManage
import time

with open('ak.token', 'r') as r:
    accToken = r.read()



App = OrgManage(accToken)
continueYN = 'Y'
cursor = None
while continueYN == 'Y':
    result = App.queryOrg(None, None, 100, cursor)
    creCsv = open("orgBackup.csv","a")
    for x in range(0,len(result['orgUnits'])):
        creCsv.write(result['orgUnits'][x]['orgUnitId']+","+result['orgUnits'][x]['orgUnitName']+"\n")
    creCsv.close()        
    if 'responseMetaData' in result:
        if 'nextCursor' in result['responseMetaData'] :
            if result['responseMetaData']['nextCursor'] != None:
                cursor = result['responseMetaData']['nextCursor']
                time.sleep(20)
            else:
                continueYN = "N"
        else:
            continueYN = "N"

