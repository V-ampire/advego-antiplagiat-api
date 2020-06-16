# advego-antiplagiat-api

## Описание

Библиотека для работы с сервисом [антиплагиата](https://advego.com/v2/support/api/api-antiplagiat/1383) от [advego.ru](https://advego.com/)

## Установка



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
Python — высокоуровневый язык программирования общего назначения, ориентированный на повышение производительности разработчика и читаемости кода. Синтаксис ядра Python минималистичен. В то же время стандартная библиотека включает большой объём полезных функций.
"""

ignore_rules = [
	domain_rule('ru.wikipedia.org'), 
	url_rule('https://ru.wikipedia.org/wiki/Python'), 
	regex_rule('.*wikipedia\\.org')
]

result = api.unique_text_add(text, ignore_rules=ignore_rules)
key = result['key']
```

В случае если текст успешно добавлен на проверку метод возвращает словарь *`{'key': NNN}`*, где NNN - номер созданной проверки.

В случае ошибки будет выброшено исключение, см. [стандартные исключения](#exceptions).


**unique_check(key, agent=None, report_json=1, get_text=False)**



<a name="exceptions"></a>
## Стандартные исключения





