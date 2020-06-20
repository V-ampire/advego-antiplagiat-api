from antiplagiat.helpers import AdvanceReport, LayerByDomain, Layer

import json


with open('tests/data/sample_text.txt', 'r') as fp:
	text = fp.read()

with open('tests/data/sample_report.json', 'r') as fp:
	data = json.load(fp)
	report_data = data.get('report')


adv_report = AdvanceReport(report_data, text)


def test_attributes():
	assert adv_report.report_data == report_data
	assert adv_report.text == text
	assert adv_report.text_words == text.split()
	assert adv_report.rewrite == report_data.get('rewrite')
	assert adv_report.equality == report_data.get('equality')

	# Простые атрибуты
	assert adv_report.error_pages == report_data.get('error_pages')
	assert adv_report.layers_cnt == report_data.get('layers_cnt')
	assert adv_report.id == report_data.get('id')
	assert adv_report.captchas == report_data.get('captchas')
	assert adv_report.domains_cnt == report_data.get('domains_cnt')
	assert adv_report.urls_stats == report_data.get('urls_stats')
	assert adv_report.length == report_data.get('len')
	assert adv_report.checked_phrases == report_data.get('checked_phrases')
	assert adv_report.progress == report_data.get('progress')
	assert adv_report.word_count == report_data.get('word_count')
	assert adv_report.error_phrases == report_data.get('error_phrases')
	assert adv_report.lang == report_data.get('lang')
	assert adv_report.found_pages == report_data.get('found_pages')
	assert adv_report.checked_pages == report_data.get('checked_pages')

	# Списочные атрибуты
	assert adv_report.sym_bins == report_data.get('error_pages', [])
	assert adv_report.text_fragments == report_data.get('text_fragments', [])
	assert adv_report.rewrite_per_bin == report_data.get('rewrite_per_bin', [])
	assert adv_report.equality_per_bin == report_data.get('equality_per_bin', [])


def test_words_by_numbers():
	numbers = report_data.get('equal_shingles', [])
	all_words = text.split()
	expected = [all_words[n] for n in numbers]
	assert expected == adv_report.words_by_numbers(report_data.get('equal_shingles', []))


def test_parse_layers():
	expected = []
	for layer in report_data.get('layers', []):
		expected.append(Layer(
			rewrite=layer.get('rewrite'),
			equality=layer.get('equality'),
			words=adv_report.words_by_numbers(layer.get('words')),
			uri=layer.get('uri'),
			shingles=adv_report.words_by_numbers(layer.get('shingles'))
		))
	assert expected == adv_report.parse_layers(report_data.get('layers', []))


def test_parse_layers_by_domain():
	expected = []
	for domain_layer in report_data.get('layers_by_domain', []):
		expected.append(LayerByDomain(
			rewrite=domain_layer.get('rewrite'),
			equality=domain_layer.get('equality'),
			layers=adv_report.parse_layers(domain_layer.get('layers')),
			domain=domain_layer.get('domain'),
		))
	assert expected == adv_report.parse_layers_by_domain(report_data.get('layers_by_domain', []))