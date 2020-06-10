def url_rule(url: str) -> str:
	"""
	Вспомогательная функция для задания правила уникальности url.
	:param url: проверка уникальности будет игнорировать данный url.
	"""
	return f'u:<{url}>'


def domain_rule(domain: str) -> str:
	"""
	Вспомогательная функция для задания правила уникальности domain.
	:param domain: проверка уникальности будет игнорировать все url, начинающиеся с domain.
	"""
	return f'b:<{domain}>'


def regex_rule(regex: str) -> str:
	"""
	Вспомогательная функция для задания правила уникальности по regex.
	:param domain: проверка уникальности будет игнорировать все url, подходящие по заданное регулярное выражение.
	"""
	# FIXME экранировать слеш и кавычки
	return f'r:<{regex}>'


def clean_text(text: str) -> str:
	"""
	Подготавливает текст.
	Если в тексте есть переносы строк (абзацы, списки и т. п.) они заменяются на символ "\n" без кавычек.
	"""
	stop_list = ['•', '‣', '⁃', '⁌', '⁍', '∙', '◦', '§', '¶']
	text = text.encode('utf-8').decode('utf-8')
	for char in stop_list:
		text = text.replace(char, '\n')
	return text


class AdvanceReport(object):
	"""
	Вспомогательный класс отчета по анализу текста на антиплагиат.
	Сопоставляет номера слов в отчете с текстом и предоставляет более наглядный вид.
	"""
	def __init__(self, report_data: dict, text: str) -> None:
		"""
		Инициализация.
		:param report_data: Данные отчета.
		"""
		self.report_data = report_data
		# FIMME Распарсить дикт в атрибуты объекта
		pass