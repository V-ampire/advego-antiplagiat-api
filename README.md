# advego-antiplagiat-api

## Описание

Библиотека для работы с сервисом [антиплагиата](https://advego.com/v2/support/api/api-antiplagiat/1383) от [advego.ru](https://advego.com/)

## Установка



## Реализованные методы

### unique_text_add(text, title=None, ignore_rules=None)

Добавляет текст на проверку уникальности.

Параметры:
**text** - текст для проверки. Для корректной работы текст должен быть в кодировке **UTF-8**. если вы не знаете в какой кодировке ваш текст, вы можете воспользоваться библиотекой [chardet](https://pypi.org/project/chardet/). Пример использования библиотеки [*examples/text_encoding.py*]()