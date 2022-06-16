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

# SC = CyrillicOrderSorter(sortorderfile)



class CharacherDescription(object):
	dangersymbols = {
		'\t': '',
		'\"': '\''
	}
	def __init__(self, unicodelibfile):
		if not os.path.exists(unicodelibfile):
			print('Unicode library file not found: %s' % unicodelibfile)
			return
		print ('Loading Unicode library: %s' % unicodelibfile)
		filedesc = open(unicodelibfile, mode = 'r')
		self.stuct = {}
		key = None
		txt = ''
		for line in filedesc:
			line = line.rstrip()

			if line and not line.startswith('@') and not line.startswith(';'):
				if line.startswith('\t'):
					pass
					# txt += line + '\n'
					# if key in self.stuct:
					# 	self.stuct[key] = txt
				else:
					key = line.split('\t')[0]
					txt = line.split('\t')[1] # + '\n'
					self.stuct[key] = txt
		filedesc.close()

	def getCharacterDescription(self, unicodechar):
		if unicodechar in self.stuct:
			r = self.stuct[unicodechar].strip()
			for k,v in self.dangersymbols.items():
				r = r.replace(k, v)
			return r #self.stuct[unicodechar].strip().replace('\t','')
		else:
			return ''


def ran_gen(size, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))

def getUniqName(cut=32):
	return 'id' + ran_gen(cut, "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

def getCharInfo(item, typestring = None):
	types = []
	unicodes = []
	for mark in marks:
		if typestring and typestring not in types:
			types.append(typestring)
		if mark in item:
			item = item.replace(mark, '')
			types.append(signtypes[mark]) # mark
	if '!' in item:
		unicodes = item.split('!')[1:]
		item = ''
		for uni in unicodes:
			item += chr(int(uni,16))
	else:
		for ch in item:
			_ch = '%04X' % ord(ch)
			unicodes.append(_ch)
	return {
		'sign': item,
		'unicodes': unicodes,
		'types': types
	}

def cascadeAltsChar(CharDesc, charsline, typestring = None, usedunicodes = None, name_eng = None):
	chars_list = [getCharInfo(sign, typestring = typestring) for sign in charsline.split(' ')]
	chars_list_wrap = []
	uniqunicodes = []
	# print ('usedunicodes input',usedunicodes)
	if usedunicodes:
		uniqunicodes.extend(usedunicodes)
	resultunicodes = []
	if not charsline: return ([],[],usedunicodes)
	for idx, item in enumerate(chars_list):
		sign = item['sign']
		unicodes = item['unicodes']
		types = item['types']
		# if typestring and types and typestring not in types:
		# 	types.append(typestring)
		alts = []
		if unicodes and unicodes[0] and unicodes[0] not in uniqunicodes:
			uniqunicodes.append(unicodes[0])
			tp = None
			if len(unicodes) == 1:
				tp = types.copy()
				if typestring and typestring not in tp:
					tp.append(typestring)
			item = {
				'id': getUniqName(),
				'sign': chr(int(unicodes[0], 16)),
				'unicode': unicodes[0],
				'display_unicode': unicodes[0],
				'types': tp,
				'description': CharDesc.getCharacterDescription(unicodes[0])
			}
			resultunicodes.append(item)
		# else:
		# 	print ('l1', name_eng, sign, unicodes)
			# break
		# for uni in unicodes:
		# 	if uni not in uniqunicodes:
		# 		uniqunicodes.append(uni)
		for nextitem in chars_list[idx + 1:]:
			_types = nextitem['types']
			if signtypes[alternatesign] in _types or signtypes[equivalentsign] in _types:# or signtypes['&'] in _types:
				_unicodes = nextitem['unicodes']
				nexttypes = nextitem['types'].copy()
				# if typestring and nexttypes and typestring not in nexttypes:
				# 	nexttypes.append(typestring)
				if signtypes[alternatesign] in nexttypes and signtypes[featuresign] in nexttypes:
					nexttypes.remove(signtypes[alternatesign])
				elif signtypes[alternatesign] in nexttypes and signtypes[featuresign] in types:
					# print ('founded replacement', name_eng, item)
					nexttypes.remove(signtypes[alternatesign])
					nexttypes.append(signtypes[replacementsign])
				alts.append({
					'id': getUniqName(),
					'sign': nextitem['sign'],
					'unicodes': _unicodes,
					'types': nexttypes, #nextitem['types'],
					'alts': [],
					'description': ', '.join(_unicodes)
				})
				if _unicodes and _unicodes[0] and _unicodes[0] not in uniqunicodes:
					uniqunicodes.append(_unicodes[0])
					tp = None
					if len(_unicodes) == 1:
						tp = nexttypes.copy()
						if typestring:
							tp.append(typestring)
					item = {
						'id': getUniqName(),
						'sign': chr(int(_unicodes[0], 16)),
						'unicode': _unicodes[0],
						'display_unicode': _unicodes[0],
						'types': tp,
						'description': CharDesc.getCharacterDescription(_unicodes[0])
					}
					resultunicodes.append(item)
					# print('l2', name_eng, sign, unicodes)
				elif _unicodes and _unicodes[0] in uniqunicodes and signtypes[alternatesign] in nextitem['types'] and signtypes[featuresign] in nextitem['types']:
					tp = None
					if len(_unicodes) == 1:
						tp = nexttypes.copy()
						if typestring:
							tp.append(typestring)
					item = {
						'id': getUniqName(),
						'sign': chr(int(_unicodes[0], 16)),
						'unicode': _unicodes[0],
						'display_unicode': '', #_unicodes[0],
						'types': tp,
						'description': CharDesc.getCharacterDescription(_unicodes[0])
					}
					resultunicodes.append(item)
					# print('l3', name_eng, sign, unicodes)
					# print (item)
				# for uni in _unicodes:
				# 	if uni not in uniqunicodes:
				# 		uniqunicodes.append(uni)
			else:
				break
		if signtypes[alternatesign] not in types and signtypes[equivalentsign] not in types:# and signtypes['&'] not in types:
			chars_list_wrap.append({
				'id': getUniqName(),
				'sign': sign,
				'unicodes': unicodes,
				'types': types,
				'alts': alts,
				'description': ', '.join(unicodes)
			})

	return (chars_list_wrap, resultunicodes, uniqunicodes)

def main(names = None): # names = ['Avar']

	workPath = os.path.dirname(__file__)

	libraryPath = 'library'  # langlib
	outputPath = 'site'
	outputLibraryPath = 'baselib'
	libraryMainFile = 'cyrillic_library.json'
	# sortorderfile = 'sortorder_cyrillic.txt'
	unicodeLibFile = 'unicode14.txt'
	print ('*'*60)
	print ('Started compiling the language library')
	print (workPath)
	basePath, _s = os.path.split(workPath)
	print ('basePath: %s' % basePath)
	libraryPath = os.path.join(basePath, libraryPath)
	print ('libraryPath: %s' % libraryPath)

	libraryMainFile = os.path.join(basePath, libraryMainFile)
	if not os.path.exists(libraryMainFile):
		print ('Main library file not found: %s' % libraryMainFile)
		return
	print ('libraryMainFile: %s' % libraryMainFile)

	unicodeLibFile = os.path.join(basePath, unicodeLibFile)

	CharDesc = CharacherDescription(unicodeLibFile)
	print('*' * 60)
	# return

	with open(libraryMainFile, "r") as read_file:
		data = json.load(read_file)

	if not names:
		names = []
		for item in data:
			names.append(item['name_eng'])

	for name in names:
		namefile = os.path.join(libraryPath, '%s.json' % name)
		if os.path.exists(namefile):
			with open(namefile, "r") as read_file:
				data = json.load(read_file)
			print('%s path:%s' % (name, namefile))

			uppercase_alphabet = data['uppercase_alphabet']
			lowercase_alphabet = data['lowercase_alphabet']

			uppercase_dialect = data['uppercase_dialect']
			lowercase_dialect = data['lowercase_dialect']
			uppercase_historic = data['uppercase_historic']
			lowercase_historic = data['lowercase_historic']
			uppercase_lexic = data['uppercase_lexic']
			lowercase_lexic = data['lowercase_lexic']

			upper_txtlist = []
			lower_txtlist = []

			(uppercase_alphabet,
			 uppercase_unicodes,
			 uppercase_usedunicodes) = cascadeAltsChar(CharDesc, uppercase_alphabet, name_eng = name)
			(lowercase_alphabet,
			 lowercase_unicodes,
			 lowercase_usedunicodes) = cascadeAltsChar(CharDesc, lowercase_alphabet, name_eng = name)

			(uppercase_dialect,
			 uppercase_dialect_unicodes,
			 uppercase_usedunicodes) = cascadeAltsChar(CharDesc, uppercase_dialect,
			                                           typestring = signtypes[dialectsign],
			                                           usedunicodes = uppercase_usedunicodes,
			                                           name_eng = name)
			(lowercase_dialect,
			 lowercase_dialect_unicodes,
			 lowercase_usedunicodes) = cascadeAltsChar(CharDesc, lowercase_dialect,
			                                           typestring = signtypes[dialectsign],
			                                           usedunicodes = lowercase_usedunicodes,
			                                           name_eng = name)

			(uppercase_historic,
			 uppercase_historic_unicodes,
			 uppercase_usedunicodes) = cascadeAltsChar(CharDesc, uppercase_historic,
			                                           typestring = signtypes[historicsign],
			                                           usedunicodes = uppercase_usedunicodes,
			                                           name_eng = name)
			(lowercase_historic,
			 lowercase_historic_unicodes,
			 lowercase_usedunicodes) = cascadeAltsChar(CharDesc, lowercase_historic,
			                                           typestring = signtypes[historicsign],
			                                           usedunicodes = lowercase_usedunicodes,
			                                           name_eng = name)

			(uppercase_lexic,
			 uppercase_lexic_unicodes,
			 uppercase_usedunicodes) = cascadeAltsChar(CharDesc, uppercase_lexic,
			                                           typestring = signtypes[lexicsign],
			                                           usedunicodes = uppercase_usedunicodes,
			                                           name_eng = name)
			(lowercase_lexic,
			 lowercase_lexic_unicodes,
			 lowercase_usedunicodes) = cascadeAltsChar(CharDesc, lowercase_lexic,
			                                           typestring = signtypes[lexicsign],
			                                           usedunicodes = lowercase_usedunicodes,
			                                           name_eng = name)


			uppercase_unicodes_list = uppercase_unicodes + uppercase_dialect_unicodes + uppercase_historic_unicodes + uppercase_lexic_unicodes#SC.getSortedCyrillicList(uppercase_unicodes_list)
			lowercase_unicodes_list = lowercase_unicodes + lowercase_dialect_unicodes + lowercase_historic_unicodes + lowercase_lexic_unicodes#SC.getSortedCyrillicList(lowercase_unicodes_list)


			outputdata = {
				'name_eng': name,

				# 'uppercase_characters_string': ' '.join([chr(int(x, 16)) for x in uppercase_unicodes_list]),
				# 'lowercase_characters_string': ' '.join([chr(int(x, 16)) for x in lowercase_unicodes_list]),
				# 'uppercase_unicodes_string': ' '.join(uppercase_unicodes_list),
				# 'lowercase_unicodes_string': ' '.join(lowercase_unicodes_list),

				'uppercase_alphabet': uppercase_alphabet,
				'lowercase_alphabet': lowercase_alphabet,

				'uppercase_dialect': uppercase_dialect,
				'lowercase_dialect': lowercase_dialect,

				'uppercase_historic': uppercase_historic,
				'lowercase_historic': lowercase_historic,

				'uppercase_lexic': uppercase_lexic,
				'lowercase_lexic': lowercase_lexic,

				'uppercase_unicodes_list': uppercase_unicodes_list,
				'lowercase_unicodes_list': lowercase_unicodes_list
			}

			outputJSONfile = os.path.join(basePath, outputPath, outputLibraryPath, '%s.json' % name)
			with open(outputJSONfile, "w") as write_file:
				json.dump(outputdata, write_file, indent = 4, ensure_ascii = False)
		else:
			print('*** Not found: %s path:%s' % (name, namefile))


if __name__ == '__main__':
	main(names = sys.argv[1:])