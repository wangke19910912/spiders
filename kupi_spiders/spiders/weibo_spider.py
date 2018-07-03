#!/usr/bin/python
# -*- coding: UTF-8 -*-
import scrapy
import json


class WeiboSpider(scrapy.Spider):
    name = "weibo"
    allowed_domains = ["weibo.cn"]
    start_urls = []

    def __init__(self, url_file=None, *args, **kwargs):
        super(WeiboSpider, self).__init__(*args, **kwargs)
        with open(url_file) as uf:	
	    for line in uf:
		index=line.find("page=1")
		if index != -1 :
		    self.start_urls.append(line[0:index+6])
			

    def parse(self, response):
        #filename = response.url.split("/")[-2]
 	filename  = "/Users/troy/workspace/local-code/scrapy/kupi_spiders/weibo_data/data"
        data = ""
	json_data = json.loads(response.body)
        cards = json_data['data']['cards']
        for card in cards:
	    if card['card_type'] == 9:
		mblog = card['mblog']
		blog_id = card['itemid']
 		text  = mblog['text'].encode('utf8')
		data = data + str(blog_id) +"	"+str(text)+"\n"
        	print("结束1")
        with open(filename, 'a') as f:
            f.write(data)
