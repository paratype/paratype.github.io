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
digraph = ':'
alphabet = '<'

signtypes = {
	# '*' : 'notrussiansign',
	dialectsign : 'dialect',
	historicsign : 'historic', #oldersign
	lexicsign : 'extended', #lexicosign
	digraph : 'digraph',
	alternatesign : 'alternatesign',
	equivalentsign : 'equivalentsign',
	featuresign : 'localform',
	replacementsign : 'replacementsign',
	alphabet : 'alphabet'
	# '.alt' : 'featuresignalt'
}

# SC = CyrillicOrderSorter(sortorderfile)
# sortorderfile = 'sortorder_cyrillic.txt'
libraryMainFile = 'cyrillic_library.json'
libraryGlyphsList = 'glyphs_list.json'
unicodeLibFiles = ['unicode14.txt', 'PT_PUA_unicodes-descritions.txt']
# libraryPath =   # langlib
# outputPath = 'site'
# outputLibraryPath = 'baselib'

class CharacherDescription(object):
	dangersymbols = {
		'\t': '',
		'\"': '\''
	}
	def __init__(self):
		self.stuct = {}


	def loadUnicodeDescriptionsFile(self, unicodelibfile):
		if not os.path.exists(unicodelibfile):
			print('Unicode library file not found: %s' % unicodelibfile)
			return
		print ('Loading Unicode library: %s' % unicodelibfile)
		filedesc = open(unicodelibfile, mode = 'r')
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
					if key not in self.stuct:
						self.stuct[key] = txt
					else:
						print ('Unicodes overlap:')
						print ('\t%s = %s' % (key, self.stuct[key]))
						print ('\t%s = %s' % (key, txt))
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
	overrideunicode = False
	for mark in marks:
		if typestring and typestring not in types:
			types.append(typestring)
		if mark in item:
			item = item.replace(mark, '')
			types.append(signtypes[mark]) # mark
	if '!' in item:
		unicodes = item.split('!')[1:]
		item = ''
		overrideunicode = True
		for uni in unicodes:
			item += chr(int(uni,16))
	else:
		for ch in item:
			_ch = '%04X' % ord(ch)
			unicodes.append(_ch)
	return {
		'sign': item,
		'unicodes': unicodes,
		'types': types,
		'overuni': overrideunicode
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
		orrideunicode = item['overuni']
		# if typestring and types and typestring not in types:
		# 	types.append(typestring)
		alts = []
		if unicodes and unicodes[0] and unicodes[0] not in uniqunicodes and signtypes[featuresign] not in types:
			uniqunicodes.append(unicodes[0])
			tp = None
			if len(unicodes) == 1:
				tp = types.copy()
				if typestring and typestring not in tp:
					tp.append(typestring)
			item = {
				'id': getUniqName(),
				'sign': chr(int(unicodes[0], 16)),
				'unicodes': [unicodes[0]],
				'display_unicode': unicodes[0],
				'types': tp,
				'description': CharDesc.getCharacterDescription(unicodes[0])
			}
			resultunicodes.append(item)
		elif unicodes and unicodes[0] and unicodes[0] not in uniqunicodes and signtypes[featuresign] in types:
			uniqunicodes.append(unicodes[0])
			tp = None
			if len(unicodes) == 1:
				tp = types.copy()
				if typestring and typestring not in tp:
					tp.append(typestring)
			display_unicode = ''
			if orrideunicode:
				display_unicode = unicodes[0]
			item = {
				'id': getUniqName(),
				'sign': chr(int(unicodes[0], 16)),
				'unicodes': [unicodes[0]],
				'display_unicode': display_unicode,
				'types': tp,
				'description': '%s %s' % (CharDesc.getCharacterDescription(unicodes[0]), name_eng)
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
					'description': ', '.join(_unicodes),
					'alts': [],
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
						'unicodes': [_unicodes[0]],
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
						'unicodes': [_unicodes[0]],
						'display_unicode': '', #_unicodes[0],
						'types': tp,
						'description': CharDesc.getCharacterDescription(_unicodes[0])
					}
					resultunicodes.append(item)
				elif _unicodes and _unicodes[0] in uniqunicodes and signtypes[replacementsign] in nexttypes:
					tp = None
					if len(_unicodes) == 1:
						tp = nexttypes.copy()
						if typestring:
							tp.append(typestring)
					item = {
						'id': getUniqName(),
						'sign': chr(int(_unicodes[0], 16)),
						'unicodes': [_unicodes[0]],
						'display_unicode': _unicodes[0],
						'types': tp,
						'description': CharDesc.getCharacterDescription(_unicodes[0])
					}
					resultunicodes.append(item)
			else:
				break
		if signtypes[alternatesign] not in types and signtypes[equivalentsign] not in types:# and signtypes['&'] not in types:
			description = ', '.join(unicodes)
			if signtypes[featuresign] in types:
				if alts and alts[0]['unicodes'] == unicodes:
					description = 'Localized form of %s' % ', '.join(alts[0]['unicodes'])
				elif alts and alts[0]['unicodes'] != unicodes:
					adddesrc = ''
					if unicodes:
						adddesrc = '(%s)' % ', '.join(unicodes)
					description = 'Localized form of %s %s' % (', '.join(alts[0]['unicodes']), adddesrc)
			chars_list_wrap.append({
				'id': getUniqName(),
				'sign': sign,
				'unicodes': unicodes,
				'types': types,
				'description': description,
				'alts': alts,
			})

	return (chars_list_wrap, resultunicodes, uniqunicodes)

def compileLagnuages(workPath, names = None): # names = ['Avar']

	# workPath = os.path.dirname(__file__)

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

	libraryGlyphsListPath = os.path.join(basePath, libraryGlyphsList)
	if not os.path.exists(libraryGlyphsListPath):
		print('Main library GlyphsList categories file not found: %s' % libraryGlyphsListPath)
		return
	print('libraryGlyphsList: %s' % libraryGlyphsListPath)


	CharDesc = CharacherDescription()
	for ulf in unicodeLibFiles:
		upath = os.path.join(basePath, ulf)
		CharDesc.loadUnicodeDescriptionsFile(upath)
	print('*' * 60)

	with open(libraryMainFilePath, "r") as read_file:
		data = json.load(read_file)
	with open(libraryGlyphsListPath, "r") as read_file:
		glcategories = json.load(read_file)
	categories = {}
	for gl in glcategories:
		categories[gl['type']] = dict (show_unicodes = gl['show_unicodes'], title = gl['title'])
	# print (categories)

	if not names:
		names = []
		for item in data:
			if item['enable']:
				names.append(item['name_eng'])

	for name in names:
		namefile = os.path.join(libraryPath, '%s.json' % name)
		outputJSONfile = os.path.join(basePath, 'site', 'baselib', 'newlib', '%s.json' % name)

		if os.path.exists(namefile):
			with open(namefile, "r") as read_file:
				data = json.load(read_file)
			print('%s path:%s' % (name, namefile))

			uppercase_usedunicodes = None
			lowercase_usedunicodes = None
			uppercase_list_unicodes = None
			lowercase_list_unicodes = None

			glyphslists = data['glyphs_list']
			outputdata = {
				'name_eng': name,
				'glyphs_list': []
			}

			for glyphlist in glyphslists:
				typelist = glyphlist['type']
				uppercaselist = glyphlist['uppercase']
				lowercaselist = glyphlist['lowercase']

				(uppercase_list,
				 uppercase_list_unicodes,
				 uppercase_usedunicodes) = cascadeAltsChar(CharDesc, uppercaselist,
				                                           typestring = typelist,
				                                           usedunicodes = uppercase_usedunicodes,
				                                           name_eng = name)
				(lowercase_list,
				 lowercase_list_unicodes,
				 lowercase_usedunicodes) = cascadeAltsChar(CharDesc, lowercaselist,
				                                           typestring = typelist,
				                                           usedunicodes = lowercase_usedunicodes,
				                                           name_eng = name)
				outputdata['glyphs_list'].append({
					'type': typelist,
					'title': categories[typelist]['title'],
					'show_unicodes': categories[typelist]['show_unicodes'],
					'uppercase': uppercase_list,
					'lowercase': lowercase_list
				})

			outputdata['glyphs_list'].append({
				'type': 'charset',
				'title': categories['charset']['title'],
				'show_unicodes': categories['charset']['show_unicodes'],
				'uppercase': uppercase_list_unicodes,
				'lowercase': lowercase_list_unicodes
			})
			with open(outputJSONfile, "w") as write_file:
				json.dump(outputdata, write_file, indent = 4, ensure_ascii = False)
		else:
			print('*** Not found: %s path:%s' % (name, namefile))

			# 	# 'uppercase_characters_string': ' '.join([chr(int(x, 16)) for x in uppercase_unicodes_list]),
			# 	# 'lowercase_characters_string': ' '.join([chr(int(x, 16)) for x in lowercase_unicodes_list]),
			# 	# 'uppercase_unicodes_string': ' '.join(uppercase_unicodes_list),
			# 	# 'lowercase_unicodes_string': ' '.join(lowercase_unicodes_list),
			#
			# 	'uppercase_alphabet': uppercase_alphabet,
			# 	'lowercase_alphabet': lowercase_alphabet,
			#
			# 	'uppercase_dialect': uppercase_dialect,
			# 	'lowercase_dialect': lowercase_dialect,
			#
			# 	'uppercase_historic': uppercase_historic,
			# 	'lowercase_historic': lowercase_historic,
			#
			# 	'uppercase_lexic': uppercase_lexic,
			# 	'lowercase_lexic': lowercase_lexic,
			#
			# 	'uppercase_unicodes_list': uppercase_unicodes_list,
			# 	'lowercase_unicodes_list': lowercase_unicodes_list
			# }

			# uppercase_alphabet = data['uppercase_alphabet']
			# lowercase_alphabet = data['lowercase_alphabet']
			#
			# uppercase_dialect = data['uppercase_dialect']
			# lowercase_dialect = data['lowercase_dialect']
			# uppercase_historic = data['uppercase_historic']
			# lowercase_historic = data['lowercase_historic']
			# uppercase_lexic = data['uppercase_lexic']
			# lowercase_lexic = data['lowercase_lexic']
			#
			# upper_txtlist = []
			# lower_txtlist = []
			#
			# (uppercase_alphabet,
			#  uppercase_unicodes,
			#  uppercase_usedunicodes) = cascadeAltsChar(CharDesc, uppercase_alphabet, name_eng = name)
			# (lowercase_alphabet,
			#  lowercase_unicodes,
			#  lowercase_usedunicodes) = cascadeAltsChar(CharDesc, lowercase_alphabet, name_eng = name)
			#
			# (uppercase_dialect,
			#  uppercase_dialect_unicodes,
			#  uppercase_usedunicodes) = cascadeAltsChar(CharDesc, uppercase_dialect,
			#                                            typestring = signtypes[dialectsign],
			#                                            usedunicodes = uppercase_usedunicodes,
			#                                            name_eng = name)
			# (lowercase_dialect,
			#  lowercase_dialect_unicodes,
			#  lowercase_usedunicodes) = cascadeAltsChar(CharDesc, lowercase_dialect,
			#                                            typestring = signtypes[dialectsign],
			#                                            usedunicodes = lowercase_usedunicodes,
			#                                            name_eng = name)
			#
			# (uppercase_historic,
			#  uppercase_historic_unicodes,
			#  uppercase_usedunicodes) = cascadeAltsChar(CharDesc, uppercase_historic,
			#                                            typestring = signtypes[historicsign],
			#                                            usedunicodes = uppercase_usedunicodes,
			#                                            name_eng = name)
			# (lowercase_historic,
			#  lowercase_historic_unicodes,
			#  lowercase_usedunicodes) = cascadeAltsChar(CharDesc, lowercase_historic,
			#                                            typestring = signtypes[historicsign],
			#                                            usedunicodes = lowercase_usedunicodes,
			#                                            name_eng = name)
			#
			# (uppercase_lexic,
			#  uppercase_lexic_unicodes,
			#  uppercase_usedunicodes) = cascadeAltsChar(CharDesc, uppercase_lexic,
			#                                            typestring = signtypes[lexicsign],
			#                                            usedunicodes = uppercase_usedunicodes,
			#                                            name_eng = name)
			# (lowercase_lexic,
			#  lowercase_lexic_unicodes,
			#  lowercase_usedunicodes) = cascadeAltsChar(CharDesc, lowercase_lexic,
			#                                            typestring = signtypes[lexicsign],
			#                                            usedunicodes = lowercase_usedunicodes,
			#                                            name_eng = name)
			#
			#
			# uppercase_unicodes_list = uppercase_unicodes + uppercase_dialect_unicodes + uppercase_historic_unicodes + uppercase_lexic_unicodes#SC.getSortedCyrillicList(uppercase_unicodes_list)
			# lowercase_unicodes_list = lowercase_unicodes + lowercase_dialect_unicodes + lowercase_historic_unicodes + lowercase_lexic_unicodes#SC.getSortedCyrillicList(lowercase_unicodes_list)
			#
			#
			# outputdata = {
			# 	'name_eng': name,
			#
			# 	# 'uppercase_characters_string': ' '.join([chr(int(x, 16)) for x in uppercase_unicodes_list]),
			# 	# 'lowercase_characters_string': ' '.join([chr(int(x, 16)) for x in lowercase_unicodes_list]),
			# 	# 'uppercase_unicodes_string': ' '.join(uppercase_unicodes_list),
			# 	# 'lowercase_unicodes_string': ' '.join(lowercase_unicodes_list),
			#
			# 	'uppercase_alphabet': uppercase_alphabet,
			# 	'lowercase_alphabet': lowercase_alphabet,
			#
			# 	'uppercase_dialect': uppercase_dialect,
			# 	'lowercase_dialect': lowercase_dialect,
			#
			# 	'uppercase_historic': uppercase_historic,
			# 	'lowercase_historic': lowercase_historic,
			#
			# 	'uppercase_lexic': uppercase_lexic,
			# 	'lowercase_lexic': lowercase_lexic,
			#
			# 	'uppercase_unicodes_list': uppercase_unicodes_list,
			# 	'lowercase_unicodes_list': lowercase_unicodes_list
			# }

		# 	with open(outputJSONfile, "w") as write_file:
		# 		json.dump(outputdata, write_file, indent = 4, ensure_ascii = False)
		# else:
		# 	print('*** Not found: %s path:%s' % (name, namefile))

def filterCharacters(name, local, charlist, unicodedlist, puazonelist, nonunicodedlist):
	# unicodedlist = {}
	# nonunicodedlist = {}
	# puazonelist = {}

	for item in charlist:
		sign = item['sign']
		unicodes = item['unicodes']
		display_unicode = item['display_unicode']

		types = item['types']
		if not types:
			types = []
		description = item['description']

		if len(unicodes) > 1:
			print('*** TOO MUCH UNICODES')
			print(unicodes)
		elif len(unicodes) < 1:
			print('*** NO UNICODES')
			print(unicodes[0], sign)
		elif not unicodes:
			print('*** NULL UNICODE')
			print(unicodes[0], sign)

		if not display_unicode:
			# TODO надо попробовать name заменить на local, чтобы избавится от дубля Македонского и Сербского
			if '%s.%s' % (unicodes[0], local) not in nonunicodedlist:
				nonunicodedlist['%s.%s' % (unicodes[0], local)] = dict(
					id = getUniqName(),
					sign = sign,
					unicodes = [unicodes[0]],
					local = local,
					display_unicode = display_unicode,
					description = description,
					languages = [dict(name = name, types = types)]
				)
			else:
				print ('*** WRONG LOCALES')
				print (name, '%s.%s' % (unicodes[0],local))
				# nonunicodedlist[unicodes[0]]['languages'].append(dict(name = name, types = types))
		elif display_unicode.startswith('F'):
			if unicodes[0] not in puazonelist:
				puazonelist[unicodes[0]] = dict(
					id = getUniqName(),
					sign = sign,
					unicodes = [unicodes[0]],
					local = local,
					display_unicode = display_unicode,
					description = description,
					languages = [dict(name = name, types = types)]
				)
			else:
				puazonelist[unicodes[0]]['languages'].append(dict(name = name, types = types))
		else:
			if unicodes[0] not in unicodedlist:
				unicodedlist[unicodes[0]] = dict(
					id = getUniqName(),
					sign = sign,
					unicodes = [unicodes[0]],
					local = local,
					display_unicode = display_unicode,
					description = description,
					languages = [dict(name = name, types = types)]
				)
			else:
				unicodedlist[unicodes[0]]['languages'].append(dict(name = name, types = types))
	return unicodedlist, puazonelist, nonunicodedlist


def makeMainCharactersSet(workPath):
	print('*' * 60)
	print('making MainCharactersSet')
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

	names = []
	for item in data:
		if item['enable']:
			names.append(item['name_eng'])

	unicodedlist_UC = {}
	nonunicodedlist_UC = {}
	puazonelist_UC = {}

	unicodedlist_LC = {}
	nonunicodedlist_LC = {}
	puazonelist_LC = {}

	for name in names:
		mainfile = os.path.join(libraryPath, '%s.json' % name)
		inputJSONfile = os.path.join(basePath, 'site', 'baselib', '%s.json' % name)

		if os.path.exists(inputJSONfile):
			with open(inputJSONfile, "r") as read_file:
				data = json.load(read_file)
			print('%s path:%s' % (name, inputJSONfile))

			local = 'ru'
			if os.path.exists(mainfile):
				with open(mainfile, "r") as read_file:
					maindata = json.load(read_file)
				print('%s path:%s' % (name, mainfile))
				local = maindata['local']
			print('LOCAL:', local)

			uppercase_unicodes_list = data['uppercase_unicodes_list']
			lowercase_unicodes_list = data['lowercase_unicodes_list']

			unicodedlist_UC, puazonelist_UC, nonunicodedlist_UC = filterCharacters(name, local, uppercase_unicodes_list, unicodedlist_UC, puazonelist_UC, nonunicodedlist_UC)
			unicodedlist_LC, puazonelist_LC, nonunicodedlist_LC = filterCharacters(name, local, lowercase_unicodes_list, unicodedlist_LC, puazonelist_LC, nonunicodedlist_LC)

	UC_unicoded_list = []
	for k,v in sorted(unicodedlist_UC.items()):
		UC_unicoded_list.append(v)
	UC_pua_list = []
	for k,v in sorted(puazonelist_UC.items()):
		UC_pua_list.append(v)
	UC_nonunicoded_list = []
	for k,v in sorted(nonunicodedlist_UC.items()):
		UC_nonunicoded_list.append(v)

	LC_unicoded_list = []
	for k,v in sorted(unicodedlist_LC.items()):
		LC_unicoded_list.append(v)
	LC_pua_list = []
	for k,v in sorted(puazonelist_LC.items()):
		LC_pua_list.append(v)
	LC_nonunicoded_list = []
	for k,v in sorted(nonunicodedlist_LC.items()):
		LC_nonunicoded_list.append(v)

	dataset = dict(
		uppercase_unicodes_list = UC_unicoded_list,
		lowercase_unicodes_list = LC_unicoded_list,

		uppercase_puazone_list = UC_pua_list,
		lowercase_puazone_list = LC_pua_list,

		uppercase_nonunicode_list = UC_nonunicoded_list,
		lowercase_nonunicode_list = LC_nonunicoded_list,
	)
	outputJSONfile = os.path.join(basePath, 'site', 'cyrillic_characters_lib.json')
	with open(outputJSONfile, "w") as write_file:
		json.dump(dataset, write_file, indent = 4, ensure_ascii = False)



def main(names = None):
	pathname = os.path.dirname(sys.argv[0])
	workPath = os.path.abspath(pathname)
	compileLagnuages(workPath, names)
	# makeMainCharactersSet(workPath)


if __name__ == '__main__':
	main(names = sys.argv[1:])