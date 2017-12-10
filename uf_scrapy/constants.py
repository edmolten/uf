from os import environ

BC_HOST = 'si3.bcentral.cl'
UF_URL = 'http://'+BC_HOST+'/IndicadoresSiete/secure/Serie.aspx?gcode=UF&param=RABmAFYAWQB3AGYAaQBuAEkALQAzADUAbgBNAGgAaAAkADUAVwBQAC4AbQBYADAARwBOAGUAYwBjACMAQQBaAHAARgBhAGcAUABTAGUAYwBsAEMAMQA0AE0AawBLAF8AdQBDACQASABzAG0AXwA2AHQAawBvAFcAZwBKAEwAegBzAF8AbgBMAHIAYgBDAC4ARQA3AFUAVwB4AFIAWQBhAEEAOABkAHkAZwAxAEEARAA%3d'
ALL_ROWS_XPATH = '//table[@id="gr"]//tr'
YEAR_XPATH = '//*[@id="lblAnioValor"]/text()'
VALUE_FORMATED_XPATH = './/td[{}]/span/text()'
DROPDOWN_YEAR_INPUT = 'DrDwnFechas'
API_CREATE_MANY_URL = 'http://ufservice:'+environ.get('PORT', '8000')+'/uf/'
SPIDER_NAME = 'uf_spider'
