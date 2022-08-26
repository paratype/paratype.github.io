# -*- coding: utf-8 -*-

import json
import os.path


descriptionsfile = 'langdesc-eng_e-25.08.2022.txt'

applyChanges = True
workPath = os.path.dirname(__file__)

libraryPath = 'library'  # langlib

print('*' * 60)
print('Started reload description')
print(workPath)
basePath, _s = os.path.split(workPath)
print('basePath: %s' % basePath)
libraryPath = os.path.join(basePath, libraryPath)
print('libraryPath: %s' % libraryPath)

filedesc = open(descriptionsfile, mode = 'r')

data = list(filedesc)
filedesc.close()

key = None
txt = ''
strukt = []
item = {}

def clearDangerSymbols(text):
	dangersymbols = {
		'\t': ' ',
		'\"': '\''
	}
	for k, v in dangersymbols.items():
		text = text.replace(k, v)
	return text


for idx, line in enumerate(data):
	# line = line.rstrip()

	# if line and not line.startswith('@') and not line.startswith(';'):
	if line.startswith('\n'):
		strukt.append(item)
		item = {}
	if line.startswith('####'):
		name_eng = line.replace('####','').strip()
		item['name_eng'] = name_eng
	if line.startswith('### Language'):
		textl = []
		for t in data[idx + 1:]:
			if t.startswith('# '):
				item['language_group_eng'] = textl
				break
			else:
				textl.append(clearDangerSymbols(t.rstrip()))
	if line.startswith('# description english'):
		textl = []
		for t in data[idx+1:]:
			if t.startswith('\n'):
				item['description_eng'] = ''.join(textl)
				break
			else:
				textl.append(clearDangerSymbols(t))

errpath = []
for item in strukt:
	name_eng = item['name_eng']
	print ('*'*30)
	print (name_eng)
	print('+' * 30)
	print (item['language_group_eng'])
	print('=' * 30)
	print (item['description_eng'])
	pathjson = os.path.join(libraryPath, '%s.json' % name_eng)
	print (pathjson)
	if os.path.exists(pathjson):
		print('path Ok')
		_data = {}
		namefile = os.path.join(libraryPath, '%s.json' % name_eng)
		with open(namefile, "r") as read_file:
			data = json.load(read_file)
		_data['name_eng'] = data['name_eng']
		_data['name_rus'] = data['name_rus']
		_data['local'] = data['local']
		_data['language_group_eng'] = item['language_group_eng']
		_data['language_group_rus'] = data['language_group_rus']
		_data['alt_names_eng'] = data['alt_names_eng']
		_data['description_eng'] = item['description_eng']
		_data['description_rus'] = data['description_rus']
		_data['glyphs_list'] = data['glyphs_list']
		for k,v in _data.items():
			print(k,v)
		outputJSONfile = namefile
		if applyChanges:
			with open(outputJSONfile, "w") as write_file:
				json.dump(_data, write_file, indent = 4, ensure_ascii = False)

	else:
		errpath.append((name_eng, pathjson))

for epath in errpath:
	print (epath)





