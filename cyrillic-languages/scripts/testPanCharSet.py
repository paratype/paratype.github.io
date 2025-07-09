import sys
import json
import os.path
import random
import string


libraryMainFile = 'cyrillic_library.json'
libraryGlyphsList = 'glyphs_list_categories.json'
unicodeLibFiles = ['unicode14.txt', 'PT_PUA_unicodes-descritions.txt']

def checkType(unicodes_list, globaltypes, language):
	for item in unicodes_list:
		if item['types']:
			for t in item['types']:
				if t not in globaltypes:
					globaltypes.append(t)
			if len(item['types']) != 1:
				print(item['sign'], item['types'])
		else:
			print('&&&', item['sign'], item['types'], language)
	return globaltypes


def testCharactersSet(workPath):
	print('*' * 60)
	print('testing MainCharactersSet')
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
	globaltypes = []
	emptydescriptions_upper = {}
	emptydescriptions_lower = {}
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
			# print('LOCAL:', local)

			uppercase_unicodes_list = None
			lowercase_unicodes_list = None
			glyphs_lists = data['glyphs_list']
			for glyphslist in glyphs_lists:
				typelist = glyphslist['type']
				if typelist == 'charset':
					uppercase_unicodes_list = glyphslist['uppercase']
					lowercase_unicodes_list = glyphslist['lowercase']

			if uppercase_unicodes_list and lowercase_unicodes_list:
				for item in uppercase_unicodes_list:
					if item['types']:
						for t in item['types']:
							if t not in globaltypes:
								globaltypes.append(t)
						if len(item['types']) != 1:
							print(item['sign'], item['types'])
					else:
						print('&&&', item['sign'], item['types'], name)
					if not item['description']:
						emptydescriptions_upper[item['unicodes'][0]] = ( item['sign'], name )
						# print('empty description', item['sign'], item['unicodes'], item['types'], name)

				# globaltypes.extend(checkType(uppercase_unicodes_list, globaltypes, name))
				# globaltypes.extend(checkType(lowercase_unicodes_list, globaltypes, name))
				for item in lowercase_unicodes_list:
					if item['types']:
						for t in item['types']:
							if t not in globaltypes:
								globaltypes.append(t)
						if len(item['types']) != 1:
							print(item['sign'], item['types'])
					else:
						print ('&&&',item['sign'], item['types'], name)
					if not item['description']:
						emptydescriptions_lower[item['unicodes'][0]] = (item['sign'], name)
						# print('empty description', item['sign'], item['unicodes'], item['types'], name)

	print ('All types:\n%s' % ('\n'.join(globaltypes)))
	if emptydescriptions_upper or emptydescriptions_lower:
		print ('Empty descritions Upper:')
		for k,v in emptydescriptions_upper.items():
			print ('%s = %s = CYRILLIC CAPITAL LETTER %s' % (v[0], k, v[1]))
		print('Empty descritions Lower:')
		for k,v in emptydescriptions_lower.items():
			print ('%s = %s = CYRILLIC SMALL LETTER %s' % (v[0], k, v[1]))

		print ('Empty descritions Upper:')
		for k,v in emptydescriptions_upper.items():
			print ('%s\tCYRILLIC CAPITAL LETTER %s' % (k, v[0]))
		print('Empty descritions Lower:')
		for k,v in emptydescriptions_lower.items():
			print ('%s\tCYRILLIC SMALL LETTER %s' % (k, v[0]))



def main (names=None):
	pathname = os.path.dirname(sys.argv[0])
	workPath = os.path.abspath(pathname)
	testCharactersSet(workPath)

if __name__ == '__main__':
	main(names = sys.argv[1:])