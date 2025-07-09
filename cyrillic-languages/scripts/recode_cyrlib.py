# -*- coding: utf-8 -*-
import sys
import json
import os.path
import random
import string



marks = ['*', '$', '#', '@', '(', ')', '[', ']', '+', '=', '&', '.alt']  # , '.alt'

dialectsign = '@'
historicsign = '#'
lexicsign = '$'
alternatesign = '+'
equivalentsign = '='
featuresign = '&'
replacementsign = '*'

signtypes = {
	# '*' : 'notrussiansign',
	dialectsign : 'dialectsign',
	historicsign : 'historicsign', #oldersign
	lexicsign : 'lexicsign', #lexicosign
	alternatesign : 'alternatesign',
	equivalentsign : 'equivalentsign',
	featuresign : 'featuresign',
	replacementsign : 'replacementsign'
	# '.alt' : 'featuresignalt'
}

libraryMainFile = 'cyrillic_library.json'
unicodeLibFiles = ['unicode14.txt', 'PT_PUA_unicodes-descritions.txt']


def compileLagnuages(workPath, names = None): # names = ['Avar']
	print('*' * 60)
	print('Started compiling the language library')
	print(workPath)
	basePath, _s = os.path.split(workPath)
	print('basePath: %s' % basePath)
	libraryPath = os.path.join(basePath, 'library')
	print('libraryPath: %s' % libraryPath)

	libraryMainFilePath = os.path.join(basePath, libraryMainFile)
	if not os.path.exists(libraryMainFilePath):
		print('Main library file not found: %s' % libraryMainFilePath)
		return
	print('libraryMainFile: %s' % libraryMainFilePath)

	with open(libraryMainFilePath, "r") as read_file:
		data = json.load(read_file)

	if not names:
		names = []
		for item in data:
			# if item['enable']:
			names.append(item['name_eng'])

	for name in names:
		namefile = os.path.join(libraryPath, '%s.json' % name)

		if os.path.exists(namefile):
			with open(namefile, "r") as read_file:
				data = json.load(read_file)
			print('%s path:%s' % (name, namefile))

			_data = {}
			_data['name_eng'] = data['name_eng']
			_data['name_rus'] = data['name_rus']
			_data['local'] = data['local']
			_data['language_group_eng'] = data['language_group_eng']
			_data['language_group_rus'] = data['language_group_rus']
			_data['alt_names_eng'] = data['alt_names_eng']
			_data['description_eng'] = data['description_eng']
			_data['description_rus'] = data['description_rus']



			_data['glyphs_list'] = []
			_data['glyphs_list'].append({
				"type": "alphabet",
				"uppercase": data['uppercase_alphabet'],
				"lowercase": data['lowercase_alphabet']
			})

			if data['uppercase_dialect'] and data['lowercase_dialect']:
				_data['glyphs_list'].append({
					"type": "dialect",
					"uppercase": data['uppercase_dialect'],
					"lowercase": data['lowercase_dialect']
				})
			if data['uppercase_historic'] and data['lowercase_historic']:
				_data['glyphs_list'].append({
					"type": "historic",
					"uppercase": data['uppercase_historic'],
					"lowercase": data['lowercase_historic']
				})
			if data['uppercase_lexic'] and data['lowercase_lexic']:
				_data['glyphs_list'].append({
					"type": "extended",
					"uppercase": data['uppercase_lexic'],
					"lowercase": data['lowercase_lexic']
				})

			outputJSONfile = os.path.join(libraryPath, 'newlib', '%s.json' % name)
			with open(outputJSONfile, "w") as write_file:
				json.dump(_data, write_file, indent = 4, ensure_ascii = False)
		else:
			print('*** Not found: %s path:%s' % (name, namefile))


def main(names = None):
	pathname = os.path.dirname(sys.argv[0])
	workPath = os.path.abspath(pathname)
	compileLagnuages(workPath, names)
	# makeMainCharactersSet(workPath)


if __name__ == '__main__':
	main(names = sys.argv[1:])