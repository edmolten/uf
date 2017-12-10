from subprocess import run
from datetime import datetime

scrapy_command = ['scrapy', 'crawl', 'uf_spider']
today = datetime.today()
if today.month == 12:
    run(scrapy_command + ['-a', 'start_year='+str(today.year), '-a', 'end_year='+str(today.year +1)])
else:
    run(scrapy_command + ['-a', 'start_year='+str(today.year), '-a', 'end_year='+str(today.year)])