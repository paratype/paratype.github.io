# -*- coding: utf-8 -*-

import json
import os.path


descriptionsfile = 'langdesc-eng.txt'

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
				textl.append(t.rstrip())
	if line.startswith('# description english'):
		textl = []
		for t in data[idx+1:]:
			if t.startswith('\n'):
				item['description_eng'] = ''.join(textl)
				break
			else:
				textl.append(t)

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
		_data['uppercase_alphabet'] = data['uppercase_alphabet']
		_data['lowercase_alphabet'] = data['lowercase_alphabet']
		_data['uppercase_dialect'] = data['uppercase_dialect']
		_data['lowercase_dialect'] = data['lowercase_dialect']
		_data['uppercase_historic'] = data['uppercase_historic']
		_data['lowercase_historic'] = data['lowercase_historic']
		_data['uppercase_lexic'] = data['uppercase_lexic']
		_data['lowercase_lexic'] = data['lowercase_lexic']
		for k,v in _data.items():
			print(k,v)
		outputJSONfile = namefile
		with open(outputJSONfile, "w") as write_file:
			json.dump(_data, write_file, indent = 4, ensure_ascii = False)

	else:
		errpath.append((name_eng, pathjson))

for epath in errpath:
	print (epath)
#
# "name_eng": "Abkhazian",
# "name_rus": "Абхазский",
# "local": "CYR",
# "language_group": [
# 	"Северокавказские языки",
# 	"Абхазо-Адыгские (Западнокавказские) языки"
# ],
# "alt_names_eng": [
# 	"Abkhazian",
# 	"Bzyb",
# 	"Abzhui",
# 	"Samurzakan"
# ],
# "description_eng": "The modern Cyrillic-based Abkhaz alphabet was introduced in 1954 and reformed in the late 1990s. It consists of 26 letters of the Russian alphabet ( Ё, Й, Щ, Ъ, Э, Ю, Я are missing ) and a number of specific letters, ligatures and combinations.\nSigns important for the language that are not included in the alphabet are shown separately.\n",
# "description_rus": "Современный абхазский алфавит на основе кириллицы был введен в 1954 году и реформирован в конце 1990-х гг. Он состоит из 26 букв русского алфавита (отсутствуют Ё, Й, Щ, Ъ, Э, Ю, Я) и ряда специфических букв, лигатур и сочетаний.\nОтдельно показаны важные для языка знаки, не входящие в алфавит.",
# "uppercase_alphabet": "А Б В Г Гь Гә Ӷ Ӷь Ӷә Д Дә Е Ж Жь Жә З Ӡ Ӡә И К Кь Кә Қ Қь Қә Ҟ Ҟь Ҟә Л М Н О П Ԥ Р С Т Тә Ҭ Ҭә У Ф Х Хь Хә Ҳ Ҳә Ц Цә Ҵ Ҵә Ч Ҷ Ҽ Ҿ Ш Шь Шә Ы Ҩ Џ Џь Ь Ә",
# "lowercase_alphabet": "а б в г гь гә ӷ ӷь ӷә д дә е ж жь жә з ӡ ӡә и к кь кә қ қь қә ҟ ҟь ҟә л м н о п ԥ р с т тә ҭ ҭә у ф х хь хә ҳ ҳә ц цә ҵ ҵә ч ҷ ҽ ҿ ш шь шә ы ҩ џ џь ь ә",
# "uppercase_dialect": "Ҙ Ҙә Ӡʼ Ҫ Ҫә Хʼ Хʼә Цʼ Ҵʼ",
# "lowercase_dialect": "ҙ ҙә ӡʼ ҫ ҫә хʼ хʼә цʼ ҵʼ",
# "uppercase_historic": "Гу Ҕ Ҕь Ҕу Ку Ҟу Ҧ Ху",
# "lowercase_historic": "гу ҕ ҕь ҕу ку ҟу ҧ ху",
# "uppercase_lexic": "Й Ў",
# "lowercase_lexic": "й ў",




