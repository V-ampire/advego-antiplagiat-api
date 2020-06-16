"""
Перед запуском примеров необходимо получить токен по адресу https://advego.com/antiplagiat/api/
и установить его в переменную окружения ADVEGO_TOKEN, например командой:
export ADVEGO_TOKEN=<token>
"""
from antiplagiat import Antiplagiat
import chardet
import os
import time


with open('./examples/texts/cp1251.txt', 'rb') as fp:
	bin_text = fp.read()

char_data = chardet.detect(bin_text)
encoding = char_data['encoding']
text = bin_text.decode(encoding)

if encoding != 'UTF-8':
	text = text.encode('utf-8').decode('utf-8')


token = os.getenv('ADVEGO_TOKEN')
api = Antiplagiat(token)

result = api.unique_text_add(text)

key = result['key']

while True:
	# Дадим время сервису выполнить проверку
	time.sleep(15)
	result = unique_check(key, agent='shopchecker')


