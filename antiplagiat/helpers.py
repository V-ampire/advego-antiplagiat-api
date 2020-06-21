import json
from typing import Dict, List, NamedTuple, Union


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
	return f'r:<{regex}>'


def clean_text(text: str) -> str:
	"""
	Подготавливает текст.
	Если в тексте есть переносы строк (абзацы, списки и т. п.) они заменяются на символ "\n" без кавычек.
	"""
	stop_list = ['‣', '⁃', '⁌', '⁍', '∙', '◦', '§', '¶']
	for char in stop_list:
		text = text.replace(char, '\n')
	return text


class Layer(NamedTuple):
	"""
	Найденное совпадение.
	"""
	rewrite: Union[int, None]
	equality: Union[int, None]
	words: List[str]
	uri: Union[str, None]
	shingles: List[str]


class LayerByDomain(NamedTuple):
	"""
	Найденное совпадение на конкретном домене.
	"""
	rewrite: Union[int, None]
	equality: Union[int, None]
	layers: List[Layer]
	domain: Union[str, None]


class AdvanceReport(object):
	"""
	Вспомогательный класс отчета по анализу текста на антиплагиат.
	Сопоставляет номера слов в отчете с текстом и предоставляет более наглядный вид.
	Атрибуты объекта соответствуют ключам словаря report_data, за одним исключением:
	ключу len соответствует аттрибут length.
	"""
	def __init__(self, report_data: dict, text: str) -> None:
		"""
		Инициализация.
		:param report_data: Данные отчета.
		:param text: Проверяемый текст.
		"""
		# Базовые атрибуты
		self.report_data = report_data
		self.text = text
		self.text_words = text.split()
		self.rewrite = report_data.get('rewrite')
		self.equality = report_data.get('equality')
		self.uniqueness = 100 - self.equality if self.equality is not None else None
		self.originality = 100 - self.rewrite if self.rewrite is not None else None

		# Простые атрибуты
		self.error_pages = report_data.get('error_pages')
		self.layers_cnt = report_data.get('layers_cnt')
		self.id = report_data.get('id')
		self.captchas = report_data.get('captchas')
		self.domains_cnt = report_data.get('domains_cnt')
		self.urls_stats = report_data.get('urls_stats')
		self.length = report_data.get('len')
		self.checked_phrases = report_data.get('checked_phrases')
		self.progress = report_data.get('progress')
		self.word_count = report_data.get('word_count')
		self.error_phrases = report_data.get('error_phrases')
		self.lang = report_data.get('lang')
		self.found_pages = report_data.get('found_pages')
		self.checked_pages = report_data.get('checked_pages')

		# Списочные атрибуты
		self.sym_bins = report_data.get('error_pages', [])
		self.text_fragments = report_data.get('text_fragments', [])
		self.rewrite_per_bin = report_data.get('rewrite_per_bin', [])
		self.layers_by_domain = self.parse_layers_by_domain(report_data.get('layers_by_domain', []))
		self.layers = self.parse_layers(report_data.get('layers', []))
		self.equality_per_bin = report_data.get('equality_per_bin', [])
		self.equal_words = self.words_by_numbers(report_data.get('equal_words', []))
		self.word_bins = report_data.get('word_bins', [])
		self.equal_shingles = self.words_by_numbers(report_data.get('equal_shingles', []))
		self.bad_words = self.words_by_numbers(report_data.get('bad_words', []))
		self.equal_shingle_words = self.words_by_numbers(report_data.get('equal_shingle_words', []))

	def words_by_numbers(self, numbers: List[int]) -> List[str]:
		"""
		Возвращает список слов по номерам их расположения в тексте.
		"""
		return [self.text_words[n] for n in numbers]

	def parse_layers(self, layers: List[Dict]) -> List[Layer]:
		"""
		Распарсить совпадения в рамках одного домена.
		"""
		result = []
		for layer in layers:
			result.append(Layer(
				rewrite=layer.get('rewrite'),
				equality=layer.get('equality'),
				words=self.words_by_numbers(layer.get('words', [])),
				uri=layer.get('uri'),
				shingles=self.words_by_numbers(layer.get('shingles', []))
			))
		return result

	def parse_layers_by_domain(self, layers_by_domain: List[Dict]) -> List[LayerByDomain]:
		"""
		Распарсить совпадения, сгруппированные по доменам.
		"""
		result = []
		for domain_layer in layers_by_domain:
			result.append(LayerByDomain(
				rewrite=domain_layer.get('rewrite'),
				equality=domain_layer.get('equality'),
				layers=self.parse_layers(domain_layer.get('layers', [])),
				domain=domain_layer.get('domain'),
			))
		return result

	def save_as_json(self, file_path: str, indent: int=4) -> None:
		"""
		Сохранить отчет в json-файл.
		:param file_path: Путь до файла.
		:optional indent: Отступы в json-файле.
		"""
		with open(file_path, 'w') as fp:
			json.dump(self.report_data, fp, ensure_ascii=False, indent=indent)

