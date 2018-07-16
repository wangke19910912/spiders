# coding=utf-8
import urllib
import urllib2
import re
import MySQLdb

url = 'https://www.zhihu.com/topic/19607535/top-answers'
print url
request = urllib2.Request(url=url)
response = urllib2.urlopen(request, timeout=20)
#得到网页的html代码
result = response.read()
print result

#re模块的findall方法可以以列表的形式返回匹配的字符串，re.S表示多行匹配<a target="_blank" data-za-detail-view-element_name="Title" href="/question/36258497/answer/67785088">《琅琊榜》最打动你的细节是哪个？</a>
#使用re模块的正则表达式，将目标字符串存入list
list = re.findall('<a target="_blank" data-za-detail-view-element_name="Title"(.*?)/a>',result,re.S)
print list
#正则表示式也是个难点
p = '>(.*?)<'

for x in list:
    title = re.search(p,x,re.S).group(1)
    hot = "insert into test(title) values('%s')" % title
    print hot
