import pprint
import argparse
import sys
import pickle
import os

class WpAPI:
    def test(self, args):
        print(args.jojo)
        
    def getParameter(self, configFileName : str):
        try:
            with open (configFileName, "rb") as f:
                return pickle.load(f)
        except:
            print("Unknown IO error occur.")
            print("Maybe there is a configuration file, but can't read.")
            print("Designate other file using -f or recreate configuration file")
            exit(1)

    def setDefParameter(self, configFileName : str, nameSpace : list, accessKey : str, secretKey : str, companyId : str):
        configParam = {}    
        data = self.getParameter(configFileName)
        
        if nameSpace[0] in data:
            nameSpaceExists = True
        else:
            data = None
            nameSpaceExists = False

        if nameSpaceExists:
            defParam = data[nameSpace[0]]
            configParam = {
                "accessKey" : accessKey if accessKey != None else defParam['accessKey'] if 'accessKey' in defParam else None,
                "secretKey" : secretKey if secretKey != None else defParam['secretKey'] if 'secretKey' in defParam else None,
                "companyId" : companyId if companyId != None else defParam['companyId'] if 'companyId' in defParam else None
            }
        else:
            configParam = {
                "accessKey" : accessKey if accessKey != None else None,
                "secretKey" : secretKey if secretKey != None else None,
                "companyId" : companyId if companyId != None else None
            }

        return configParam
    
    def manageConfigure(self, args):
        updateParam  = dict()
        newConfigure = dict()
        asisParam    = dict()
        isConfigureExists = os.path.isfile(args.f)
        
        if args.operationType == "ADD":
            if not args.a and not args.s and not args.i:
                print("No Arguments are set")
                print("\"configure add -h\" to help")
                exit(1)
            if isConfigureExists:
                asisParam = self.getParameter(args.f)
            else:
                paramFile=open(args.f,"wb")

            if args.n == None:
                args.n = ["default"]

            # Parameter Setting
            newConfigure = {
                "accessKey" : args.a if args.a != None else asisParam[args.n[0]]["accessKey"] if isConfigureExists else None,
                "secretKey" : args.s if args.s != None else asisParam[args.n[0]]["secretKey"] if isConfigureExists else None,
                "companyId" : args.i if args.i != None else asisParam[args.n[0]]["companyId"] if isConfigureExists else None 
            }
            
            if isConfigureExists:
                if args.n[0] in asisParam:
                    asisParam[args.n[0]].update(newConfigure)
                else:
                    asisParam[args.n[0]] = newConfigure

                with open(args.f,"wb") as paramFile:
                    pickle.dump(asisParam, paramFile)
                return     
            else:
                updateParam[args.n[0]] = newConfigure
                pickle.dump(updateParam, paramFile)
                paramFile.close()
                return
                
        elif args.operationType == "SHOW":
            data = self.getParameter(args.f)
            if data == None:
                print("Can't open configuration File.")
                exit(1)
            else:
                if args.n != None:
                    if args.n[0] in data:
                        pprint.pprint(data[args.n[0]], indent=2)
                    else:
                        print("There is no '" + args.n[0] + "' Namespace.")
                else:
                    pprint.pprint(data, indent=2)

    def manageOrganization(self, args):
        from workplace.OrgManage import OrgManage
        arguments = self.setDefParameter(args.f, args.n, args.a, args.s, args.i)       # Load defaults Param
        App = OrgManage(arguments["accessKey"], arguments["secretKey"], arguments["companyId"])

        if args.operationType == "QUERY":
            arguments.update({
                "externalKey" : args.k if args.k != None else None,
                "offset"      : args.offset if args.offset != None else None,
                "limit"       : args.limit  if args.limit != None else None
            }) 
            result = App.queryOrganization(arguments["externalKey"], arguments["offset"], arguments["limit"])
            if 'error' not in result:
                if args.dkn:
                    for resultCnt in range(0, len(result['elements'])):
                        print("\"" + result['elements'][resultCnt]['name'] + "\"," + "\"" + result['elements'][resultCnt]['externalKey'] + "\"")
                else:
                    pprint.pprint(result, indent=2)
        elif args.operationType == "ADD":
            pprint.pprint(App.addOrganization(args.extkey, args.name, args.order, args.pextkey, 
                                            args.email, args.remail), indent=2)
        elif args.operationType == "UPDATE":
            pprint.pprint(App.modOrganization(args.extkey, args.name, args.order, args.pextkey,
                                            args.deptno, args.pdeptno, args.email, args.remail), indent=2)
                        
    def manageEmployees(self, args):
        arguments = self.setDefParameter(args.f, args.n, args.a, args.s, args.i)       # Load defaults Param
        from workplace.EmpManage import EmpManage
        App = EmpManage(arguments["accessKey"], arguments["secretKey"], arguments["companyId"])
        if args.operationType == "QUERY":
            arguments.update({
                "externalKey" : args.k if args.k != None else None,
                "offset"      : args.offset if args.offset != None else None,
                "limit"       : args.limit  if args.limit != None else None
            })
            pprint.pprint(App.queryEmployees(arguments["externalKey"], arguments["offset"], arguments["limit"]), indent=2)
        elif args.operationType == "ADD":
            pprint.pprint(
                App.addEmployee(
                    args.k, args.id, args.email, args.joindt, args.name, args.deptkey, args.cdeptkey, args.emptype,
                    args.passtype, args.initpass, args.tel, args.cel, args.birth, args.gender, args.nick,
                    args.locale, args.tz, args.zip, args.addr, args.addrd, args.grade, args.job
                    ),
                indent=2
            )
        elif args.operationType == "DELETE":
            pprint.pprint(
                App.deleteEmployee(args.k),
                indent=2
            )


    def manageGrade(self, args):
        arguments = self.setDefParameter(args.f, args.n, args.a, args.s, args.i)       # Load defaults Param

        if args.operationType == "QUERY":
            arguments.update({
                "externalKey" : args.k if args.k != None else None,
                "offset"      : args.offset if args.offset != None else None,
                "limit"       : args.limit  if args.limit != None else None
            })
            
            from workplace.GrdManage import GrdManage
            App = GrdManage(arguments["accessKey"], arguments["secretKey"], arguments["companyId"])
            pprint.pprint(App.queryGrade(arguments["externalKey"], arguments["offset"], arguments["limit"]), indent=2)
            
    def manageJob(self, args):
        arguments = self.setDefParameter(args.f, args.n, args.a, args.s, args.i)       # Load defaults Param
        if args.operationType == "QUERY":
            arguments.update({
                "externalKey" : args.k if args.k != None else None,
                "offset"      : args.offset if args.offset != None else None,
                "limit"       : args.limit  if args.limit != None else None
            })
            from workplace.JobManage import JobManage
            App = JobManage(arguments["accessKey"], arguments["secretKey"], arguments["companyId"])
            pprint.pprint(App.queryJob(arguments["externalKey"], arguments["offset"], arguments["limit"]), indent=2)

    def manageEmpType(self, args):
        arguments = self.setDefParameter(args.f, args.n, args.a, args.s, args.i)       # Load defaults Param

        if args.operationType == "QUERY":
            arguments.update({
            "externalKey" : args.k if args.k != None else None,
            "offset"      : args.offset if args.offset != None else None,
            "limit"       : args.limit  if args.limit != None else None
            })
            from workplace.EmpTypeManage import EmpTypeManage
            App = EmpTypeManage(arguments["accessKey"], arguments["secretKey"], arguments["companyId"])
            pprint.pprint(App.queryEmpType(arguments["externalKey"], arguments["offset"], arguments["limit"]), indent=2)

if __name__ == "__main__":
    App=WpAPI()
    parser = argparse.ArgumentParser(description = "WORKS | WORKSPLACE API Management Program V2")
    parser.add_argument("--dkn", help="Display Key and Name", action="store_true", default=False)
    parserSub = parser.add_subparsers(title="Commands", description="Select what you want..", help="Description")
    ################################################################################
    # Configure                                                                    #
    ################################################################################
    parserSubConfigure = parserSub.add_parser('configure', help="Configuration")
    parserSubConfigureSub = parserSubConfigure.add_subparsers(title="Commands", description="You can add or delete configuration here.", help="Description", dest='CONFIGURE')
    ################################################################################
    # Configure - Add                                                              #
    ################################################################################
    parserSubConfigureSubAdd = parserSubConfigureSub.add_parser('add', description="You can pre define access key, secret key and company Id. These three items always required." ,help="Add Configuration")
    parserSubConfigureSubAdd.add_argument("-a", help = "Access Key", type = str, metavar = "Access Key")
    parserSubConfigureSubAdd.add_argument("-s", help = "Secret Key", type = str, metavar = "Secret Key")
    parserSubConfigureSubAdd.add_argument("-i", help = "Company Id", type = str, metavar = "Company Id")
    parserSubConfigureSubAdd.add_argument("-f", help = "Configure File. Default : .wpapi.config", type = str, metavar = "Configure file Name", default = ".wpapi.config")
    parserSubConfigureSubAdd.add_argument("-n", help = "Configuration Namespace. Default default", type = str, metavar = "Namespace", nargs=1, default = ["default"])
    parserSubConfigureSubAdd.set_defaults(operationType="ADD")
    parserSubConfigureSubAdd.set_defaults(func=App.manageConfigure)
    ################################################################################
    # Configure - Show                                                             #
    ################################################################################
    parserSubConfigureSubShow = parserSubConfigureSub.add_parser('show', help="Show Configuration")
    parserSubConfigureSubShow.add_argument("-n", help = "Configuration Namespace. Default default", type = str, metavar = "Namespace", nargs=1)
    parserSubConfigureSubShow.add_argument("-f", help = "Configure File. Default : .wpapi.config", type = str, metavar = "Configure file Name", default = ".wpapi.config")
    parserSubConfigureSubShow.set_defaults(operationType="SHOW")
    parserSubConfigureSubShow.set_defaults(func=App.manageConfigure)
    # # Configure - Trunc
    # parserSubConfigureSubTruncate = parserSubConfigureSub.add_parser("trunc", help="Truncate Configuration")
    # parserSubConfigureSubTruncate.add_argument('-n', help = "Configuration Namespace. if not define, truncate \"ALL\" namespace configuration", type = str, metavar = "Namespace", default=["default"], nargs='*')

    ################################################################################
    # Query                                                                        #
    ################################################################################
    parserSubQuery = parserSub.add_parser('query', help="Query Information")
    parserSubQuerySub = parserSubQuery.add_subparsers(title="Query Cateogry", description="Query any information here. Choose Category", help="Description", dest="QUERY")
    ################################################################################
    # Query - Org                                                                  #
    ################################################################################
    parserSubQuerySubOrg = parserSubQuerySub.add_parser("org", help="Query Organization Info")
    parserSubQuerySubOrg.set_defaults(func=App.manageOrganization)
    parserSubQuerySubOrgGrConfFile = parserSubQuerySubOrg.add_argument_group(title="Config File Option Group", description="You can use configuration file. If you use options on cli, options in configuration file will be overrided.")
    parserSubQuerySubOrgGrConfFile.add_argument("-f", help = "Use Configure File. Default : .wpapi.config", type = str, metavar = "Configure file Name", default = ".wpapi.config")
    parserSubQuerySubOrgGrConfFile.add_argument("-n", help = "Configuration Namespace. Default default", type = str, metavar = "Namespace", nargs=1, default = ["default"])
    parserSubQuerySubOrgGrAuth     = parserSubQuerySubOrg.add_argument_group(title="Authuntication Option Group")
    parserSubQuerySubOrgGrAuth.add_argument("-a", help = "Access Key", type = str, metavar = "Access Key")
    parserSubQuerySubOrgGrAuth.add_argument("-s", help = "Secret Key", type = str, metavar = "Secret Key")
    parserSubQuerySubOrgGrOption   = parserSubQuerySubOrg.add_argument_group(title="Query Organization Option Group")
    parserSubQuerySubOrgGrOption.add_argument("-i", help = "Company ID", type = str, metavar="companyId")
    parserSubQuerySubOrgGrOption.add_argument("-k", help = "Organization External Key", type = str, metavar="externalKey")
    parserSubQuerySubOrgGrOption.add_argument("--offset", help = "List offset. Ignore when -k set", type = int, metavar="Offset")
    parserSubQuerySubOrgGrOption.add_argument("--limit", help = "Page Limit. Ignore when -k set", type = int, metavar="Limit")
    parserSubQuerySubOrgGrOption.set_defaults(operationType="QUERY")
    ################################################################################
    # Query - Emp                                                                  #
    ################################################################################
    parserSubQuerySubEmp = parserSubQuerySub.add_parser("emp", help="Query Organization Info")
    parserSubQuerySubEmp.set_defaults(func=App.manageEmployees)
    parserSubQuerySubEmpGrConfFile = parserSubQuerySubEmp.add_argument_group(title="Config File Option Group", description="You can use configuration file. If you use options on cli, options in configuration file will be overrided.")
    parserSubQuerySubEmpGrConfFile.add_argument("-f", help = "Use Configure File. Default : .wpapi.config", type = str, metavar = "Configure file Name", default = ".wpapi.config")
    parserSubQuerySubEmpGrConfFile.add_argument("-n", help = "Configuration Namespace. Default default", type = str, metavar = "Namespace", nargs=1, default = ["default"])
    parserSubQuerySubEmpGrAuth     = parserSubQuerySubEmp.add_argument_group(title="Authuntication Option Group")
    parserSubQuerySubEmpGrAuth.add_argument("-a", help = "Access Key", type = str, metavar = "Access Key")
    parserSubQuerySubEmpGrAuth.add_argument("-s", help = "Secret Key", type = str, metavar = "Secret Key")
    parserSubQuerySubEmpGrOption   = parserSubQuerySubEmp.add_argument_group(title="Query Employee Option Group")
    parserSubQuerySubEmpGrOption.add_argument("-i", help = "Company ID", type = str, metavar="companyId")
    parserSubQuerySubEmpGrOption.add_argument("-k", help = "Employee External Key", type = str, metavar="externalKey")
    parserSubQuerySubEmpGrOption.add_argument("--offset", help = "List offset. Ignore when -k set", type = int, metavar="Offset")
    parserSubQuerySubEmpGrOption.add_argument("--limit", help = "Page Limit. Ignore when -k set", type = int, metavar="Limit")
    parserSubQuerySubEmpGrOption.set_defaults(operationType="QUERY")
    ################################################################################
    # Query - Grade                                                                #
    ################################################################################
    parserSubQuerySubGrd = parserSubQuerySub.add_parser("grade", help="Query Grade Info")
    parserSubQuerySubGrd.set_defaults(func=App.manageGrade)
    parserSubQuerySubGrdGrConfFile = parserSubQuerySubGrd.add_argument_group(title="Config File Option Group", description="You can use configuration file. If you use options on cli, options in configuration file will be overrided.")
    parserSubQuerySubGrdGrConfFile.add_argument("-f", help = "Use Configure File. Default : .wpapi.config", type = str, metavar = "Configure file Name", default = ".wpapi.config")
    parserSubQuerySubGrdGrConfFile.add_argument("-n", help = "Configuration Namespace. Default default", type = str, metavar = "Namespace", nargs=1, default = ["default"])
    parserSubQuerySubGrdGrAuth     = parserSubQuerySubGrd.add_argument_group(title="Authuntication Option Group")
    parserSubQuerySubGrdGrAuth.add_argument("-a", help = "Access Key", type = str, metavar = "Access Key")
    parserSubQuerySubGrdGrAuth.add_argument("-s", help = "Secret Key", type = str, metavar = "Secret Key")
    parserSubQuerySubGrdGrOption   = parserSubQuerySubGrd.add_argument_group(title="Query Grade Option Group")
    parserSubQuerySubGrdGrOption.add_argument("-i", help = "Company ID", type = str, metavar="companyId")
    parserSubQuerySubGrdGrOption.add_argument("-k", help = "Grade External Key", type = str, metavar="externalKey")
    parserSubQuerySubGrdGrOption.add_argument("--offset", help = "List offset. Ignore when -k set", type = int, metavar="Offset")
    parserSubQuerySubGrdGrOption.add_argument("--limit", help = "Page Limit. Ignore when -k set", type = int, metavar="Limit")
    parserSubQuerySubGrdGrOption.set_defaults(operationType="QUERY")
    ################################################################################
    # Query - Job                                                                  #
    ################################################################################
    parserSubQuerySubJob = parserSubQuerySub.add_parser("job", help="Query Job Info")
    parserSubQuerySubJob.set_defaults(func=App.manageJob)
    parserSubQuerySubJobGrConfFile = parserSubQuerySubJob.add_argument_group(title="Config File Option Group", description="You can use configuration file. If you use options on cli, options in configuration file will be overrided.")
    parserSubQuerySubJobGrConfFile.add_argument("-f", help = "Use Configure File. Default : .wpapi.config", type = str, metavar = "Configure file Name", default = ".wpapi.config")
    parserSubQuerySubJobGrConfFile.add_argument("-n", help = "Configuration Namespace. Default default", type = str, metavar = "Namespace", nargs=1, default = ["default"])
    parserSubQuerySubJobGrAuth     = parserSubQuerySubJob.add_argument_group(title="Authuntication Option Group")
    parserSubQuerySubJobGrAuth.add_argument("-a", help = "Access Key", type = str, metavar = "Access Key")
    parserSubQuerySubJobGrAuth.add_argument("-s", help = "Secret Key", type = str, metavar = "Secret Key")
    parserSubQuerySubJobGrOption   = parserSubQuerySubJob.add_argument_group(title="Query Job Option Group")
    parserSubQuerySubJobGrOption.add_argument("-i", help = "Company ID", type = str, metavar="companyId")
    parserSubQuerySubJobGrOption.add_argument("-k", help = "Job External Key", type = str, metavar="externalKey")
    parserSubQuerySubJobGrOption.add_argument("--offset", help = "List offset. Ignore when -k set", type = int, metavar="Offset")
    parserSubQuerySubJobGrOption.add_argument("--limit", help = "Page Limit. Ignore when -k set", type = int, metavar="Limit")
    parserSubQuerySubJobGrOption.set_defaults(operationType="QUERY")
    ################################################################################
    # Query - Employee Type                                                        #
    ################################################################################
    parserSubQuerySubEmpt = parserSubQuerySub.add_parser("emptype", help="Query Employee Type Info")
    parserSubQuerySubEmpt.set_defaults(func=App.manageEmpType)
    parserSubQuerySubEmptGrConfFile = parserSubQuerySubEmpt.add_argument_group(title="Config File Option Group", description="You can use configuration file. If you use options on cli, options in configuration file will be overrided.")
    parserSubQuerySubEmptGrConfFile.add_argument("-f", help = "Use Configure File. Default : .wpapi.config", type = str, metavar = "Configure file Name", default = ".wpapi.config")
    parserSubQuerySubEmptGrConfFile.add_argument("-n", help = "Configuration Namespace. Default default", type = str, metavar = "Namespace", nargs=1, default = ["default"])
    parserSubQuerySubEmptGrAuth     = parserSubQuerySubEmpt.add_argument_group(title="Authuntication Option Group")
    parserSubQuerySubEmptGrAuth.add_argument("-a", help = "Access Key", type = str, metavar = "Access Key")
    parserSubQuerySubEmptGrAuth.add_argument("-s", help = "Secret Key", type = str, metavar = "Secret Key")
    parserSubQuerySubEmptGrOption   = parserSubQuerySubEmpt.add_argument_group(title="Query Employee Type Option Group")
    parserSubQuerySubEmptGrOption.add_argument("-i", help = "Company ID", type = str, metavar="companyId")
    parserSubQuerySubEmptGrOption.add_argument("-k", help = "Employee Type External Key", type = str, metavar="externalKey")
    parserSubQuerySubEmptGrOption.add_argument("--offset", help = "List offset. Ignore when -k set", type = int, metavar="Offset")
    parserSubQuerySubEmptGrOption.add_argument("--limit", help = "Page Limit. Ignore when -k set", type = int, metavar="Limit")
    parserSubQuerySubEmptGrOption.set_defaults(operationType="QUERY")

    ################################################################################
    # Add                                                                          #
    ################################################################################
    parserSubAdd = parserSub.add_parser('add', help="Query Information")
    parserSubAdd.set_defaults(operationType="ADD")
    parserSubAddSub = parserSubAdd.add_subparsers(title="Add Cateogry", description="Query any information here. Choose Category", help="Description", dest="ADD")
    ################################################################################
    # Add - Org                                                                    #
    ################################################################################
    parserSubAddSubOrg = parserSubAddSub.add_parser("org", help="Add Employee Info")
    parserSubAddSubOrg.set_defaults(func=App.manageOrganization)
    parserSubAddSubOrgGrConfFile = parserSubAddSubOrg.add_argument_group(title="Config File Option Group", description="You can use configuration file. If you use options on cli, options in configuration file will be overrided.")
    parserSubAddSubOrgGrConfFile.add_argument("-f", help = "Use Configure File. Default : .wpapi.config", type = str, metavar = "Configure file Name", default = ".wpapi.config")
    parserSubAddSubOrgGrConfFile.add_argument("-n", help = "Configuration Namespace. Default default", type = str, metavar = "Namespace", nargs=1, default = ["default"])
    parserSubAddSubOrgGrAuth     = parserSubAddSubOrg.add_argument_group(title="Authuntication Option Group")
    parserSubAddSubOrgGrAuth.add_argument("-a", help = "Access Key", type = str, metavar = "Access Key")
    parserSubAddSubOrgGrAuth.add_argument("-s", help = "Secret Key", type = str, metavar = "Secret Key")
    parserSubAddSubOrgGrOption   = parserSubAddSubOrg.add_argument_group(title="Adding Organization Option Group")
    parserSubAddSubOrgGrOption.add_argument("-i", help = "Company ID", type = str, metavar="companyId")
    parserSubAddSubOrgGrOption   = parserSubAddSubOrg.add_argument_group(title="Required Info")
    parserSubAddSubOrgGrOption.add_argument("--name", help="Organization Name", type = str, metavar = "Name", required = True)
    parserSubAddSubOrgGrOption.add_argument("--extkey", help = "Organization External Key. Rquired", type = str, metavar="externalKey", required=True)
    parserSubAddSubOrgGrOption.add_argument("--pextkey", help="Parents departments ext key", metavar = "deptExtKey", type=str, default="#")
    parserSubAddSubOrgGrOption.add_argument("--order", help="Display order", metavar = "number", type=str)
    parserSubAddSubOrgGrOption   = parserSubAddSubOrg.add_argument_group(title="Optional Info")
    parserSubAddSubOrgGrOption.add_argument("--email", help="Organization Email", metavar = "email@email.com", type=str)
    parserSubAddSubOrgGrOption.add_argument("--remail", help="Allow Receive external mail.", action="store_true", default=False)

    ################################################################################
    # Add - Emp                                                                    #
    ################################################################################
    parserSubAddSubEmp = parserSubAddSub.add_parser("emp", help="Add Employee Info")
    parserSubAddSubEmp.set_defaults(func=App.manageEmployees)
    parserSubAddSubEmpGrConfFile = parserSubAddSubEmp.add_argument_group(title="Config File Option Group", description="You can use configuration file. If you use options on cli, options in configuration file will be overrided.")
    parserSubAddSubEmpGrConfFile.add_argument("-f", help = "Use Configure File. Default : .wpapi.config", type = str, metavar = "Configure file Name", default = ".wpapi.config")
    parserSubAddSubEmpGrConfFile.add_argument("-n", help = "Configuration Namespace. Default default", type = str, metavar = "Namespace", nargs=1, default = ["default"])
    parserSubAddSubEmpGrAuth     = parserSubAddSubEmp.add_argument_group(title="Authuntication Option Group")
    parserSubAddSubEmpGrAuth.add_argument("-a", help = "Access Key. if ommitted, use configuration file.", type = str, metavar = "Access Key")
    parserSubAddSubEmpGrAuth.add_argument("-s", help = "Secret Key. if ommitted, use configuration file.", type = str, metavar = "Secret Key")
    parserSubAddSubEmpGrOption   = parserSubAddSubEmp.add_argument_group(title="Adding Employee Option Group")
    parserSubAddSubEmpGrOption.add_argument("-i", help = "Company ID. if ommitted, use configuration file.", type = str, metavar="companyId")
    parserSubAddSubEmpGrOption.add_argument("-k", help = "Employee External Key", type = str, metavar="externalKey", required=True)
    parserSubAddSubEmpGrOption   = parserSubAddSubEmp.add_argument_group(title="Required Info")
    parserSubAddSubEmpGrOption.add_argument("--id", help="Login Id", type = str, metavar = "Login Id", required = True)
    parserSubAddSubEmpGrOption.add_argument("--email", help="Email Address", type = str, metavar = "Email", required = True)
    parserSubAddSubEmpGrOption.add_argument("--joindt", help="Join Day", type = str, metavar="yyyy-MM-dd", required = True)
    parserSubAddSubEmpGrOption.add_argument("--name", help="default Name", type = str, metavar = "Name", required = True)
    parserSubAddSubEmpGrOption.add_argument("--deptkey", help="Department Ext Key", type = str, metavar = "deptExtKey", required = True)
    parserSubAddSubEmpGrOption.add_argument("--cdeptkey", help="Concurrent Dept Key", metavar = "deptExtKey", type=str, nargs="*", default=[])
    parserSubAddSubEmpGrOption.add_argument("--emptype", help="Employee Type external Key", metavar = "empExtKey", type=str, required=True)
    parserSubAddSubEmpGrOption.add_argument("--passtype", help="Password Setting Type.", choices=["admin","user"], required=True)
    parserSubAddSubEmpGrOption.add_argument("--initpass", help="--passtype - ADMIN: initial passsword | USER: invite email", type=str, metavar="initial password | invited Password", required=True)
    parserSubAddSubEmpGrOption   = parserSubAddSubEmp.add_argument_group(title="Optional Info")
    parserSubAddSubEmpGrOption.add_argument("--tel", help="Telephone Number. without hypen(-)", metavar = "01000000000", type=str)
    parserSubAddSubEmpGrOption.add_argument("--cel", help="Cell Phone Number. without hypen(-)", metavar = "01000000000", type=str)
    parserSubAddSubEmpGrOption.add_argument("--birth", help="Birthday", type=str, metavar="yyyy-MM-dd")
    parserSubAddSubEmpGrOption.add_argument("--gender", help="Gender", choices=["male","female"], metavar="male|female")
    parserSubAddSubEmpGrOption.add_argument("--nick", help="Nick Name", type=str, metavar="nickname")
    parserSubAddSubEmpGrOption.add_argument("--locale", help="Locale Type.(ex: ko_KR, ja_JP). Ref: https://api.ncloud-docs.com/docs/busines-application-workplace-emp-v2#지원하는언어코드", metavar = "language/nation", type=str)
    parserSubAddSubEmpGrOption.add_argument("--tz", help="TimeZone. ex (Asia/Seoul). Ref: https://api.ncloud-docs.com/docs/busines-application-workplace-emp-v2#지원하는언어코드", metavar = "Region/City", type=str)
    parserSubAddSubEmpGrOption.add_argument("--zip", help="ZipCode", type=str, metavar="ZipCode")
    parserSubAddSubEmpGrOption.add_argument("--addr", help="Address", type=str, metavar="Address")
    parserSubAddSubEmpGrOption.add_argument("--addrd", help="Address Detail", type=str, metavar="Address")
    parserSubAddSubEmpGrOption.add_argument("--grade", help="Grade External Key", type=str, metavar="gradeExternalKey")
    parserSubAddSubEmpGrOption.add_argument("--job", help="Job External Key", type=str, metavar="jobExternalKey")


    ################################################################################
    # UPDATE                                                                       #
    ################################################################################
    parserSubMod = parserSub.add_parser('update', help="Update Information")
    parserSubMod.set_defaults(operationType="UPDATE")
    parserSubModSub = parserSubMod.add_subparsers(title="Update Cateogry", description="Update information here. Choose Category", help="Description", dest="UPDATE")
    ################################################################################
    # UPDATE - Org                                                                 #
    ################################################################################
    parserSubModSubOrg = parserSubModSub.add_parser("org", help="Modify Employee Info", description="*****### You should supply ALL INFORAMTION even not change ###*****")
    parserSubModSubOrg.set_defaults(func=App.manageOrganization)
    parserSubModSubOrgGrConfFile = parserSubModSubOrg.add_argument_group(title="Config File Option Group", description="You can use configuration file. If you use options on cli, options in configuration file will be overrided.")
    parserSubModSubOrgGrConfFile.add_argument("-f", help = "Use Configure File. Default : .wpapi.config", type = str, metavar = "Configure file Name", default = ".wpapi.config")
    parserSubModSubOrgGrConfFile.add_argument("-n", help = "Configuration Namespace. Default default", type = str, metavar = "Namespace", nargs=1, default = ["default"])
    parserSubModSubOrgGrAuth     = parserSubModSubOrg.add_argument_group(title="Authuntication Option Group")
    parserSubModSubOrgGrAuth.add_argument("-a", help = "Access Key", type = str, metavar = "Access Key")
    parserSubModSubOrgGrAuth.add_argument("-s", help = "Secret Key", type = str, metavar = "Secret Key")
    parserSubModSubOrgGrOption   = parserSubModSubOrg.add_argument_group(title="Adding Organization Option Group")
    parserSubModSubOrgGrOption.add_argument("-i", help = "Company ID", type = str, metavar="companyId")
    parserSubModSubOrgGrOption   = parserSubModSubOrg.add_argument_group(title="Required Info")
    parserSubModSubOrgGrOption.add_argument("--name", help="Organization Name", type = str, metavar = "Name", required = True)
    parserSubModSubOrgGrOption.add_argument("--extkey", help = "Organization External Key. Rquired", type = str, metavar="externalKey", required=True)
    parserSubModSubOrgGrOption.add_argument("--pextkey", help="Parents departments ext key", metavar = "deptExtKey", type=str, default="#")
    parserSubModSubOrgGrOption.add_argument("--order", help="Display order", metavar = "number", type=str)
    parserSubModSubOrgGrOption   = parserSubModSubOrg.add_argument_group(title="Optional Info")
    parserSubModSubOrgGrOption.add_argument("--deptno", help = "Organization Department Id. Rquired", type = str, metavar="deptNo")
    parserSubModSubOrgGrOption.add_argument("--pdeptno", help = "Organization Parent Department Id.", type = str, metavar="parentDeptNo")
    parserSubModSubOrgGrOption.add_argument("--email", help="Organization Email", metavar = "email@email.com", type=str)
    parserSubModSubOrgGrOption.add_argument("--remail", help="Allow Receive external mail.", action="store_true", default=False)
    ################################################################################
    # UPDATE - Emp                                                                 #
    ################################################################################
    parserSubModSubEmp = parserSubModSub.add_parser("emp", help="Update Employee Info", description="******You should supply ALL INFORMATION even not change******")
    parserSubModSubEmp.set_defaults(func=App.manageEmployees)
    parserSubModSubEmpGrConfFile = parserSubModSubEmp.add_argument_group(title="Config File Option Group", description="You can use configuration file. If you use options on cli, options in configuration file will be overrided.")
    parserSubModSubEmpGrConfFile.add_argument("-f", help = "Use Configure File. Default : .wpapi.config", type = str, metavar = "Configure file Name", default = ".wpapi.config")
    parserSubModSubEmpGrConfFile.add_argument("-n", help = "Configuration Namespace. Default default", type = str, metavar = "Namespace", nargs=1, default = ["default"])
    parserSubModSubEmpGrAuth     = parserSubModSubEmp.add_argument_group(title="Authuntication Option Group")
    parserSubModSubEmpGrAuth.add_argument("-a", help = "Access Key. if ommitted, use configuration file.", type = str, metavar = "Access Key")
    parserSubModSubEmpGrAuth.add_argument("-s", help = "Secret Key. if ommitted, use configuration file.", type = str, metavar = "Secret Key")
    parserSubModSubEmpGrOption   = parserSubModSubEmp.add_argument_group(title="Adding Employee Option Group")
    parserSubModSubEmpGrOption.add_argument("-i", help = "Company ID. if ommitted, use configuration file.", type = str, metavar="companyId")
    parserSubModSubEmpGrOption.add_argument("-k", help = "Employee External Key", type = str, metavar="externalKey", required=True)
    parserSubModSubEmpGrOption   = parserSubModSubEmp.add_argument_group(title="Required Info")
    parserSubModSubEmpGrOption.add_argument("--id", help="Login Id", type = str, metavar = "Login Id", required = True)
    parserSubModSubEmpGrOption.add_argument("--email", help="Email Address", type = str, metavar = "Email", required = True)
    parserSubModSubEmpGrOption.add_argument("--joindt", help="Join Day", type = str, metavar="yyyy-MM-dd", required = True)
    parserSubModSubEmpGrOption.add_argument("--name", help="default Name", type = str, metavar = "Name", required = True)
    parserSubModSubEmpGrOption.add_argument("--deptkey", help="Department Ext Key", type = str, metavar = "deptExtKey", required = True)
    parserSubModSubEmpGrOption.add_argument("--cdeptkey", help="Concurrent Dept Key", metavar = "deptExtKey", type=str, nargs="*", default=[])
    parserSubModSubEmpGrOption.add_argument("--emptype", help="Employee Type external Key", metavar = "empTypeExtKey", type=str, required=True)
    parserSubModSubEmpGrOption.add_argument("--passtype", help="Password Setting Type.", choices=["admin","user"], required=True)
    parserSubModSubEmpGrOption.add_argument("--initpass", help="if passtype is \"admin\": initial passsword or \"user\": invite email", type=str, metavar="[ initial password | invited Password ]", required=True)
    parserSubModSubEmpGrOption   = parserSubModSubEmp.add_argument_group(title="Optional Info") 
    parserSubModSubEmpGrOption.add_argument("--tel", help="Telephone Number. without hypen(-)", metavar = "01000000000", type=str)
    parserSubModSubEmpGrOption.add_argument("--cel", help="Cell Phone Number. without hypen(-)", metavar = "01000000000", type=str)
    parserSubModSubEmpGrOption.add_argument("--birth", help="Birthday", type=str, metavar="yyyy-MM-dd")
    parserSubModSubEmpGrOption.add_argument("--gender", help="Gender", choices=["male","female"], metavar="male|female")
    parserSubModSubEmpGrOption.add_argument("--nick", help="Nick Name", type=str, metavar="nickname")
    parserSubModSubEmpGrOption.add_argument("--locale", help="Locale Type.(ex: ko_KR, ja_JP). Ref: https://api.ncloud-docs.com/docs/busines-application-workplace-emp-v2#지원하는언어코드", metavar = "language/nation", type=str)
    parserSubModSubEmpGrOption.add_argument("--tz", help="TimeZone. ex (Asia/Seoul). Ref: https://api.ncloud-docs.com/docs/busines-application-workplace-emp-v2#지원하는언어코드", metavar = "Region/City", type=str)
    parserSubModSubEmpGrOption.add_argument("--zip", help="ZipCode", type=str, metavar="ZipCode")
    parserSubModSubEmpGrOption.add_argument("--addr", help="Address", type=str, metavar="Address")
    parserSubModSubEmpGrOption.add_argument("--addrd", help="Address Detail", type=str, metavar="Address")
    parserSubModSubEmpGrOption.add_argument("--grade", help="Grade External Key", type=str, metavar="gradeExternalKey")
    parserSubModSubEmpGrOption.add_argument("--job", help="Job External Key", type=str, metavar="jobExternalKey")

    ################################################################################
    # DELETE                                                                       #
    ################################################################################
    parserSubDel = parserSub.add_parser('delete', help="Update Information")
    parserSubDel.set_defaults(operationType="DELETE")
    parserSubDelSub = parserSubDel.add_subparsers(title="Delete Cateogry", description="Delete information here. Choose Category", help="Description", dest="DELETE")
    ################################################################################
    # DELETE - Emp                                                                 #
    ################################################################################
    parserSubDelSubEmp = parserSubDelSub.add_parser("emp", help="Delete Employee Info")
    parserSubDelSubEmp.set_defaults(func=App.manageEmployees)
    parserSubDelSubEmpGrConfFile = parserSubDelSubEmp.add_argument_group(title="Config File Option Group", description="You can use configuration file. If you use options on cli, options in configuration file will be overrided.")
    parserSubDelSubEmpGrConfFile.add_argument("-f", help = "Use Configure File. Default : .wpapi.config", type = str, metavar = "Configure file Name", default = ".wpapi.config")
    parserSubDelSubEmpGrConfFile.add_argument("-n", help = "Configuration Namespace. Default default", type = str, metavar = "Namespace", nargs=1, default = ["default"])
    parserSubDelSubEmpGrAuth     = parserSubDelSubEmp.add_argument_group(title="Authuntication Option Group")
    parserSubDelSubEmpGrAuth.add_argument("-a", help = "Access Key. if ommitted, use configuration file.", type = str, metavar = "Access Key")
    parserSubDelSubEmpGrAuth.add_argument("-s", help = "Secret Key. if ommitted, use configuration file.", type = str, metavar = "Secret Key")
    parserSubDelSubEmpGrOption   = parserSubDelSubEmp.add_argument_group(title="Delete Employee Option Group")
    parserSubDelSubEmpGrOption.add_argument("-i", help = "Company ID. if ommitted, use configuration file.", type = str, metavar="companyId")
    parserSubDelSubEmpGrOption.add_argument("-k", help = "Employee External Key", type = str, metavar="externalKey", required=True)


    if len(sys.argv) < 2:
        parser.parse_args(['-h'])   # Argparse Bug
    else:
        args=parser.parse_args()
        pprint.pprint(args, indent=2)
        if "QUERY" in args :
            if args.QUERY==None:
                parserSubQuery.parse_args(['-h'])
                exit(0)
        elif "ADD" in args:
            if args.ADD==None:
                parserSubAdd.parse_args(['-h'])
                exit(0)
        elif "UPDATE" in args:
            if args.UPDATE==None:
                parserSubMod.parse_args(['-h'])
                exit(0)
        elif "DELETE" in args:
            if args.DELETE==None:
                parserSubDel.parse_args(['-h'])
                exit(0)
        elif "CONFIGURE" in args:
            if args.CONFIGURE==None:
                parserSubConfigure.parse_args(['-h']) 
                exit(0)
        args.func(args)