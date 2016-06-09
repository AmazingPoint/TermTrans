#!/usr/bin/python
# coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
from termcolor import colored

class Trans:

	APIKEY = '344912610'	
	KEYFROM = 'datastack'
	TYPE = 'data'
	DOCTYPE = 'json' 
	VERSION = '1.1'
	APIURL = 'http://fanyi.youdao.com/openapi.do'
	
	ERRORCODE = {
		0:'正常',
		20:'要翻译的文本过长',
		30:'无法进行有效的翻译',
		40:'不支持的语言类型',
		50:'无效的key',
		60:'无词典结果'
	}	

	def __init__(self):
		pass
	
	def dotrans(self, query_value):
		'''do translate, 从网络上获取翻译信息
		参数：query_value  要查询的词
		返回：网页获取内容'''
		
		if query_value is None or query_value == '':
			print colored('请输入您要查询的内容', 'red')
			return None
		params = self.makeparams(query_value)
		try:
			response = requests.get(self.APIURL,params=params)
			return response.json()
		except Exception as e:
			print colored('网络异常', 'red')
			print e
			return None
		

	def checkstatus(self, code):
		'''如果有错误，输出错误信息'''
		if code != 0:
			print colored(ERRORCODE[code], 'red')
	
	def makeparams(self, query_value):
		'''返回url参数'''
		params = {
			'keyfrom': self.KEYFROM,
			'key': self.APIKEY,
			'type': self.TYPE,
			'doctype': self.DOCTYPE,
			'version': self.VERSION,
			'q': query_value
		}
		return params
	
	def output(self, query_value):
		data = self.dotrans(query_value)
		if data is not None:
			self.checkstatus(data['errorCode'])
			print colored('有道翻译：', 'green')
			for value in data['translation']:
				print colored('\t %s', 'yellow') % value
			print colored('基本词典:', 'green')
			print colored('\t uk: %s  us：%s', 'blue') % (data['basic']['uk-phonetic'], data['basic']['us-phonetic'])
			for value in data['basic']['explains']:
				print colored('\t %s','yellow') % value



q = None
if sys.argv[1] is not None:
	q = sys.argv[1]
else:
	print colored('请输入一个参数', 'red')
t = Trans()
t.output(q)
