# -*- coding:utf-8 -*-

__author__ = 'shouke'

import time
from globalpkg.log import logger
from globalpkg.globalpy import testcase_report_tb
from globalpkg.globalpy import executed_history_id
from globalpkg.globalpy import testdb
from globalpkg.globalpy import mytestlink
from testcase import TestCase
#from globalpkg.othertools import OtherTools


class TestSuite:
    def __init__(self, testsuite_id, testsuite_name, details, project_name):
        self.testsuite_id = testsuite_id
        self.testsuite_name = testsuite_name
        self.details = details
        self.project_name = project_name

    # 获取测试套件包含的所有用例的id
    def get_testcases_id_for_testsuite(self):
        testcases_id = mytestlink.getTestCasesForTestSuite(self.testsuite_id, False, 'only_id')
        return testcases_id

    # 获取测试套件包含的所有用例的完整信息
    def get_testcases_info_for_testsuite(self):
        testcase_info = mytestlink.getTestCasesForTestSuite(self.testsuite_id, True, 'full')
        return testcase_info

    # 获取测试套件的配置信息(ip,端口，协议)
    def get_testsuite_conf(self):
        return self.details

    # 获取测试套件所属项目
    def get_project_name(self):
        return self.project_name

    # 运行测试套件
    def run_testsuite(self, http):
        logger.info('正在获取套件[id=%s，name=%s]的测试用例...' % (self.testsuite_id, self.testsuite_name))
        testcases_id_list_for_testsuit = self.get_testcases_id_for_testsuite()

        for testcase_id in testcases_id_list_for_testsuit[:]:
            testcase_info = mytestlink.getTestCase(testcase_id)  # 获取测试用例基本信息
            #debug by david
            logger.info("测试用例信息%s"%testcase_info)
            # 构造测试用例对象

            testcase_name = testcase_info[0]['name']
            testcase_steps = testcase_info[0]['steps']
            #testcase_steps = testcase_steps[0]["actions"]
            testcase_isactive = int(testcase_info[0]['active'])
            #调试用by david
            #logger.info('输出用例信息 =====step===david========%s'%testcase_info)
            #处理测试用例的步骤
            #other_tools = OtherTools()
            #testcase_steps = other_tools.conver_date_from_testlink(testcase_steps)
            #示例testsuite_details = other_tools.conver_date_from_testlink(testsuite_info['details'])
            #logger.info('输出用例信息 ===处理后=====david========%s' % testcase_steps)


            testcase_obj = TestCase(testcase_id, testcase_name, testcase_steps, testcase_isactive, self.project_name)




            sql_insert = 'INSERT INTO '+testcase_report_tb +'(executed_history_id, testcase_id, testcase_name, testsuit, testplan, project, runresult, runtime)' \
                         ' VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'
            testplan = '无计划'
            #MODIFY BY DAVID BLOCK TO PASS
            data = (executed_history_id, testcase_id, testcase_name, self.testsuite_name, testplan, self.project_name, 'PASS','')
            logger.info('记录测试用例到到测试用例报表')
            testdb.execute_insert(sql_insert, data)

            logger.info('开始执行测试用例[id=%s，name=%s]' % (testcase_id, testcase_name))
            run_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 记录运行时间
            testcase_run_result = testcase_obj.run_testcase(http, testplan)

            logger.info('正在更新用例执行结果')
            sql_update = 'UPDATE '+testcase_report_tb +' SET runresult=\"%s\", runtime=\"%s\"' \
                         ' WHERE executed_history_id = %s and testcase_id = %s' \
                         ' AND project=\'%s\' AND testplan=\'%s\'' % \
                           (testcase_run_result, run_time, executed_history_id, testcase_id, self.project_name, testplan)
            testdb.execute_update(sql_update)

        logger.info('测试套件[id=%s ,name=%s]已执行完' % (self.testsuite_id, self.testsuite_name))
