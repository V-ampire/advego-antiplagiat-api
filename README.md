# advego-antiplagiat-api

## Описание

Библиотека для работы с сервисом [антиплагиата](https://advego.com/v2/support/api/api-antiplagiat/1383) от [advego.ru](https://advego.com/)

## Установка


## Пример использования
```
from antiplagiat import Antiplagiat

import time


TOKEN = os.getenv('ADVEGO_TOKEN')

api = Antiplagiat(TOKEN)

with open('example.txt', 'r') as fp:
	text = fp.read()


result = api.unique_text_add(text)
key = result['key']

while True:
	# дадим некоторое время на проверку
	time.sleep(200)
	result = api.unique_check(key)
	if result['status'] == 'done':
		print('Done!')
		# сделать чтото с отчетом
		return
	elif result['status'] == 'error':
		print(f'Error: {result}')
		return
	elif result['status'] == 'not found':
		print('Not found!')
		return
	else:
		print('In progress...')
```

## Реализованные методы

**unique_text_add(text, title=None, ignore_rules=None)**

Добавляет текст на проверку уникальности.

Параметры:

**text** - текст для проверки. Для корректной работы текст должен быть в кодировке **UTF-8**.

**title** - (необязательно) название проверки.

**ignore_rules** — (необязательно) перечень правил, по которым будут игнорироваться сайты при проверки.

Доступные правила:
- `"u:<url>"` - проверка уникальности будет игнорировать данный url;
- `"b:<domain>"` - проверка уникальности будет игнорировать все url, начинающиеся с domain;
- `"r:<regex>"` - проверка уникальности будет игнорировать все url, подходящие по заданное регулярное выражение. Если в регулярном выражении используется обратный слэш `\` или двойные кавычки `""`, их нужно экранировать.

Для задания правил также можно использовать вспомогательные функции из модуля [helpers.py](https://github.com/V-ampire/advego-antiplagiat-api/blob/master/antiplagiat/helpers.py).
```
from antiplagiat import Antiplagiat
from antiplagiat.helpers import url_rule, domain_rule, regex_url

TOKEN = 'token' # ваш токен
api = Antiplagiat(TOKEN)

text = """
Python — высокоуровневый язык программирования общего назначения, 
ориентированный на повышение производительности разработчика и читаемости кода. 
Синтаксис ядра Python минималистичен. 
В то же время стандартная библиотека включает большой объём полезных функций.
"""

ignore_rules = [
	domain_rule('ru.wikipedia.org'), 
	url_rule('https://ru.wikipedia.org/wiki/Python'), 
	regex_rule('.*wikipedia\\.org')
]

result = api.unique_text_add(text, ignore_rules=ignore_rules)
key = result['key']
```

В случае если текст успешно добавлен на проверку метод возвращает словарь `{'key': NNN}`, где NNN - номер созданной проверки.

В случае ошибки будет выброшено исключение, см. [стандартные исключения](#exceptions).



**unique_check(key, agent=None, report_json=1, get_text=False)**

Возвращает состояние проверки и [отчет](#report), если проверка выполнена.

Параметры:

**key** — идентификатор проверки, полученный при добавлении.

**get_text** - если указан, то вместе с отчетом будет возвращен проверенный текст.

**agent** - тип проверки, указывается чтобы получить результат проверки работы или статьи. Для проверки текста указывать agent не нужно.

**report_json** - формат отчета, рекомендуется значение 1.

Возможны следующие ответы:

- `{"msg": "", "status": "in progress"}` - проверка выполняется.

- `{"report": {...}, "status": "done", "text": "..."}` - проверка выполнена.

- `{"msg": "Error message", "status": "error_code"}` - проверка завершилась с ошибкой, где `"error_code"` код [ошибки](#exceptions).

- `{"msg": "", "status": "not found"}` - проверка с данным ключом не найдена.



**unique_recheck(key)**

Запускает новую проверку ранее добавленного текста. При этом удаляет предыдущие проверки из очереди.

Параметры:

**key** — идентификатор проверки, полученный при добавлении.

в случает успеха возвращает `1`.

В случае ошибки будет выброшено исключение, см. [стандартные исключения](#exceptions).



**unique_get_text(key)**

Возвращает текст на проверке.

Параметры:

**key** — идентификатор проверки, полученный при добавлении.

При успешном запросе возвращает словарь, содержащий проверяемый текст `{"text": "..."}`

В случае ошибки будет выброшено исключение, см. [стандартные исключения](#exceptions).


<a name="report"></a>
## Отчет

<a name="exceptions"></a>
## Стандартные исключения


**APIException** - общее исключение для ошибок при запросе сервиса антиплагиата. От него наследуются все остальные исключения.


**CharAccountError** - не хватает символов на счету. Код ошибки `-1`.


**AccountError** - не хватает денежных средств на счету. Код ошибки `-2`.


**DatabaseError** - ошибка подключения к БД. Код ошибки `-5`.


**TextKeyError** - получен неверный ключ. Код ошибки `-10`.


**TokenError** - ошибка авторизации по токену. Код ошибки `-11`.


**TextError** - ошибка при проверке поля text. Код ошибки `-13`.


**TitleError** - ошибка при проверке поля title. Код ошибки `-14`.


**AddCheckError** - ошибка добавления работы. Код ошибки `-17`.


**TextNotFoundError** - текст не найден. Код ошибки `-21`.


**NotEnoughSymbolsError** - недостаточно символов на счету, минимальное количество – 100 000. Код ошибки `-67`.





