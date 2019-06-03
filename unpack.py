


def start_index(content, b):
	start = 0
	while start < len(content):
		if content[start] == b:
			break
		start += 1
	return start

def end_index(content, b):
	end = len(content) - 1
	while end > 0:
		if content[end] == b:
			break
		end -= 1
	return end

def unpack_json_block(content):
	new_content = ''
	count = 0
	char = 0
	start = start_index(content, '{')
	end = end_index(content, '}')
	content = content[start + 1:end]
	while char < len(content):
		if content[char] == '[':
			count += 1
		elif content[char] == ']':
			count -= 1
		if count > 0 and (content[char] == ' ' or content[char] == ','):
			new_content = new_content + '^'
		else:
			new_content = new_content + content[char]
		char += 1

	for values in new_content.split(','):
		key = values[:values.find(':')]
		val = values[values.find(':'):]
		val = val.replace('^^', ' ').replace('^', ',')
		print('key ', key, ' val ', val)
		

def unpack_json_file(content, op, cls):
	
	new_content = ''
	count = 0
	char = 0
	start = start_index(content, '{')
	end = end_index(content, '}')
	content = content[start + 1:end]
	while char < len(content):
		
		if content[char] == op:
			count += 1
		elif content[char] == cls:
			count -= 1
		if count > 0 and (content[char] == ' ' or content[char] == ','):
			if content[char] == ' ':
				new_content = new_content + '^'
			else:	
				new_content = new_content + '***'
		else:
			new_content = new_content + content[char]	
		char += 1

	return new_content

def unittest(new_content):
	for values in new_content.split(','):
		key = values[:values.find(':')]
		val = values[values.find(':'):]
		val = val.replace('^^', ' ').replace('^', ',')
		print('key ', key, ' val ', val)
		


# import sys
# unpack_json_object(open(sys.argv[1]).read(), '[', ']')




