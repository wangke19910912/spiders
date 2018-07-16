#!/usr/bin/python # -*- coding: UTF-8 -*- import scrapy import json
import MySQLdb
import urllib
import urllib2
import sys
import scrapy
import json

class UserNameSpider(scrapy.Spider):
    name = "user_name"
    allowed_domains = ["weibo.cn"]
    start_urls = []
    user_info_set = set()
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'} 

    def __init__(self, url_file=None, *args, **kwargs):
        super(UserNameSpider, self).__init__(*args, **kwargs)
        begin_urls=["https://m.weibo.cn/api/attitudes/show?id=4261474698359430&page=",
	"https://m.weibo.cn/api/attitudes/show?id=4261587185118373&page=",
	"https://m.weibo.cn/api/attitudes/show?id=4258349094364852&page=",
	"https://m.weibo.cn/api/attitudes/show?id=4260981699839481&page=",
	"https://m.weibo.cn/api/attitudes/show?id=4260717198290838&page=",
	"https://m.weibo.cn/api/attitudes/show?id=4261668668303105&page=",
	"https://m.weibo.cn/api/attitudes/show?id=4260766826307125&page=",
	"https://m.weibo.cn/api/attitudes/show?id=4261227570612682&page=",
	"https://m.weibo.cn/api/attitudes/show?id=4260595752700536&page=",
	"https://m.weibo.cn/api/attitudes/show?id=4261359165918958&page=",
	"https://m.weibo.cn/api/attitudes/show?id=4261060901561915&page="]
	for url in begin_urls:
	    for i in range(1,10):
                self.start_urls.append(url+str(i))	

    def parse(self, response):
	json_data = json.loads(response.body)
        isOK = json_data['ok']
	if isOK == 1:
	    data = json_data['data']['data']
	with open(self.file, 'a+') as f:
            for item in data:
	        user = item['user']	
	        name = user['screen_name'] 
	        pic = user['profile_image_url']
	        line = name +" " + pic + "\n"
	        f.write(line.encode('utf8'))
