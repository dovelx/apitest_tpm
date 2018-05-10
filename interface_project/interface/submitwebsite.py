# -*- coding:utf-8 -*-

__author__ = 'shouke'

import json

from globalpkg.log import logger
from unittesttestcase import MyUnittestTestCase
from htmlparser import  MyHTMLParser

class SubmitWebsite(MyUnittestTestCase):
   def setUp(self):
       pass

      #测试提交网站
   def test_submit_website(self):
       '''演示POST请求，请求头内容类型为：Content-Type: application/x-www-form-urlencoded'''
       header = {'Content-Type':'application/x-www-form-urlencoded','charset':'utf-8','Cookie':'pharmconverge=7vql1rrh4pgslp9pjbpvm304b7'}
       self.http.set_header(header)

       #params = (self.params)[0]
       #params = str(params)
       #params = params.replace('|', ':')
       #params = params.encode('utf-8')
       #logger.info(params)

       # self.parmas = json.dumps(eval(self.params)) # 字符
       # logger.info(self.params)
       # self.params = self.params.encode('utf-8')


       logger.info('正在发起POST请求...')

       response = self.http.post(self.url)
       #response = self.http.post(self.url, params)
       #response = response.decode('utf-8')
       print (response)
       logger.info('正在解析返回结果:%s' % response)

       # 解析HTML文档
       #parser = MyHTMLParser(strict = False)
       #parser.feed(response)
       #self.assertNotEqual(str(i), self.expected_result['result'], msg='访问WebTours失败')
       logger.debug(response)
      # 断言
      # 略

   def tearDown(self):
       pass



