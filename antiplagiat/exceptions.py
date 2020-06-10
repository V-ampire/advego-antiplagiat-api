"""
-1 — не хватает символов на счету;
-2 — не хватает денежных средств на счету;
-5 — ошибка подключения к БД;
-10 — получен неверный ключ;
-11 — ошибка авторизации по токену;
-13 — ошибка при проверке поля text;
-14 — ошибка при проверке поля title;
-17 — ошибка добавления работы;
-21 — текст не найден;
-67 — not enough symbols – недостаточно символов на счету, минимальное количество – 100 000.
"""
class APIException(Exception):
	msg = 'Ошибка API advego антиплагиат'

	def __init__(self, msg=None, *args, **kwargs):
		if not msg:
			msg = self.msg
		return super().__init__(msg, *args, **kwargs)


class CharAccountError(APIException):
	code = -1
	msg = 'не хватает символов на счету'


class AccountError(APIException):
	code = -2
	msg = 'не хватает денежных средств на счету'


class DatabaseError(APIException):
	code = -5
	msg = 'ошибка подключения к БД'


class TextKeyError(APIException):
	code = -10
	msg = 'получен неверный ключ'


class TokenError(APIException):
	code = -11
	msg = 'ошибка авторизации по токену'


class TextError(APIException):
	code = -13
	msg = 'ошибка при проверке поля text'


class TitleError(APIException):
	code = -14
	msg = 'ошибка при проверке поля title'


class AddCheckError(APIException):
	code = -17
	msg = 'ошибка добавления работы'


class TextNotFoundError(APIException):
	code = -21
	msg = 'текст не найден'


class NotEnoughSymbolsError(APIException):
	code = -67
	msg = 'недостаточно символов на счету, минимальное количество – 100 000'


