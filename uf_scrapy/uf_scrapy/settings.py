import os
import sys
import django

DJANGO_PROJECT_PATH = '/home/edmolten/Desktop/uf/uf_service/service_uf' #TODO CHANGE!!
DJANGO_SETTINGS_MODULE = 'service_uf.settings'
sys.path.append(DJANGO_PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_SETTINGS_MODULE
BOT_NAME = 'uf_scrapy'
SPIDER_MODULES = ['uf_scrapy.spiders']
NEWSPIDER_MODULE = 'uf_scrapy.spiders'
django.setup()

