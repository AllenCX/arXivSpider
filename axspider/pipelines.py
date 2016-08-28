# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.mail import MailSender
from axspider.emailSender import send_mail

class AxspiderPipeline(object):
	def __init__(self):
		self.file = open('axPipeline.json', 'wb+')
		self.msg = "spider test"
		self.subject = "The spider has finished its job!"
		self.body = "spider test"
		self.to_list = ["445631326@qq.com"]

	def open_spider(self, spider):
		#self.mailer = MailSender.from_settings(spider.settings)
		print("+"*80)

	def process_item(self, item, spider):
		line = json.dumps(dict(item)) + "\n"
		#without encode(), there will be an error...
		line = line.encode()
		self.file.write(line)
		return item

	def close_spider(self, spider):
		self.msg = self.msg + " " + str(spider.article_num_today)
		send_mail(self.to_list, self.subject, self.msg)
		print("="*80)
		print("Now the spider ends!")
		print("="*80)
		#self.mailer.send(to=self.TO, subject=self.subject, body=self.body)
		self.file.close()

