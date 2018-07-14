from scrapy import cmdline

cmdline.execute("scrapy crawl weibo -aurl_file=weibo_source/source".split())
