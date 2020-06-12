import pytest

from antiplagiat import exceptions


def test_api_exception_init():
	default_msg = 'Ошибка API advego антиплагиат'

	exc1 = exceptions.APIException()
	exc2 = exceptions.APIException('Test error')

	with pytest.raises(exceptions.APIException) as e:
		test_exc1 = e
		raise exc1

	with pytest.raises(exceptions.APIException) as e:
		test_exc2 = e
		raise exc2

	assert default_msg == test_exc1.value.args[0]
	assert 'Test error' == test_exc2.value.args[0]


