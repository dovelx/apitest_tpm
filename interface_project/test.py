# -*- coding:utf-8 -*-
import testlink
from testlink import TestLinkHelper, TestlinkAPIClient

manual = 1  # 手动
automation = 2  # 自动

# 连接test link
url = "http://192.168.1.199/testlink/lib/api/xmlrpc/v1/xmlrpc.php"
key = "73bd9ba331e2c96cfcbe497d7cebfee6"  # 我这个key是错误的key
tlc = testlink.TestlinkAPIClient(url,devKey=key)
#获取testlink上的信息
def get_information_test_project():
    print("Number of Projects      in TestLink: %s " % tlc.countProjects())
    print("Number of Platforms  (in TestPlans): %s " % tlc.countPlatforms())
    print("Number of Builds                   : %s " % tlc.countBuilds())
    print("Number of TestPlans                : %s " % tlc.countTestPlans())
    print("Number of TestSuites               : %s " % tlc.countTestSuites())
    print("Number of TestCases (in TestSuites): %s " % tlc.countTestCasesTS())
    print("Number of TestCases (in TestPlans) : %s " % tlc.countTestCasesTP())
    tlc.listProjects()
#获取 test suite
def get_test_suite():
    projects = tlc.getProjects()
    top_suites = tlc.getFirstLevelTestSuitesForTestProject(projects[0]["id"])
    for suite in top_suites:
        print (suite["id"], suite["name"])
#创建测试用例集
def create_test_suite(project_id, test_suite_name, test_suite_describe, father_id):
    if father_id == "":
        tlc.createTestSuite(project_id, test_suite_name, test_suite_describe)
    else:
        tlc.createTestSuite(project_id, test_suite_name, test_suite_describe, parentid=father_id)
#创建测试用例
def create_test_case(father_id, data):
    #操作步骤
    tlc.initStep(data[0][2], data[0][3], automation)#操作步骤1
    for i in range(1, len(data)):
        tlc.appendStep(data[i][2], data[i][3], automation)#操作步骤2
    tlc.createTestCase(data[0][0], father_id, "1", "david", "我是摘要", preconditions=data[0][1])
#tlc.createTestCase(标题, father_id, "测试用例集ID", "david", "摘要", preconditions=前提)
#发送测试结果
def report_test_result(test_plan_id, test_case_id, test_result):
    tlc.reportTCResult(None, test_plan_id, None, test_result, "", guess=True,
                       testcaseexternalid=test_case_id, platformname="0")
#获取测试用例
def get_test_case(test_case_id):
    test_case = tlc.getTestCase(None, testcaseexternalid=test_case_id)
    for i in test_case:
        print  ("序列", "执行步骤", "预期结果")
        for m in i.get("steps"):
            print
            m.get("step_number"), m.get("actions"), m.get("expected_results")
#获取项目信息
#get_information_test_project()
#获取测试用例集
#get_test_suite()
#创建测试用例集
#create_test_suite("1", "c_by_python", "david no.1", "")

#创建测试用例
casedata =[["我是标题","2-前提","3-步骤1-1","4-期望结果1-1"],["5","6","步骤2-1","期望2-1"],["9","10","步骤3-1","期望3-1"]]
#create_test_case("35",casedata)
#获取测试用例
#get_test_case(10)
#通过用例名称获取用例ID
response = tlc.getTestCaseIDByName("我是标题", testprojectname="项目1")
print (response)
test_case = tlc.getTestCase(None, testcaseexternalid='10')
print(test_case)
