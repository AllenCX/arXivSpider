# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.mail import MailSender
from axspider.emailSender import send_mail
import time

class AxspiderPipeline(object):
	def __init__(self):
		self.send_time = time.strftime("%Y%m%d", time.localtime())

		self.file = open('axPipeline.json', 'wb+')
		self.msg = ("Here are the articles published on arXiv today!<br>"
				+ "="*80 + '<br>')
		self.subject = ""
		
		#self.body = "spider test"
		self.to_list = ["445631326@qq.com"]

		self.total_num = 0

		self.msg_dict = dict()

	def assemble_msg(self, item):
		'''
		input:
			content: the item fetched by the spider, see axspider.py

		return:
			string, the email's body content.
		'''
		article_dict = dict(item)
		print(article_dict["sec_subject"])
		tmp_str = ("<h2>[{5}]{1}</h2>"
					"<p style='font-size:120%; line-height:120%'>"
					"<b>url:</b>{4}<br>"
					"<b>sec_subject:</b>{0}<br>"
					"<b>authors:</b>{2}<br>"
					"<b>abstract:</b>{3}<br>" + 
					"="*80 + '<br>'
					"</p>").format(article_dict["sec_subject"],article_dict["title"],
							article_dict["authors"],article_dict["abstract"],article_dict["url"],
							article_dict["num"])
		return tmp_str

	def assemble_msg_dict(self, item):
		pass

	def open_spider(self, spider):
		#self.mailer = MailSender.from_settings(spider.settings)
		print("+"*80)

	def process_item(self, item, spider):
		line = json.dumps(dict(item)) + "\n"

		tmp_dict = dict(item)
		#without encode(), there will be an error...
		order_index = ord(tmp_dict["sec_subject"][-2])*10 + ord(tmp_dict["sec_subject"][-1]) + tmp_dict["num"]
		self.msg_dict[order_index] = self.assemble_msg(item)
		line = line.encode()
		self.file.write(line)
		
		#self.msg += self.assemble_msg(item)
		self.total_num += 1
		return item

	def close_spider(self, spider):

		#Because scrapy concurrently process items, so we have to sort the message
		sortedkeys = sorted(self.msg_dict.keys())
		for i in sortedkeys:
			self.msg +=  self.msg_dict[i]
		print(sortedkeys)
		self.subject = ("[{0}] {1} new articles on arXiv.org!").format(self.send_time,self.total_num)
		send_mail(self.to_list, self.subject, self.msg, 'html')
		print("="*80)
		print("Now the spider ends!")
		print("="*80)
		#self.mailer.send(to=self.TO, subject=self.subject, body=self.body)
		self.file.close()

