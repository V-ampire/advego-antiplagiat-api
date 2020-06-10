from itertools import count
import requests
from typing import Union, Dict, List

from antiplagiat import exceptions
from antiplagiat.helpers import clean_text


class Antiplagiat(object):
	"""
	Api для доступа к системе антиплагиата advego.ru.
	"""
	_request_count = count()

	API_URL = 'https://api.advego.com/json/antiplagiat/'

	def __init__(self, token: str) -> None:
		"""
		Инициализация.
		:param token: Токен для доступа к api advego.ru.
		"""
		self.token = token

	def unique_text_add(self, text: str, title: str=None, ignore_rules: List[str]=None) -> Dict:
		"""
		Добавляет текст на проверку уникальности.
		:param text: Текст, который нужно проверить;
		:optional title: Название проверки;
		:optional ignore_rules: Перечень правил, по которым будут игнорироваться сайты при проверки.
		"""
		params = {}
		params['text'] = clean_text(text)
		if title:
			params['title'] = title
		if ignore_rules:
			params['ignore_rules'] = ignore_rules
		return self.process_rpc('add', 'unique_text_add', params)

	def unique_check(self, key: str, agent: str, report_json: int=1, get_text: bool=False,) -> Dict:
		"""
		Возвращает состояние проверки и отчет, если проверка выполнена.
		:param key: идентификатор проверки, полученный при добавлении;
		:param agent: тип проверки, указывается чтобы получить результат проверки работы или статьи;
		Возможные значения:
			- shopchecker - получить отчет о проверки статьи, key - id статьи;
			- jobchecker - получить отчет о проверки работы, key - id работы.
		:optional report_json: формат отчета, рекомендуется значение 1;
		:optional get_text: если указан, то вместе с отчетом будет возвращен проверенный текст;
		"""
		params = {
			'key': key,
			'agent': agent,
			'report_json': report_json,
			'get_text': get_text
		}
		return self.process_rpc('get', 'unique_check', params)


	def unique_recheck(self, key: str) -> Dict:
		"""
		Запускает новую проверку ранее добавленного текста. При этом удаляет предыдущие проверки из очереди.
		:param key: идентификатор проверки, полученный при добавлении.
		"""
		return self.process_rpc('', 'unique_recheck', {'key': key})

	def unique_get_text(self, key: str) -> Dict:
		"""
		Возвращает текст на проверке.
		:param key: идентификатор проверки, полученный при добавлении.
		"""
		return self.process_rpc('', 'unique_get_text', {'key': key})

	def process_rpc(self, url: str, method: str, params: Dict, headers=None) -> Dict:
		if not headers:
			headers = {}
		headers['User-Agent'] = "Advego.Antiplagiat.API/Python"
		data = self._prepare_params(method, params)
		response = requests.post(f'{self.API_URL}{url}', data=data, headers=headers)
		if response.status_code >= 400:
			pass
			#do smth
		return self.process_response(response.json())

	def process_response(self, response: Dict) -> Dict:
		"""
		Обработать ответ от антиплагиата.
		:param response: Словарь с ответом по протоколу json-rpc 2.0.
		"""
		result = response.get('result')
		if result.get('error'):
			self.raise_error(result.get('error'))
		return result

	def raise_error(self, error: str) -> Dict:
		"""
		Обработка ошибок от антиплагиата. Выбрасывает исключение соответствующее коду ошибки.
		Если код не соответствует ниодной ошибке то выбрасывает APIException.
		:param error: Код ошибки.
		"""
		if error == '-1':
			raise exceptions.CharAccountError()
		if error == '-2':
			raise exceptions.AccountError()
		if error == '-5':
			raise exceptions.DatabaseError()
		if error == '-10':
			raise exceptions.TextKeyError()
		if error == '-11':
			raise exceptions.TokenError()
		if error == '-13':
			raise exceptions.TextError()
		if error == '-14':
			raise exceptions.TitleError()
		if error == '-17':
			raise exceptions.AddCheckError()
		if error == '-21':
			raise exceptions.TextNotFoundError()
		if error == '-67':
			raise exceptions.NotEnoughSymbolsError()
		raise exceptions.APIException(f'Ошибка API advego антиплагиат: {error}')

	def prepare_params(self, method: str, params: Dict) -> Dict:
		"""
		Подготавливает данные для запроса по протоколу json-rpc 2.0.
		:param method: Название метода.
		:param params: Параметры запроса.
		"""
		id_ = self._request_count()
		params['token'] = self.token

		return {"jsonrpc": "2.0", "method": method, "params": params, "id": id_ }
