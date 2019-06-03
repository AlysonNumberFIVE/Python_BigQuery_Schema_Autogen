
import sys
from unpack import unpack_json_file, start_index, end_index

def query_level(level):
	x = 0
	while x < level:
		print('    ', end='')
		x += 1

def small_indent(level):
	x = 0
	while x < level:	
		print('  ', end='')
		x += 1

def display_field(mode, name, type_name, indent_level):
	mode = mode + ','
	name = name + ','
	if type_name == '"RECORD",':
		mode = '"REPEATED",'
	query_level(indent_level+2)
	print('{')
	query_level(indent_level+3)
	print('"mode":', mode)
	query_level(indent_level+3)
	print('"name":', name)
	query_level(indent_level+3)
	print('"type":', type_name)


def repeated_loop(val, indent_level, key):
	val = val[start_index(val, '[') + 2:end_index(val, ']') - 1]
	repeated_items = val.split('} {')
	for item in repeated_items:
		item = '{' + item + '}'
		bigquery_schema_gen(item.replace(' ', ',').replace(':,', ':'), indent_level+1)

def convert_to_schema_block(key, val, indent_level):
	schema_value_type = ''
	val = val.strip()
	if len(val) == 0:
		return
	if val.isdigit():
		schema_value_type = '"INTEGER"'
	elif val[0] == '[':
		schema_value_type = '"RECORD",'
		display_field('"NULL"', key.strip(), schema_value_type, indent_level)
		query_level(indent_level+3)
		print('"fields": [')
		repeated_loop(val, indent_level+1, key.strip())
		query_level(indent_level+3)
		print(']')
		query_level(indent_level+2)
		print('},')
		return 
	elif val[0] == '{':
		schema_value_type = '"RECORD",'
		display_field('"NULLABLE"', key.strip(), schema_value_type, indent_level)
		query_level(indent_level+3)
		print('"fields": [')
		bigquery_schema_gen(val.strip(), indent_level+2)
		query_level(indent_level+3)
		print(']')
		query_level(indent_level+2)
		print('},')
		return 
	elif val[0] == '"':
		schema_value_type = '"STRING"'
	elif '.' in val:
		schema_value_type = '"FLOAT"'
	display_field('"NULLABLE"', key.strip(), schema_value_type, indent_level)
	query_level(indent_level+2)
	print('},')



def cleanly_separate_key_values(line):
	"""Find the delimiter that separates key from value.

	Splitting with .split() often yields inaccurate results
	as some values have the same delimiter value ':', splitting 
	the string too inaccurately.
	"""
	index = line.find(':')
	key = line[:index]
	value = line[index + 1:]
	return key, value
	
	
def bigquery_schema_gen(output, indent_level):
	"""Automate the generation of BigQuery schema if json file is flattened."""
	new_content = output	
	if '[' in output:
		new_content = unpack_json_file(output, '[', ']')
	if '{' in output:
		new_content = unpack_json_file(output, '{', '}')			
	for values in new_content.split(','):
		key = values[:values.find(':')]
		val = values[values.find(':') + 1:]
		val = val.replace('***', ',').replace('^', ' ')
		convert_to_schema_block(key, val, indent_level)


if len(sys.argv) != 2:
	print('Usage : %s [json file]' % sys.argv[0])
	sys.exit(1)
if not sys.argv[1].endswith('json'):
	print('Error : file must be a .json file')
	sys.exit(1)


print('schema = [')
bigquery_schema_gen(open(sys.argv[1]).read(), 1)
print(']')










