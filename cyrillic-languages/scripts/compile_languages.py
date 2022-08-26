# -*- coding: utf-8 -*-
import sys
import json
import os.path
import random
import string, re



marks = ['*', '$', '#', '@', '(', ')', '[', ']', '+', '=', '&', '.alt', '.ita', '.str']

dialectsign = '@'
historicsign = '#'
lexicsign = '$'
alternatesign = '+'
equivalentsign = '='
featuresign = '&'
replacementsign = '*'
digraph = ':'
alphabet = '<'
italiconly = '.ita'
straightonly = '.str'

signtypes = {
	# '*' : 'notrussiansign',
	dialectsign : 'dialect',
	historicsign : 'historic',
	lexicsign : 'extended',
	digraph : 'digraph',
	alternatesign : 'alternatesign',
	equivalentsign : 'equivalentsign',
	featuresign : 'localform',
	replacementsign : 'replacementsign',
	alphabet : 'alphabet',
	italiconly : 'italic',
	straightonly : 'straight'
	# '.alt' : 'featuresignalt'
}

# SC = CyrillicOrderSorter(sortorderfile)
# sortorderfile = 'sortorder_cyrillic.txt'
libraryMainFile = 'cyrillic_library.json'
libraryGlyphsList = 'glyphs_list_categories.json'
sortOrderFile = 'sortorder_cyrillic.txt'
unicodeLibFiles = ['unicode14.txt', 'PT_PUA_unicodes-descritions.txt']

DEVELOPMENT = True

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
			r = r.title()
			return r #self.stuct[unicodechar].strip().replace('\t','')
		else:
			return ''


class PanCyrillicOrderSorter(object):
	def __init__(self, sortorderfile):
		self.missigChars = {}
		print ('Initializing sorting keys..')
		print ('from file: %s' % sortorderfile)
		f = open(sortorderfile, mode = 'r')
		locales = ['', '.ru', '.ba', '.bg', '.cv', '.sr']
		self.upperlist = []
		self.lowerlist = []
		for idx, line in enumerate(f):
			line = line.strip()
			line = re.sub("\s\s+" , " ", line)
			if line and not line.startswith('#'):
				rawline = line.split('/')
				rawupper, rawlower = None, None
				if len(rawline) == 2:
					rawupper = rawline[0]
					rawlower = rawline[1]
				elif len(rawline) == 1:
					rawupper = rawline[0]
				else:
					print ('ERROR', sortorderfile, idx)
				if rawupper:
					# sign = rawupper.split('=')[0]
					uni = rawupper.split('=')[1]
					# sign = chr(int(uni,16))
					for local in locales:
						self.upperlist.append('%s%s' % (uni, local))
				if rawlower:
					# sign = rawlower.split('=')[0]
					uni = rawlower.split('=')[1]
					# sign = chr(int(uni, 16))
					for local in locales:
						self.lowerlist.append('%s%s' % (uni, local))
		self.sortkey = self.upperlist + self.lowerlist
		f.close()

	def getSortedGlyphsList(self, characherslist):
		result = []
		for ch in self.sortkey:
			if ch in characherslist and ch not in result:
				result.append(characherslist[ch])

		for ch in characherslist:
			if ch not in self.sortkey:
				print ('*** Unicode not in SortOrder, added to the end of the list ', ch)
				result.append(characherslist[ch])

		return result


def getUniqName(cut=32):
	def ran_gen (size, chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for x in range(size))
	return 'id%s' % ran_gen(cut, "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

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


def checkTypeSign(typesign, name_eng):
	if typesign:
		if len(typesign)>1:
			while 'alphabet' in typesign:
				typesign.remove('alphabet')
		return typesign
	else:
		print ('ERROR', name_eng, typesign)
		return None


def cascadeAltsChar(CharDesc, charsline, typestring = None, usedunicodes = None, wrapedunicodes = None, name_eng = None, localdef = 'ru', local = None, extendedglyph = None, casesign = None):
	chars_list = [getCharInfo(sign, typestring = typestring) for sign in charsline.split(' ')]
	chars_list_wrap = []
	uniqunicodes = []
	if not local:
		local = localdef
	if usedunicodes:
		uniqunicodes.extend(usedunicodes)
	resultunicodes = []
	if wrapedunicodes:
		resultunicodes.extend(wrapedunicodes)
	_extendedglyph = []
	if extendedglyph:
		_extendedglyph.extend(extendedglyph)
	if not charsline: return ([],[],usedunicodes)
	_chars_list = chars_list.copy()
	for idx, item in enumerate(chars_list):
		sign = item['sign']
		unicodes = item['unicodes']
		# if len(unicodes) > 1:
		# 	print('& & & & XXXGraph', sign, unicodes, name_eng, typestring)
		types = item['types']
		orrideunicode = item['overuni']
		# if typestring and types and typestring not in types:
		# 	types.append(typestring)
		alts = []
		if unicodes and unicodes[0] and unicodes[0] not in uniqunicodes and signtypes[featuresign] not in types:
			""" знак с уникальным юникодом и не локальная форма """
			uniqunicodes.append(unicodes[0])
			tp = None
			if len(unicodes) == 1:
				tp = types.copy()
				if typestring and typestring not in tp:
					tp.append(typestring)
			item = {
				'sign': chr(int(unicodes[0], 16)),
				'unicodes': [unicodes[0]],
				'local': localdef,
				'display_unicode': unicodes[0],
				'types': tp,
				'description': CharDesc.getCharacterDescription(unicodes[0]),
				# 'id': getUniqName(8)
			}
			resultunicodes.append(item)
		elif unicodes and unicodes[0] and unicodes[0] not in uniqunicodes and signtypes[featuresign] in types:
			""" знак с уникальным юникодом и локальная форма """
			uniqunicodes.append(unicodes[0])
			tp = None
			# print('+++')
			if len(unicodes) == 1:
				tp = types.copy()
				if typestring and typestring not in tp:
					tp.append(typestring)
			tp = checkTypeSign(tp, name_eng)
			display_unicode = ''
			if orrideunicode:
				display_unicode = unicodes[0]
			# tt = ''
			# if display_unicode:
			# 	tt = '%s ' % display_unicode
			item = {
				'sign': chr(int(unicodes[0], 16)),
				'unicodes': [unicodes[0]],
				'local': local,
				'display_unicode': display_unicode,
				'types': tp,
				'description': CharDesc.getCharacterDescription(unicodes[0]) #'%sLocalized form of %s' % (tt, unicodes[0]) #
				# 'id': getUniqName(8)
			}
			resultunicodes.append(item)

		for nextitem in chars_list[idx + 1:]:
			""" проверяем следующий по порядку знак """
			_types = nextitem['types']
			if signtypes[alternatesign] in _types or signtypes[equivalentsign] in _types:
				""" следующий знак - альтернатива или эквивалент """
				_unicodes = nextitem['unicodes']
				nexttypes = nextitem['types'].copy()
				if signtypes[alternatesign] in nexttypes and signtypes[featuresign] in nexttypes:
					nexttypes.remove(signtypes[alternatesign])
				elif signtypes[alternatesign] in nexttypes and signtypes[featuresign] in types:
					nexttypes.remove(signtypes[alternatesign])
					nexttypes.append(signtypes[replacementsign])
				nexttypes = checkTypeSign(nexttypes, name_eng)
				alts.append({
					'sign': nextitem['sign'],
					'unicodes': _unicodes,
					'local': localdef,
					'types': nexttypes, #nextitem['types'],
					'description': ', '.join(_unicodes),
					# 'id': getUniqName(8),
					'alts': [],

				})
				if _unicodes and _unicodes[0] and _unicodes[0] not in uniqunicodes:
					""" у знака уникальный юникод """
					uniqunicodes.append(_unicodes[0])
					tp = None
					if len(_unicodes) == 1:
						tp = nexttypes.copy()
						if typestring and typestring not in tp:
							tp.append(typestring)
					tp = checkTypeSign(tp, name_eng)
					item = {
						'sign': chr(int(_unicodes[0], 16)),
						'unicodes': [_unicodes[0]],
						'local': localdef,
						'display_unicode': _unicodes[0],
						'types': tp,
						'description': CharDesc.getCharacterDescription(_unicodes[0]),
						# 'id': getUniqName(8)
					}
					resultunicodes.append(item)
				elif _unicodes and _unicodes[0] in uniqunicodes and signtypes[alternatesign] in nextitem['types'] and signtypes[featuresign] in nextitem['types']:
					""" юникод знака уже встречался в списке, 
						но ну него тип альтернативы и локальной формы - &a +a 
					"""
					# print ('@@')
					tp = None
					if len(_unicodes) == 1:
						tp = nexttypes.copy()
						if typestring and typestring not in tp:
							tp.append(typestring)
					tp = checkTypeSign(tp, name_eng)
					item = {
						'sign': chr(int(_unicodes[0], 16)),
						'unicodes': [_unicodes[0]],
						'local': local,
						'display_unicode': '', #_unicodes[0],
						'types': tp,
						'description': CharDesc.getCharacterDescription(_unicodes[0]),
						# 'id': getUniqName(8)
					}
					resultunicodes.append(item)
				elif _unicodes and _unicodes[0] in uniqunicodes and signtypes[replacementsign] in nexttypes:
					""" юникод знака уже встречался в списке, 
						но ну него тип replacement и локальной формы - &a *a 
					"""
					# print ('&&')
					tp = None
					if len(_unicodes) == 1:
						tp = nexttypes.copy()
						if typestring and typestring not in tp:
							tp.append(typestring)
					tp = checkTypeSign(tp, name_eng)
					item = {
						'sign': chr(int(_unicodes[0], 16)),
						'unicodes': [_unicodes[0]],
						'local': localdef,
						'display_unicode': _unicodes[0],
						'types': tp,
						'description': CharDesc.getCharacterDescription(_unicodes[0]),
						# 'id': getUniqName(8)
					}
					resultunicodes.append(item)
			else:
				break
		if signtypes[alternatesign] not in types and signtypes[equivalentsign] not in types:
			description = ', '.join(unicodes)
			_local = localdef
			if signtypes[featuresign] in types:
				_local = local
				if alts and alts[0]['unicodes'] == unicodes:
					description = 'Localized form of %s' % ', '.join(alts[0]['unicodes'])
					# print ('_+_', resultunicodes[-2], description)
				elif alts and alts[0]['unicodes'] != unicodes:
					adddesrc = ''
					if unicodes:
						adddesrc = '%s ' % ', '.join(unicodes)
					description = '%sLocalized form of %s' % (adddesrc, ', '.join(alts[0]['unicodes']))
					# print('_=_', resultunicodes[-2], description)
			types = checkTypeSign(types, name_eng)
			chars_list_wrap.append({
				'sign': sign,
				'unicodes': unicodes,
				'local': _local,
				'types': types,
				'description': description,
				# 'id': getUniqName(8),
				'alts': alts,
			})
	for idx, item in enumerate(_chars_list):
		sign = item['sign']
		unicodes = item['unicodes']
		if len(unicodes) > 1:
			for uni in unicodes[1:]:
				if uni not in uniqunicodes:
					if (uni, casesign, 'alphabet') not in _extendedglyph and (uni, casesign, typestring) not in _extendedglyph:
						_extendedglyph.append((uni, casesign, typestring))

	return (chars_list_wrap, resultunicodes, uniqunicodes, _extendedglyph)

def compileLagnuages(workPath, names = None): # names = ['Avar']
	print('*' * 60)
	print('Started compiling the language library')
	# print(workPath)
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

	if not names:
		names = []
		for item in data:
			if item['enable']:
				names.append(item['name_eng'])

	for name in names:
		namefile = os.path.join(libraryPath, '%s.json' % name)
		outputJSONfile = os.path.join(basePath, 'site', 'baselib', '%s.json' % name)

		if os.path.exists(namefile):
			with open(namefile, "r") as read_file:
				data = json.load(read_file)
			# print('%s path:%s' % (name, namefile))
			print('%s' % name)
			usedunicodes = None
			uppercase_usedunicodes = None
			lowercase_usedunicodes = None
			uppercase_list_unicodes = None
			lowercase_list_unicodes = None
			extendedglyphs = None

			glyphslists = data['glyphs_list']
			local = data['local']
			outputdata = {
				'name_eng': name,
				'glyphs_list': []
			}
			makeCharSet = True
			# if 'charset' not in data:
			# 	makeCharSet = False

			for glyphlist in glyphslists:
				typelist = glyphlist['type']
				uppercaselist = glyphlist['uppercase']
				lowercaselist = glyphlist['lowercase']

				(lowercase_list,
				 lowercase_list_unicodes,
				 usedunicodes, extendedglyphs) = cascadeAltsChar(CharDesc, lowercaselist,
				                                           typestring = typelist,
				                                           usedunicodes = usedunicodes,
				                                           wrapedunicodes = lowercase_list_unicodes,
				                                           name_eng = name, local = local, extendedglyph = extendedglyphs, casesign = 'lower')

				(uppercase_list,
				 uppercase_list_unicodes,
				 usedunicodes, extendedglyphs) = cascadeAltsChar(CharDesc, uppercaselist,
				                                           typestring = typelist,
				                                           usedunicodes = usedunicodes,
                                                           wrapedunicodes = uppercase_list_unicodes,
				                                           name_eng = name, local = local, extendedglyph = extendedglyphs, casesign = 'upper')

				outputdata['glyphs_list'].append({
					'type': typelist,
					'title': categories[typelist]['title'],
					'show_unicodes': categories[typelist]['show_unicodes'],
					'uppercase': uppercase_list,
					'lowercase': lowercase_list
				})
			if extendedglyphs:
				for exglyph in extendedglyphs:
					(uni, casesign, typestring) = exglyph
					print ('*** Extended glyph:', name, chr(int(uni, 16)), uni, casesign, typestring )
					extendeditem = {
						'sign': chr(int(uni, 16)),
						'unicodes': [uni],
						'local': local,
						'display_unicode': uni,
						'types': [typestring],
						'description': CharDesc.getCharacterDescription(uni),
						# 'id': getUniqName(8)
					}
					if casesign == 'lower':
						lowercase_list_unicodes.append( extendeditem )
					elif casesign == 'upper':
						uppercase_list_unicodes.append( extendeditem )
			if makeCharSet:
				outputdata['glyphs_list'].append({
					'type': 'charset',
					'title': categories['charset']['title'],
					'show_unicodes': categories['charset']['show_unicodes'],
					'uppercase': uppercase_list_unicodes,
					'lowercase': lowercase_list_unicodes
				})
			indent = None
			if DEVELOPMENT:
				indent = 4
			with open(outputJSONfile, "w") as write_file:
				json.dump(outputdata, write_file, indent = indent, ensure_ascii = False) #indent = 4,
		else:
			print('*** Not found: %s path:%s' % (name, namefile))


def filterCharacters(name, local, charlist, unicodedlist, puazonelist, nonunicodedlist):
	for item in charlist:
		sign = item['sign']
		unicodes = item['unicodes']
		display_unicode = item['display_unicode']
		_local = item['local']

		types = item['types']
		if not types:
			types = []
		description = item['description']

		hide = ''
		if 'italic' in types:
			# print ('ITA:', name, sign, _local, unicodes)
			hide = 'straight'
		elif 'straight' in types:
			# print('STR:',name, sign, _local, unicodes)
			hide = 'italic'
		else:
			hide = ''
			# print ('*')

		if len(unicodes) > 1:
			print('*** TOO MUCH UNICODES')
			print(unicodes)
		elif len(unicodes) < 1:
			print('*** NO UNICODES')
			print(unicodes, sign)
		elif not unicodes:
			print('*** NULL UNICODE')
			print(unicodes, sign)

		if not display_unicode:
			if '%s.%s' % (unicodes[0], _local) not in nonunicodedlist:
				nonunicodedlist['%s.%s' % (unicodes[0], _local)] = dict(
					sign = sign,
					unicodes = [unicodes[0]],
					local = _local,
					display_unicode = display_unicode,
					description = description,
					hide = hide,
					languages = [dict(name = name, types = types)],
					id = getUniqName(8)
				)
			else:
				nonunicodedlist['%s.%s' % (unicodes[0], _local)]['languages'].append(dict(name = name, types = types))

		elif display_unicode.startswith('F'):
			if unicodes[0] not in puazonelist:
				puazonelist[unicodes[0]] = dict(
					sign = sign,
					unicodes = [unicodes[0]],
					local = _local,
					display_unicode = display_unicode,
					description = description,
					hide = hide,
					languages = [dict(name = name, types = types)],
					id = getUniqName(8)
				)
			else:
				puazonelist[unicodes[0]]['languages'].append(dict(name = name, types = types))
		else:
			if unicodes[0] not in unicodedlist:
				unicodedlist[unicodes[0]] = dict(
					sign = sign,
					unicodes = [unicodes[0]],
					local = _local,
					display_unicode = display_unicode,
					description = description,
					hide = hide,
					languages = [dict(name = name, types = types)],
					id = getUniqName(8)
				)
			else:
				unicodedlist[unicodes[0]]['languages'].append(dict(name = name, types = types))

	return unicodedlist, puazonelist, nonunicodedlist

def sortGlyphsList(glyphslist, names, sortOrder = None):
	resultList = []

	if not sortOrder:
		sortedGlyphsList = sorted(glyphslist.items())
		for k, v in sortedGlyphsList:
			if len(v['languages']) == len(names):
				v['languages'].append(dict(name = 'All', types = ['alphabet']))
			resultList.append(v)
	else:
		sortedGlyphsList = sortOrder.getSortedGlyphsList(glyphslist)
		for v in sortedGlyphsList:
			if len(v['languages']) == len(names):
				v['languages'].append(dict(name = 'All', types = ['alphabet']))
			resultList.append(v)

	return resultList


def makeMainCharactersSet(workPath):
	print('*' * 60)
	print('making MainCharactersSet..')
	# print(workPath)
	basePath, _s = os.path.split(workPath)
	print('basePath: %s' % basePath)
	libraryPath = os.path.join(basePath, 'library')
	print('libraryPath: %s' % libraryPath)

	libraryMainFilePath = os.path.join(basePath, libraryMainFile)
	if not os.path.exists(libraryMainFilePath):
		print('Main library file not found: %s' % libraryMainFilePath)
		return
	print('libraryMainFile: %s' % libraryMainFilePath)


	sortOrderFilePath = os.path.join(basePath, sortOrderFile)
	SortOrderCyrl = None
	if os.path.exists(sortOrderFilePath):
		SortOrderCyrl = PanCyrillicOrderSorter(sortOrderFilePath)
	else:
		print('SortOrder file not found: %s' % sortOrderFilePath)

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
			# print('%s path:%s' % (name, inputJSONfile))

			local = 'ru'
			if os.path.exists(mainfile):
				with open(mainfile, "r") as read_file:
					maindata = json.load(read_file)
				# print('%s path:%s' % (name, mainfile))
				local = maindata['local']

			uppercase_unicodes_list = None
			lowercase_unicodes_list = None
			glyphs_lists = data['glyphs_list']
			for glyphslist in glyphs_lists:
				typelist = glyphslist['type']
				if typelist == 'charset':
					uppercase_unicodes_list = glyphslist['uppercase']
					lowercase_unicodes_list = glyphslist['lowercase']
			if uppercase_unicodes_list and lowercase_unicodes_list:
				unicodedlist_UC, puazonelist_UC, nonunicodedlist_UC = filterCharacters(name, local, uppercase_unicodes_list, unicodedlist_UC, puazonelist_UC, nonunicodedlist_UC)
				unicodedlist_LC, puazonelist_LC, nonunicodedlist_LC = filterCharacters(name, local, lowercase_unicodes_list, unicodedlist_LC, puazonelist_LC, nonunicodedlist_LC)

	UC_unicoded_list = sortGlyphsList({ **unicodedlist_UC, **puazonelist_UC, **nonunicodedlist_UC}, names, sortOrder = SortOrderCyrl)
	# UC_pua_list = sortGlyphsList(puazonelist_UC, names, sortOrder = SortOrderCyrl)
	# UC_nonunicoded_list = sortGlyphsList(nonunicodedlist_UC, names, sortOrder = SortOrderCyrl)
	UC_sorted_list = sortGlyphsList({ **unicodedlist_UC, **puazonelist_UC, **nonunicodedlist_UC}, names)
	LC_unicoded_list = sortGlyphsList({ **unicodedlist_LC, **puazonelist_LC, **nonunicodedlist_LC}, names, sortOrder = SortOrderCyrl)
	LC_sorted_list = sortGlyphsList({ **unicodedlist_LC, **puazonelist_LC, **nonunicodedlist_LC}, names)
	# LC_pua_list = sortGlyphsList(puazonelist_LC, names, sortOrder = SortOrderCyrl)
	# LC_nonunicoded_list = sortGlyphsList(nonunicodedlist_LC, names, sortOrder = SortOrderCyrl)


	dataset = dict(
		uppercase_unicodes_list = UC_unicoded_list,
		lowercase_unicodes_list = LC_unicoded_list,

		uppercase_puazone_list = [], # UC_pua_list,
		lowercase_puazone_list = [], # LC_pua_list,

		uppercase_nonunicode_list = [], # UC_nonunicoded_list,
		lowercase_nonunicode_list = [], # LC_nonunicoded_list,

		uppercase_sorted_by_unicodes = UC_sorted_list,
		lowercase_sorted_by_unicodes = LC_sorted_list,
	)
	outputJSONfile = os.path.join(basePath, 'site', 'cyrillic_characters_lib.json')
	indent = None
	if DEVELOPMENT:
		indent = 4
	with open(outputJSONfile, "w") as write_file:
		json.dump(dataset, write_file, indent = indent, ensure_ascii = False) #indent = 4,
	print('..done')



def main(names = None):
	pathname = os.path.dirname(sys.argv[0])
	workPath = os.path.abspath(pathname)
	compileLagnuages(workPath, names)
	makeMainCharactersSet(workPath)


if __name__ == '__main__':
	main(names = sys.argv[1:])