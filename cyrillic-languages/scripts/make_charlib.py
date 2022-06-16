# -*- coding: utf-8 -*-
"""
The script creates a library of Cyrillic characters based on the "sortorder_cyrillic.txt"
file, the database displays the unicode of the character and the description
from the 'unicode14.txt' file
"""

import importlib, json, os

import PTLangLib
importlib.reload(PTLangLib)
from PTLangLib import *

sortorderfile = 'sortorder_cyrillic.txt'
unicodelibfile = 'unicode14.txt'
outputJSONpath = 'langlib'
outputLIBFile = 'cyrillic_characters_lib.json'


SC = CyrillicOrderSorter(sortorderfile)
CD = CharacherDescription(unicodelibfile)
data = []
for idx, k in enumerate(SC.upperlist):
	alt = ''
	if '.alt' in k:
		k = k.replace('.alt','')
		alt = k#'%04X' % ord(k)
	uni = k #'%04X' % ord(k)
	inf = 'Paratype PUA code'
	if uni in CD.stuct:
		inf = CD.stuct[uni].strip().replace('\t','')
	data.append( { 'uni': uni,
	               'char': chr(int(uni, 16)),
	               'case': 'capital',
	               'alt': alt,
	               'info': inf})
	if idx < len(SC.lowerlist):
		k = SC.lowerlist[idx]
		alt = ''
		if '.alt' in k:
			k = k.replace('.alt', '')
			alt = k# '%04X' % ord(k)
		_uni = k #'%04X' % ord(k)
		inf = 'Paratype PUA code'
		if _uni in CD.stuct:
			inf = CD.stuct[_uni].strip().replace('\t', '')
		data.append({'uni': _uni,
		             'char': chr(int(_uni, 16)),
		             'case': 'small',
		             'alt': alt,
		             'info': inf})

f = os.path.join(outputJSONpath, outputLIBFile)
with open(f, "w") as write_file:
	json.dump(data, write_file, indent = 4, ensure_ascii = False)