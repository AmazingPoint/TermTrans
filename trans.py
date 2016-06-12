#!/usr/bin/python
# coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
from termcolor import colored
import re

import sqlite3
import os

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

	def ischinese(self, query_value):
		if re.match(r'[a-z]|[A-Z]', query_value) is None:
			return True
		else:
			return False


	def output(self, query_value):
		data = self.dotrans(query_value)
		if data is not None:
			self.checkstatus(data['errorCode'])

			print colored('有道翻译：', 'green')
			for value in data['translation']:
				print colored('\t %s', 'yellow') % value

			print colored('基本词典:', 'green')
			if 'basic' in data:
				if self.ischinese(query_value):
					if 'phonetic' in data['basic']:
						print colored('\t pinyin：%s', 'blue') % data['basic']['phonetic']
				else:
					if 'us-phonetic' in data['basic'] and 'uk-phonetic' in data['basic'] :
						print colored('\t uk: %s  us：%s', 'blue') %\
						 (data['basic']['uk-phonetic'], data['basic']['us-phonetic'])
				for value in data['basic']['explains']:
					print colored('\t %s','yellow') % value
			else:
				print colored('\tNone(没有合适的解释)', 'red')

		else:
			print '没有找到释义'

		dbpath = os.path.join(os.path.expanduser('~'),'.trans.db')
		conn = sqlite3.connect(dbpath)
		cur = conn.cursor()
		cur.execute('CREATE TABLE IF NOT EXISTS words(word VARCHAR(32), trans VARCHAR(128), count INTEGER)')

		rs = cur.execute('SELECT * FROM words WHERE word="'+query_value+'"').fetchall()
		if len(rs) > 0:
			count = cur.execute('SELECT count FROM words WHERE word="'+query_value+'"').fetchall()[0][0]
			newcount = int(count)+1
			cur.execute('UPDATE words SET count='+str(newcount)+' WHERE word="'+query_value+'"')
		else:
			tr = data['translation'][0]
			cur.execute('INSERT INTO words VALUES("'+query_value+'","'+ tr +'", 1)')
		cur.close()
		conn.commit()
		conn.close()




q = None

if len(sys.argv) > 1:
	if sys.argv[1].startswith('-'):
		if sys.argv[1] == '-l':
			dbpath = os.path.join(os.path.expanduser('~'),'.trans.db')
			conn = sqlite3.connect(dbpath)
			cur = conn.cursor()
			cur.execute('SELECT * FROM words ORDER BY count DESC')

			for eachword in cur.fetchall():
				colorname = 'yellow'
				rate = '低频'
				if(int(eachword[2])>4):
					rate = '高频'
					colorname = 'red'
				if(int(eachword[2]) < 5 and int(eachword[2]) > 2 ):
					rate = '中频'
					colorname = 'green'
				print colored('%s====>%s                %s次查询                 (%s)', colorname) % (eachword[0],eachword[1],eachword[2],rate)
			cur.close()
			conn.commit()
			conn.close()
		if sys.argv[1] == '-h':
			print 'you can use -l to list words you searched.'
			print 'you can use -h to show this help message.'
			print 'you can use trans word to trans'
	else:
		q = sys.argv[1]
		t = Trans()
		t.output(q)
else:
	print colored('请输入一个参数', 'red')


