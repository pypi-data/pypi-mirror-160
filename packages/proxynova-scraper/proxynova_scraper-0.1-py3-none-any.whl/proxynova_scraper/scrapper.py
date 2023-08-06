from bs4 import BeautifulSoup
from .utils import _to_camelcase, _replace_chars

def _get_soup_instance(html: str):
	"""
		Returns a BeautifulSoup given an html string
		Arguments: 
			html: a string 
		Returns:
			A BeautifulSoup instance
	"""
	return BeautifulSoup(html, 'html.parser')

def _get_table_by_id(instance: BeautifulSoup, id: str):
	"""
		Finds an Table element by id
		Arguments:
			instance: a BeautifulSoup instance
			id: a string
		Returns:
			A BeautifulSoup instance (html table)
	"""
	return instance.find('table',id=id)

def _get_table_columns(table_instance: BeautifulSoup):
	"""
		Extracts all the column names from an html table
		Arguments:
			table_instance: BeautifulSoup instance
		Returns:
			An array of strings containing all the column names
	"""
	header_node = table_instance.find('thead')
	properties_nodes = (header_node.find('tr').select('th'))
	properties_strings = list(map(lambda node: _replace_chars(_to_camelcase(node.text)), properties_nodes))
	return properties_strings

def _get_table_content(table_instance: BeautifulSoup):
	"""
		Returns all table rows
		Arguments:
			table_instance: BeautifulSoup instance
		Returns:
			An array of tr elements
	"""
	return table_instance.find('tbody').select('tr')

def _generic_row_parser(row: BeautifulSoup, column_parser):
	"""
		Function that parses all the content of each row
		Arguments:
			row: BeautifulSoup instance
			column_parser: function that parses all the content of each column
		Returns:
			An array of the parsed values
	"""
	columns = row.find_all('td')
	row_values = []
	for index, column in enumerate(columns):
		row_values.append(column_parser(column, index))
	return row_values
