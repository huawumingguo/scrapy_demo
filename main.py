# -*- coding: utf-8 -*-
import scrapy


from scrapy.cmdline import execute
import sys,os
print (os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#scrapy crawl jobbole
execute(['scrapy','crawl','anjuke_gz'])