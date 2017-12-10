from subprocess import run
from datetime import datetime
from constants import *
import sys

today = datetime.today()
scrapy_command = ['scrapy', 'crawl', SPIDER_NAME, '-a']
if 'populate' in sys.argv:
    scrapy_command += ['start_year=1977']
else:
    scrapy_command += ['start_year='+str(today.year)]
run(scrapy_command)
