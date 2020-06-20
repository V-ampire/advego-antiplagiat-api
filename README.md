# advego-antiplagiat-api

## Описание

Библиотека для работы с сервисом [антиплагиата](https://advego.com/v2/support/api/api-antiplagiat/1383) от [advego.ru](https://advego.com/). Библиотека не является официальной, при обновлении сервисов advego возможно возникновение ошибок.


## Документация

[Документация по API](https://advego.com/v2/support/api/api-antiplagiat/1383)
[Как считается уникальность текста](https://advego.com/blog/read/faq_plagiatus/1298909/all1/)


## Требования
Python 3.8+

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


Формат возвращаемого отчета:
```
{
    "status": "done",
    "report": {
        "layers_by_domain": [
            {
                "rewrite": 33,
                "equality": 19,
                "layers": [
                    {
                        "equality": 19,
                        "rewrite": 33,
                        "uri": "https://site/",
                        "words": [
                            7,
                            30,
                            31,
                            32
                        ],
                        "shingles": [
                            31,
                            32,
                            33,
                            34,
                            35,
                            36,
                            37,
                            38
                        ]
                    },
            	],
            }
        ]
        "len": 1050,
        "bad_words": [],
        "equal_words": [
            0,
            1,
            3,
            5,
            7,
            15,
            19,
            20,
            22,
            24,
            25,
            27,
            28,
            30
        ],
        "word_count": 154,
        "lang": "russian",
        "error_pages": 0,
        "rewrite": 82,
        "progress": 100,
        "text_fragments": [
            "",
            "Слово1",
            " ",
            "Слово2",
            " ",
            "Слово3",
            " ",
            "Слово4",
            " ",
            "Слово5",
            ". "
        ],
        "captchas": 0,
        "found_pages": 11,
        "checked_pages": 48,
        "equal_shingles": [
            31,
            32,
            36,
            37,
            38,
            40
        ],
        "checked_phrases": 8,
    },
}
```

Расшифровка:

**layers_by_domain** - найденные страницы с совпадениями, сгруппированные по доменам (если найдено несколько страниц на одном сайте),

**layers** - найденные страницы линейным списком,

**equality** - количество найденных совпадений по фразам в указанном источнике (uri), процентов,

**rewrite** - количество найденных совпадений по словам в указанном источнике (uri), процентов,

**uri** - адрес страницы с найденными совпадениями,

**words** - слова, входящие в найденные совпадения по словам (см. text_fragments),

**shingles** - слова, входящие в найденные совпадения по фразам (см. text_fragments),

**len** - длина текста в символах с пробелами,

**bad_words** - слова с подменой символов,

**equal_words** - аналогично words, но для всего текста,

**equal_shingles** - аналогично shingles, но для всего текста,

**word_count** - количество слов в проверяемом тексте,

**text_fragments** - фрагменты текста для восстановления совпадений по словам и фразам.

Порядковый номер фрагмента вычисляется по формуле 2n + 1, где n = номеру, указанному в соответствущей секции words, shingles, equal_words и equal_shingles.


Для удобной работы с отчетом можно использовать вспомогательный класс `AdvanceReport`. Атрибуты этого класса соответствуют ключам словаря `report`, но в отличие от отчета получаемого от сервиса антиплагиата, такие значения как `words`,  `shingles`, `equal_words` и т.п. содержат не номера слов в тексте, а уже сами слова.


Исключение: ключу `len` соответствует атрибут `length`.


Также `AdvanceReport` предоставляет атрибуты `uniqueness` и `originality`, соответствующие значениям уникальности и оригинальности текста, подробнее см. [как считается уникальность текста](https://advego.com/blog/read/faq_plagiatus/1298909/all1/).


### Методы AdvanceReport


**words_by_numbers(numbers)**

Возвращает слова по номерам в тексте.

Параметры:

**numbers** - список номеров слов.


**save_as_json(file_path, indent=4)**

Сохранить отчет в json. Будет сохранен словарь, переданный при инициализации.

Параметры:

**file_path** - путь до файла.

**indent** - размер отступов.


Пример:
```
from antiplagiat import Antiplagiat, AdvanceReport


TOKEN = os.getenv('ADVEGO_TOKEN')

api = Antiplagiat(TOKEN)

text = """some text"""

# ... отправляем текст на проверку и получаем ключ key

result = api.unique_check(key)

adv_report = AdvanceReport(result.get('report'), text)

print(f'Уникальность текста {adv_report.uniqueness}/{adv_report.originality}')

print('Найденные источники:')
for domain in adv_report.layers_by_domain:
    for layer in domain.layers:
        print(layer.uri)
```


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
