
from lxml import etree
import json
import os

PATH_DATA = 'data_raw/jmdict/JMdict_e'
PATH_JSON_OUTPUT = 'data_raw/json'

def parse_keb(expr_entry):

	"""
	Given an expression entry, parse and
	return semi-colon delimited list of
	keb
	"""

	keb_list = expr_entry.xpath('k_ele/keb/text()')
	return '; '.join(keb_list)

def parse_reb(expr_entry):
	
	"""
	Given an expression entry, parse and
	return semi-colon delimited list of
	reb
	"""
	reb_list = expr_entry.xpath('r_ele/reb/text()')
	return '; '.join(reb_list)

def parse_gloss(expr_entry):
	
	"""
	Given an expression entry, parse and
	return semi-colon delimited list of
	meanings
	"""
	gloss_list = expr_entry.xpath('sense/gloss/text()')
	return '; '.join(gloss_list)


def main():

	with open(PATH_DATA, 'rb') as f:
		data = f.read()

	tree = etree.fromstring(data)

	# Getting all expressions

	expr_list = tree.xpath('''
					entry/sense/pos[contains(text(), 'expr')]
					/parent::sense
					/parent::entry''')

	# For all the expressions, create a nice JSON packet

	expr_json = []

	for expr_el in expr_list:
		expr = {}

		expr['ent_seq'] = expr_el.xpath('ent_seq/text()')[0]
		expr['keb'] = parse_keb(expr_el)
		expr['reb'] = parse_reb(expr_el)
		expr['meaning'] = parse_gloss(expr_el)

		expr_json.append(expr)

	with open(os.path.join(PATH_JSON_OUTPUT, 'expr.json'), 'w') as f:
		json.dump(expr_json, f)

if __name__ == "__main__":
	main()
