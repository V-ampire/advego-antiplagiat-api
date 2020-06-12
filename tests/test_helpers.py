from antiplagiat import helpers
from tests.data import text


def test_url_rule():
	url = 'https://test.test'
	expected = f'u:<{url}>'

	assert helpers.url_rule(url) == expected


def test_domain_rule():
	domain = 'test.test'
	expected = f'b:<{domain}>'

	assert helpers.domain_rule(domain) == expected


def test_regex_rule():
	regex1 = r'.*my\.site'
	expected1 = f'r:<.*my\\.site>'

	assert helpers.regex_rule(regex1) == expected1


def test_clean_text():
	
	assert helpers.clean_text(text.dirty) == text.cleaned
