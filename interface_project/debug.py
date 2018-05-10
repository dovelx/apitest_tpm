# -*- coding:utf-8 -*-
__author__ = 'shouke'

import datetime
import json
import  time
import  configparser
import os.path

from globalpkg.log import logger
from globalpkg.globalpy import testdb
from globalpkg.globalpy import mytestlink
from globalpkg.globalpy import testcase_report_tb
from globalpkg.globalpy import case_step_report_tb
from globalpkg.globalpy import other_tools
from globalpkg.globalpy import executed_history_id
from config.runmodeconfig import RunModeConfig
from testsuite import TestSuite
from testplan import TestPlan
from testproject import TestProject
from httpprotocol import MyHttp
from htmlreporter import HtmlReport
from sendmail import MyMail

run_mode_conf = RunModeConfig('./config/runmodeconfig.conf')
run_mode = int(run_mode_conf.get_run_mode())
if 1:
        logger.info('按套件运行测试')
        testsuits_id_list = run_mode_conf.get_testsuits()
        logger.info('已获取配置的套件id列表：%s' % testsuits_id_list)

        testsuits_id_list = eval(testsuits_id_list)
        for testsuite_id in testsuits_id_list:
            # 构造测试套件对象
            try:
                testsuite_info = mytestlink.getTestSuiteByID(testsuite_id)
            except Exception as e:
                logger.error('测试套件[id=%s]不存在，暂时无法执行' % testsuite_id)
                continue
            testsuite_name = testsuite_info['name']

            print("testsuitename=%s"%testsuite_name)
            testsuite_details = other_tools.conver_date_from_testlink(testsuite_info['details'])
            print ("testsuite_details=%s"%testsuite_details)
            project = mytestlink.getFullPath(testsuite_id)
            print("project1=%s"%project)
            project = project[str(testsuite_id)][0]
            print("project2=%s" % project)
            testsuite_obj = TestSuite(testsuite_id, testsuite_name, testsuite_details, project)
            print("testsuite_obj=%s"%testsuite_obj)
            logger.info('正在读取套件[id=%s，name=%s]的协议，host，端口配置...' % (testsuite_id, testsuite_name))
            testsuite_conf = testsuite_obj.get_testsuite_conf()  # 获取套件基本信息
            print ("testsuite_conf=%s"%testsuite_conf)
            if '' == testsuite_conf:
                logger.error('测试套件[id=%s ,name=%s]未配置协议，host，端口信息，暂时无法执行' % (testsuite_id, testsuite_name))
                continue

            try:
                details = json.loads(testsuite_conf)
                print (details)
                protocol = details['protocol']
                host = details['host']
                port = details['port']
            except Exception as e:
                logger.error('测试套件[id=%s ,name=%s]协议，host，端口信息配置错误,未执行：%s'% (testsuite_id, testsuite_name, e))
                continue

            # 构造http对象
            #myhttp = MyHttp(protocol, host, port)

            #logger.info('正在执行测试套件[id=%s ,name=%s]' % (testsuite_id, testsuite_name))
            #testsuite_obj.run_testsuite(myhttp)