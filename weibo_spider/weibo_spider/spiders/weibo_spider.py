#!/usr/bin/python # -*- coding: UTF-8 -*-
import scrapy
import json
import MySQLdb
import urllib
import urllib2
import sys

class WeiboSpider(scrapy.Spider):
    name = "weibo"
    allowed_domains = ["weibo.cn"]
    start_urls = []
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'} 

    def __init__(self, url_file=None, *args, **kwargs):
        super(WeiboSpider, self).__init__(*args, **kwargs)
        with open(url_file) as uf:	
	    for line in uf:
		index=line.find("page=1")
		if index != -1 :
		    self.start_urls.append(line[0:index+5]+"1")
		    self.start_urls.append(line[0:index+5]+"2")
			

    def parse(self, response):
	db = MySQLdb.connect("39.104.94.203", "dboper", "DB2018kp!", "kp", charset='utf8' )
	cursor = db.cursor()
	json_data = json.loads(response.body)
        cards = json_data['data']['cards']
        for card in cards:
	    if card['card_type'] == 9:
		resultDic = {}
	        home = card['scheme']
		mblog = card['mblog']
		user = mblog['user']
		user_blog_id = card['itemid']
		blog_id = mblog['id']	
 		text  = mblog['text']
		if u"全文" in text:
		    request_url = 'https://m.weibo.cn/statuses/extend?id=' + str(blog_id)
		    print request_url
		    req = urllib2.Request(request_url,headers=self.headers)
		    res = urllib2.urlopen(req).read()
		    #type = sys.getfilesystemencoding()	
		    #print (res.decode('utf8').encode(type))
		    text = json.loads(res)['data']['longTextContent']

		resultDic['type']=0
		resultDic['home']=home
		resultDic['text']=text.replace("'","\"")
		resultDic['user']={}
		resultDic['user']['name']=user['screen_name']
		resultDic['user']['image']=user['profile_image_url']

		if 'pics' in mblog:
		    resultDic['type']=1
		    resultDic['pics_info']=mblog['pics']	
		elif 'page_info' in mblog and 'media_info' in mblog['page_info']:
		    resultDic['type']=2
		    resultDic['video_info']=mblog['page_info']
		else:
		    pass

		resultJson = json.dumps(resultDic,ensure_ascii=False)
		print resultJson
		select_sql = "SELECT COUNT(*) FROM crawl_origin_data \
                              WHERE thirdid = '%s'" % user_blog_id 

		insert_sql = "INSERT INTO crawl_origin_data(\
       		       thirdid, content, source, status) \
                       VALUES ('%s', '%s', '%d', '%d' )" % \
                       (user_blog_id,resultJson, 1,0)

		try:
		    print insert_sql
		    cursor.execute(select_sql)
		    if cursor.fetchone()[0]==0L :
		        cursor.execute(insert_sql)
	                db.commit()
		except Exception, e:
		    print e
		    db.rollback()
	db.close()