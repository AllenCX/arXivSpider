# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class AxspiderPipeline(object):
	def __init__(self):
		self.file = open('axPipeline.json', 'wb+')
		self.msg = ""
		self.subject = "The spider has finished its job!"
		self.TO = "445631326@qq.com"

	def open_spider(self, spider):
		print("+"*80)

	def process_item(self, item, spider):
		line = json.dumps(dict(item)) + "\n"
		#without encode(), there will be an error...
		line = line.encode()
		self.file.write(line)
		return item

	def close_spider(self, spider):
		print("="*80)
		print("Now the spider ends!")
		print("="*80)

		self.file.close()

