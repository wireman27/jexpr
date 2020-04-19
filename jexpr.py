#!/usr/bin/python3

import argparse
import os
import json

PATH_EXPR = 'data_raw/json/expr.json'

def verify_file(file_path):

	"""
	Verifies that the input file is workable
	"""

	try:
		with open(file_path, 'r') as f:
			data = f.read()
		assert len(data) > 0

	except AssertionError:
		raise Exception("There seems to be something with the input file.")
	except FileNotFoundError:
		raise Exception("Bad file", "The input file path you provided could not be found.")
	except:
		raise BadFileException("Unhandled exception in the file path you provided.")

def create_expr_list(expr_data):

	"""
	A simple function that creates 
	one massive list of all the readings
	(both keb and reb) of all expressions
	"""

	expr_list_all = []

	for expr in expr_data:
		if 'keb' in expr.keys():
			expr_list_all.extend([x.strip() for x in expr['keb'].split('; ')])
		if 'reb' in expr.keys():
			expr_list_all.extend([x.strip() for x in expr['reb'].split('; ')])

	# Quick haircut
	expr_list_all = [x for x in expr_list_all if x != ''] 

	return expr_list_all

def prettify_output(expr_found):

	"""
	Takes a list of expressions found and
	makes it pretty for display on a terminal

	Sample output:

	*Expression*:
	*Snippet*
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

		expression_text = f'{bold}Expression{endc}\n{unique_expr}\n\n'

		final_out += '-+-+-+-\n'
		final_out += expression_text
		final_out += f'{bold}Snippets: {endc}\n'

		for common_snippet in common_snippets:
			snippet_format_start = s = common_snippet.index(unique_expr)
			snippet_format_end = e = s + len(unique_expr)

			snippet_hl_text = f'{warning}{common_snippet[s:e]}{endc}'
			snippet_full_text = f'{common_snippet[:s]}{snippet_hl_text}{common_snippet[e:]}\n'

			final_out += snippet_full_text

		final_out += '-+-+-+-\n\n'

	print(final_out)


def process_file(file_path):

	"""
	If file is provided, process file
	
	1. Read file
	2. Extract sentences
	3. Return expressions
	"""

	with open(PATH_EXPR, 'r') as f:
		data = json.loads(f.read())

	with open(file_path, 'r') as f:
		text_block = f.read()

	expr_list_all = create_expr_list(data)

	sentences = extract_sentences(text_block)

	expr_found = []
	for expr in expr_list_all:
		for sentence in sentences:
			if expr in sentence and len(expr) > 3:
				expr_meta = {}
				expr_meta['expr_found'] = expr
				expr_meta['snippet'] = sentence
				expr_found.append(expr_meta)

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

	# for paragraph in paragraphs:
	# 	sentences.extend(paragraph.split('。'))

	return sentences

def main():

	"""
	Input can be one of:
		- A URL
		- A file
		- A string
	"""

	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--file', help='A .txt file to find expressions in')
	args = parser.parse_args()

	if args.file:
		expr_found = process_file(args.file)
		prettify_output(expr_found)


if __name__ == "__main__":

	main()


