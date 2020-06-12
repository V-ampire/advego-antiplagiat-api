import pytest
from unittest.mock import patch

from antiplagiat.api import Antiplagiat
from antiplagiat import exceptions


token = 'test-token'

api = Antiplagiat(token)


def test_raise_char_account_error():
	with pytest.raises(exceptions.CharAccountError):
		api.raise_error('-1')

def test_raise_account_error():
	with pytest.raises(exceptions.AccountError):
		api.raise_error('-2')

def test_raise_database_error():
	with pytest.raises(exceptions.DatabaseError):
		api.raise_error('-5')

def test_raise_text_key_error():
	with pytest.raises(exceptions.TextKeyError):
		api.raise_error('-10')

def test_raise_token_error():
	with pytest.raises(exceptions.TokenError):
		api.raise_error('-11')

def test_raise_text_error():
	with pytest.raises(exceptions.TextError):
		api.raise_error('-13')

def test_raise_title_error():
	with pytest.raises(exceptions.TitleError):
		api.raise_error('-14')

def test_raise_add_check_error():
	with pytest.raises(exceptions.AddCheckError):
		api.raise_error('-17')

def test_raise_text_not_found_error():
	with pytest.raises(exceptions.TextNotFoundError):
		api.raise_error('-21')

def test_raise_not_enough_symbols_error():
	with pytest.raises(exceptions.NotEnoughSymbolsError):
		api.raise_error('-67')

def test_raise_api_error_error():
	with pytest.raises(exceptions.APIException):
		api.raise_error('999')


def test_prepare_params():
	api = Antiplagiat(token)
	method = 'test-method'
	method_params = {
		'name': 'test',
	}
	params = api.prepare_params(method, method_params)
	method_params.update({'token': api.token})
	expected = {"jsonrpc": "2.0", "method": method, "params": method_params, "id": 1}

	assert params == expected


def test_process_error_response():
	with patch('antiplagiat.api.Antiplagiat.raise_error') as mock_raise:
		error_code = '-1'
		response = {'result': {'error': error_code}}
		api.process_response(response)

		assert mock_raise.call_count == 1
		assert error_code in list(mock_raise.call_args)[0]


def test_process_fail_response():
	response = {'data': 'test-data'}
	with pytest.raises(exceptions.APIException) as e:
		exc = e
		api.process_response(response)

	assert str(response) in str(exc.value)


def test_process_success_response():
	response = {'result': {'data': 'test-data'}}
	result = api.process_response(response)

	assert response['result'] == result


@patch('antiplagiat.api.requests.post')
def test_process_rpc(mock_post):
	response_json = {"result": {"response": "mock_response"}}

	class MockResponse(object):
		@staticmethod
		def json():
			return response_json
		@staticmethod
		def raise_for_status():
			return True

	mock_post.return_value = MockResponse
	url = 'test-url'
	method = 'test-method'
	params = {'name': 'test'}
	response = api.process_rpc(url, method, params)
	expected_headers = {'User-Agent': 'Advego.Antiplagiat.API/Python'}

	assert response == response_json['result']
	assert f'{api.API_URL}{url}' in list(mock_post.call_args)[0]
	assert list(mock_post.call_args)[1]['headers'] == expected_headers


@patch('antiplagiat.api.Antiplagiat.process_rpc')
def test_unique_get_text(mock_rpc):
	expected_url = ''
	expected_method = 'unique_get_text'
	expected_params = {'key': 'test-key'}
	api.unique_get_text('test-key')

	assert expected_url in list(mock_rpc.call_args)[0]
	assert expected_method in list(mock_rpc.call_args)[0]
	assert expected_params in list(mock_rpc.call_args)[0]


@patch('antiplagiat.api.Antiplagiat.process_rpc')
def test_unique_recheck(mock_rpc):
	expected_url = ''
	expected_method = 'unique_recheck'
	expected_params = {'key': 'test-key'}
	api.unique_recheck('test-key')

	assert expected_url in list(mock_rpc.call_args)[0]
	assert expected_method in list(mock_rpc.call_args)[0]
	assert expected_params in list(mock_rpc.call_args)[0]


@patch('antiplagiat.api.Antiplagiat.process_rpc')
def unique_check(mock_rpc):
	expected_url = 'get'
	expected_method = 'unique_check'
	expected_params = {
		'key': 'test-key',
		'agent': 'shopchecker',
		'report_json': 1,
		'get_text': True
	}
	api.unique_check('test-key', 'shopchecker', get_text=True)

	assert expected_url in list(mock_rpc.call_args)[0]
	assert expected_method in list(mock_rpc.call_args)[0]
	assert expected_params in list(mock_rpc.call_args)[0]


@patch('antiplagiat.api.Antiplagiat.process_rpc')
@patch('antiplagiat.api.clean_text')
def test_unique_text_add(mock_clean, mock_rpc):
	expected_url = 'add'
	expected_method = 'unique_text_add'
	expected_text = 'cleaned-test-text'
	expected_title = 'test-title'
	expected_rules = ['rule1', 'rule2']
	expected_params = {
		'text': expected_text,
		'title': expected_title,
		'ignore_rules': expected_rules,
	}
	text = 'test-text'
	mock_clean.return_value = expected_text
	api.unique_text_add(text, title=expected_title, ignore_rules=expected_rules)

	assert expected_url in list(mock_rpc.call_args)[0]
	assert expected_method in list(mock_rpc.call_args)[0]
	assert expected_params in list(mock_rpc.call_args)[0]
	assert text in list(mock_clean.call_args)[0]





