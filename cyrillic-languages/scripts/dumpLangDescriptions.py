# -*- coding: utf-8 -*-

import json
import os.path

workpath = 'langlib'
outputpath = 'output'
codeslangfile = 'cyrillic_lib.json'
sortorderfile = 'sortorder_cyrillic.txt'
unicodelibfile = 'unicode14.txt'

with open(codeslangfile, "r") as read_file:
	data = json.load(read_file)

names = []

for item in data:
	# print(item)
	names.append(item['name_eng'])


textdata = []
for name in names:
	namefile = os.path.join(workpath, '%s.json' % name)
	with open(namefile, "r") as read_file:
		data = json.load(read_file)
	name_eng = data['name_eng']
	name_rus = data['name_rus']
	language_group = data['language_group']
	alt_names_eng = data['alt_names_eng']
	description_eng = data['description_eng']
	description_rus = data['description_rus']

	textdata.append('#### ' + name_eng)
	textdata.append('### Языковые группы')
	textdata.extend(language_group)
	# textdata.append('## Латинские названия')
	# textdata.extend(alt_names_eng)
	# textdata.append('# description english')
	# textdata.append(description_eng)
	textdata.append('# description russian')
	textdata.append(description_rus)
	textdata.append('')
	# textdata.append('')

for item in textdata:
	print(item)


