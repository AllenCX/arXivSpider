import scrapy

class axspider(scrapy.Spider):
	name = 'axspider'
	allowed_domains = ['arxiv.org']
	start_urls = [
				'https://arxiv.org/list/cs.CL/recent',
				'https://arxiv.org/list/cs.LG/recent',
				'https://arxiv.org/list/cs.CV/recent'
				]

	def __init__(self):
		self.article_num_today = 0
		self.sec_subject_list = list()

	def parse(self, response):
		article_num_today = response.xpath('//ul[1]/li[2]/a/@href').extract()
		article_num_today = int(article_num_today[0][article_num_today[0].find('m')+1:]) - 1
		self.article_num_today = article_num_today
		print("There are {0} articles published today!".format(article_num_today))
		print("processing " + response.url)
		#find the articles' url
		for i in range(article_num_today):
		#or i in range(2):
			article_xpath_tmp = "//a[@name = 'item{0}']/parent::*//a/@href".format(i+1)
			abs_url = "http://arxiv.org" + response.xpath(article_xpath_tmp)[0].extract()
			sec_subject = response.url.split('/')[-2]
			if sec_subject not in self.sec_subject_list:
				self.sec_subject_list.append(sec_subject)
			request = scrapy.Request(abs_url, callback=self.parse_articles)
			request.meta["num"] = i + 1
			request.meta["order_index"] = ord(sec_subject[-2]) * 100 + ord(sec_subject[-1]) * 10 + i + 1
			request.meta['sec_subject'] = response.url.split('/')[-2]
			yield request
			#print(scrapy.Request(abs_url, callback=self.parse_articles))

	def parse_articles(self, response):
		#print(response.url)
		#print("="*10)
		article_url = response.url

		title = response.xpath("//title/text()").extract()[0]
		title = " ".join(title.split())
		
		sec_subject = response.xpath("//div[@class='current']/text()").extract()[0]
		#return a list of authors
		authors = response.xpath("//div[@class='authors']//a/text()").extract()
		#type(authors) == list
		
		#according to the source code of the page, it will return a list
		abs_list = response.xpath("//blockquote[@class='abstract mathjax']/text()").extract()
		for i in abs_list:
			i = i.strip()
			if len(i) > 0:
				abstract = i
				break
		abstract = abstract.replace("\n", " ").strip()

		yield {
			'num' : response.meta["num"],
			'sec_subject':response.meta['sec_subject'],
			'title':title,
			'authors':authors,
			'abstract':abstract,
			'url':article_url,
			'order_index': response.meta["order_index"]
		}
