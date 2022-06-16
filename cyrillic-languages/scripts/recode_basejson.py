# -*- coding: utf-8 -*-

import json
import os.path
import importlib

import PTLangLib
importlib.reload(PTLangLib)
from PTLangLib import *

workpath = 'langlib'
outputpath = 'output'
codeslangfile = 'cyrillic_lib.json'
sortorderfile = 'sortorder_cyrillic.txt'
unicodelibfile = 'unicode14.txt'

marks = ['*', '$', '#', '@', '(', ')', '[', ']', '+', '=', '&', '.alt']  # , '.alt'
signtypes = {
	'*' : 'notrussiansign',
	'@' : 'dialectsign',
	'#' : 'oldersign',
	"$" : 'lexicosign',
	'+' : 'alternatesign',
	'=' : 'equivalentsign',
	'&' : 'featuresign',
	# '.alt' : 'featuresignalt'
}
# replacementsign

def splitAdds(txt):
	historic = []
	lexic = []
	dialect = []
	_t = txt.split(' ')
	for item in _t:
		if '$' in item:
			item = item.replace('$', '')
			lexic.append(item)
		if '#' in item:
			item = item.replace('#', '')
			historic.append(item)
		if '@' in item:
			item = item.replace('@', '')
			dialect.append(item)
	return (dialect, historic, lexic )



with open(codeslangfile, "r") as read_file:
	data = json.load(read_file)

names = []

for item in data:
	# print(item)
	names.append(item['name_eng'])



for name in names:
	namefile = os.path.join(workpath, '%s.json' % name)
	with open(namefile, "r") as read_file:
		data = json.load(read_file)
	uppercase_alphabet = data['uppercase_alphabet']
	lowercase_alphabet = data['lowercase_alphabet']
	uppercase_alphabet_adds = data['uppercase_alphabet_adds']
	lowercase_alphabet_adds = data['lowercase_alphabet_adds']

	uppercase_alphabet = uppercase_alphabet.replace('*','')
	lowercase_alphabet = lowercase_alphabet.replace('*','')

	(uppercase_dialect, uppercase_historic, uppercase_lexic) = splitAdds(uppercase_alphabet_adds)
	(lowercase_dialect, lowercase_historic, lowercase_lexic) = splitAdds(lowercase_alphabet_adds)

	uppercase_dialect = ' '.join(uppercase_dialect)
	lowercase_dialect = ' '.join(lowercase_dialect)
	uppercase_historic = ' '.join(uppercase_historic)
	lowercase_historic = ' '.join(lowercase_historic)
	uppercase_lexic = ' '.join(uppercase_lexic)
	lowercase_lexic = ' '.join(lowercase_lexic)

	print(name)

	data2 = data
	data2['uppercase_alphabet'] = uppercase_alphabet
	data2['lowercase_alphabet'] = lowercase_alphabet
	data2.pop('uppercase_alphabet_adds')
	data2.pop('lowercase_alphabet_adds')
	data2['uppercase_dialect'] = uppercase_dialect
	data2['lowercase_dialect'] = lowercase_dialect
	data2['uppercase_historic'] = uppercase_historic
	data2['lowercase_historic'] = lowercase_historic
	data2['uppercase_lexic'] = uppercase_lexic
	data2['lowercase_lexic'] = lowercase_lexic

	print (data2)
	outputJSONfile = namefile
	with open(outputJSONfile, "w") as write_file:
		json.dump(data2, write_file, indent = 4, ensure_ascii = False)



