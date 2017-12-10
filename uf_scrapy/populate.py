from subprocess import run
from datetime import datetime

scrapy_command = ['scrapy', 'crawl', 'uf_spider','-a', 'start_year=1977']
today = datetime.today()
if today.month == 12 and today.day >= 10:
    run(scrapy_command + ['-a', 'end_year='+str(today.year +1)])
else:
    run(scrapy_command + ['-a', 'end_year='+str(today.year)])