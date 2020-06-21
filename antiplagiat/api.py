from itertools import count
import requests
from typing import Union, Dict, List, Optional, NoReturn

from antiplagiat import exceptions
from antiplagiat.helpers import clean_text


class Antiplagiat(object):
	"""
	Api для доступа к системе антиплагиата advego.ru.
	"""
	_request_count = count(1)

	API_URL = 'https://api.advego.com/json/antiplagiat/'

	def __init__(self, token: str) -> None:
		"""
		Инициализация.
		:param token: Токен для доступа к api advego.ru.
		"""
		self.token = token

	def unique_text_add(self, text: str, title: str=None, ignore_rules: Optional[List[str]]=None) -> Dict:
		"""
		Добавляет текст на проверку уникальности.
		:param text: Текст, который нужно проверить;
		:optional title: Название проверки;
		:optional ignore_rules: Перечень правил, по которым будут игнорироваться сайты при проверки.
		"""
		params = {} # type: Dict
		params['text'] = clean_text(text)
		if title:
			params['title'] = title
		if ignore_rules:
			params['ignore_rules'] = ignore_rules
		return self.process_rpc('add', 'unique_text_add', params)

	def unique_check(self, key: str, agent: str=None, report_json: int=1, get_text: bool=False,) -> Dict:
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
			'report_json': report_json,
			'get_text': get_text
		}
		if agent:
			params['agent'] = agent
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

	def process_rpc(self, url: str, method: str, params: Dict, headers: Optional[Dict]=None) -> Dict:
		if not headers:
			headers = {}
		headers['User-Agent'] = "Advego.Antiplagiat.API/Python"
		data = self.prepare_params(method, params)
		response = requests.post(f'{self.API_URL}{url}', json=data, headers=headers)
		response.raise_for_status()
		return self.process_response(response.json())

	def process_response(self, response: Dict) -> Dict:
		"""
		Обработать ответ от антиплагиата.
		:param response: Словарь с ответом по протоколу json-rpc 2.0.
		"""
		result = response.get('result')
		if not result:
			raise exceptions.APIException(f'Неизвестный формат ответа: {response}')
		if isinstance(result, Dict) and result.get('error'):
			error = result['error'] # type: Union[str, int]
			self.raise_error(error)
		return result

	def prepare_params(self, method: str, params: Dict) -> Dict:
		"""
		Подготавливает данные для запроса по протоколу json-rpc 2.0.
		:param method: Название метода.
		:param params: Параметры запроса.
		"""
		id_ = next(self._request_count)
		params['token'] = self.token
		return {"jsonrpc": "2.0", "method": method, "params": params, "id": id_ }

	def raise_error(self, error_code: Union[str, int]) -> NoReturn:
		"""
		Обработка ошибок от антиплагиата. Выбрасывает исключение соответствующее коду ошибки.
		Если код не соответствует ниодной ошибке то выбрасывает APIException.
		:param error: Код ошибки.
		"""
		error_code = str(error_code)
		if error_code == '-1':
			raise exceptions.CharAccountError()
		if error_code == '-2':
			raise exceptions.AccountError()
		if error_code == '-5':
			raise exceptions.DatabaseError()
		if error_code == '-10':
			raise exceptions.TextKeyError()
		if error_code == '-11':
			raise exceptions.TokenError()
		if error_code == '-13':
			raise exceptions.TextError()
		if error_code == '-14':
			raise exceptions.TitleError()
		if error_code == '-17':
			raise exceptions.AddCheckError()
		if error_code == '-21':
			raise exceptions.TextNotFoundError()
		if error_code == '-67':
			raise exceptions.NotEnoughSymbolsError()
		raise exceptions.APIException(f'Ошибка API advego антиплагиат: {error_code}')
