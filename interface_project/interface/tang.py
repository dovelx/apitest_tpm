# -*- coding:utf-8 -*-

__author__ = 'shouke'

import urllib.parse
import json

from globalpkg.log import logger
from htmlparser import  MyHTMLParser
from unittesttestcase import MyUnittestTestCase

step_output = None

class TANGRev(MyUnittestTestCase):
   def setUp(self):
       pass

   # 测试接口2
   def test_rev(self):
       '''提交body数据为json格式的POST请求'''

       header = {'Content-Type':'application/json','charset':'utf-8'}
       self.http.set_header(header)

       self.params = json.dumps(eval(self.params)) # 将参数转为url编码字符串# 注意，此处params为字典类型的数据
       self.params = self.params.encode('utf-8')

       response = self.http.post(self.url, self.params)
       print("return result:",response)
       #self.assertEqual(response['code'], 0, msg='返回code不等于0')

       logger.info('正在解析返回结果')
       #response = response.decode('gbk')  # decode函数对获取的字节数据进行解码
       TANGRev.step_output = response  # 保存返回结果供其它接口使用
       print("return result:", response)

   '''
       response = response.split('localAddress=')[1]
       response = response.split(',')[0]
       response = response.split(':')[1]
       response = response.replace('\"', '')

       self.assertEqual(response,  self.expected_result['city_name'], msg='city不为深圳市')
   '''

   def tearDown(self):
       pass