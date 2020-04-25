#!/usr/bin/python3

import argparse
import os
import json
import re

from lxml import html
import requests

PATH_EXPR = 'data_raw/json/expr.json'

def verify_file(file_path):

	"""
	Verifies that the input file is workable
	"""

	try:
		with open(file_path, 'r') as f:
			data = f.read()
		assert len(data) > 0
		return True

	except AssertionError:
		raise Exception("There doesn't seem to be data in the file.")
	except FileNotFoundError:
		raise Exception("Bad file", "The input file path you provided could not be found.")
	except:
		raise BadFileException("Unhandled exception in the file path you provided.")

def create_expr_list(expr_data):

	"""
	A simple function that creates 
	one massive list of all the readings
	(both keb and reb) of all expressions.

	Returns a list of dictionaries where
	each dictionary contains the expression
	and the meaning.
	"""

	expr_list_all = []

	for expr in expr_data:
		expr_pack = {}
		expr_pack['meaning'] = expr['meaning']
		expr_pack['readings_all'] = []

		if 'keb' in expr.keys():
			expr_pack['readings_all'].extend([
						x.strip() for x in expr['keb'].split('; ') if x != ''])
		if 'reb' in expr.keys():
			expr_pack['readings_all'].extend(
						[x.strip() for x in expr['reb'].split('; ') if x != ''])

		expr_list_all.append(expr_pack)

	return expr_list_all

def prettify_output(expr_found):

	"""
	Takes a list of expressions found and
	makes it pretty for display on a terminal.
	"""

	# ANSI Formatting
	bold = '\033[1m'
	warning = '\033[93m'
	endc = '\033[0m'

	final_out = ''

	unique_exprs = list(set([expr['expr_found'] for expr in expr_found]))

	for unique_expr in unique_exprs:

		common_snippets = [expr['snippet'] for expr in expr_found 
							if unique_expr == expr['expr_found']]

		meaning = [expr['meaning'] for expr in expr_found 
					if unique_expr == expr['expr_found']][0]

		expression_text = f'{bold}Expression{endc}\n{unique_expr}\n\n'
		meaning_text = f'{bold}Meaning{endc}\n{meaning}\n\n'

		final_out += '-+-+-+-\n'
		final_out += expression_text
		final_out += meaning_text
		final_out += f'{bold}Snippets: {endc}\n'

		for common_snippet in common_snippets:
			snippet_format_start = s = common_snippet.index(unique_expr)
			snippet_format_end = e = s + len(unique_expr)

			snippet_hl_text = f'{warning}{common_snippet[s:e]}{endc}'
			snippet_full_text = f'{common_snippet[:s]}{snippet_hl_text}{common_snippet[e:]}\n'

			final_out += snippet_full_text

		final_out += '-+-+-+-\n\n'

	print(final_out)

def process_url(url):

	"""
	If a url is provided as a command line argument,
	fetch the page and return a block of text that best
	represents the Japanese content on the website.
	"""

	print(f"Fetching {url}")

	page = requests.get(url)

	# Requests makes guesses about the encoding. Sometimes
	# it gets it wrong, for example:
	# https://www.city.itabashi.tokyo.jp/kenko/kansensho/mers/1022016.html

	page.encoding = 'utf-8'

	tree = html.fromstring(page.text)

	# Remove any script elements
	script_el_list = tree.xpath("//script")

	for script_el in script_el_list:
		script_el.getparent().remove(script_el)

	# Identify all Hiragana characters
	regex = u'[\u3040-\u309Fー]+'

	text_blocks_all = tree.xpath("//text()")

	text_blocks_ja = [x for x in text_blocks_all if re.search(regex, x, re.U)]

	full_text_ja = '\n\n'.join(text_blocks_ja)

	expr_found = parse_expressions(full_text_ja)

	return expr_found

def parse_expressions(text_block):

	"""
	Given a block of text, parse out the 
	expressions found.
	"""

	with open(PATH_EXPR, 'r') as f:
		data = json.loads(f.read())

	expr_list_all = create_expr_list(data)

	sentences = extract_sentences(text_block)

	expr_found = []

	for expr_pack in expr_list_all:
		readings_all = expr_pack['readings_all']
		for sentence in sentences:
			for reading in readings_all:
				if reading in sentence and len(reading) > 3:
					expr_meta = {}
					expr_meta['expr_found'] = reading
					expr_meta['snippet'] = sentence
					expr_meta['meaning'] = expr_pack['meaning']
					expr_found.append(expr_meta)

	return expr_found


def process_file(file_path):

	"""
	If a file is provided as a command line argument,
	process the file and return the final output.
	"""

	with open(file_path, 'r') as f:
		text_block = f.read()

	expr_found = parse_expressions(text_block)

	return expr_found
	

def extract_sentences(text_block):

	"""
	Given a block of text, return the list
	of sentences that make up the block of text.
	"""

	# To differentiate titles/headings from text

	sentences = []
	text_block = text_block.replace('\n\n', '。')

	sentences.extend([x for x in text_block.split('。')])

	return sentences

def main():

	parser = argparse.ArgumentParser()
	group = parser.add_mutually_exclusive_group(required=True)

	group.add_argument('-f', '--file', 
						help='A .txt file to find expressions in',
						type=str)

	group.add_argument('-u', '--url', 
						help='A url to parse and find expressions in',
						type=str)

	args = parser.parse_args()

	if args.file:
		filepath = args.file
		assert verify_file(filepath)
		expr_found = process_file(filepath)

	elif args.url:
		url = args.url
		expr_found = process_url(url)

	prettify_output(expr_found)


if __name__ == "__main__":

	main()


