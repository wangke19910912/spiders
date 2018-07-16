from scrapy import cmdline

cmdline.execute("scrapy crawl weibo -aurl_file=weibo_source/source -ausername_file=../user_name_spider/username".split())
