
import json
import sys, os.path
import glob
from fontParts.world import OpenFont #.world import *



marks = ['*', '$', '#', '@', '(', ')', '[', ']', '+', '=', '&', '.alt']  # , '.alt'

dialectsign = '@'
historicsign = '#'
lexicsign = '$'
alternatesign = '+'
equivalentsign = '='
featuresign = '&'

signtypes = {
	# '*' : 'notrussiansign',
	dialectsign: 'dialectsign',
	historicsign: 'historicsign',  # oldersign
	lexicsign: 'lexicsign',  # lexicosign
	alternatesign: 'alternatesign',
	equivalentsign: 'equivalentsign',
	featuresign: 'featuresign',
	# '.alt' : 'featuresignalt'
}

locales = {
	'ba': ['alt', 'BSH'],
	'bg': ['BGR'],
	'sr-Cyrl-CS': ['SRB'],
	'CYR': [''],
	'cv': ['alt02', 'CHU']
}
ignoredLanguages = [] #'Russian Old (XIX)', 'Russian Ancient (XVIII)', 'Russian Church (X-XVII)'
fontsStorage = []


def getFontFilesList (fontsFolder, ext='*.ufo'):
	filepath = os.path.join(fontsFolder, ext)
	listoffilepaths = glob.glob(filepath)
	listoffilenames = []
	for filename in listoffilepaths:
		listoffilenames.append(filename)
	return listoffilenames

def loadFonts2Storage(path):
	fontsPathsList = getFontFilesList(path)
	for fontpath in fontsPathsList:
		font = OpenFont(fontpath)
		fontsStorage.append(font)
		print (font.info.familyName, font.info.styleName)
		print (fontpath)
		print ('Loaded..')
		# print (font.getCharacterMapping())
		# print (f)

def main (ufofolder = None):

	pathname = os.path.dirname(sys.argv[0])
	workPath = os.path.abspath(pathname)

	libraryPath = 'library'  # langlib
	outputPath = 'site'
	outputLibraryPath = 'baselib'
	libraryMainFile = 'cyrillic_library.json'
	print ('*'*60)
	print ('Testing of UFO files for language support has started')
	print (workPath)
	basePath, _s = os.path.split(workPath)
	# print ('basePath: %s' % basePath)
	libraryPath = os.path.join(basePath, libraryPath)
	print ('libraryPath: %s' % libraryPath)

	libraryMainFile = os.path.join(basePath, libraryMainFile)
	if not os.path.exists(libraryMainFile):
		print ('Main library file not found: %s' % libraryMainFile)
		return
	print ('libraryMainFile: %s' % libraryMainFile)

	if not ufofolder: return
	loadFonts2Storage(path = ufofolder[0])

	#os.path.join(path2langlib, codeslangfile)
	with open(libraryMainFile, "r") as read_file:
		data = json.load(read_file)
	# print (data)
	# names = ['Avar']
	names = []

	if not names:
		for item in data:
			name = item['name_eng']
			if name not in ignoredLanguages:
				names.append(name)
	missgloballist = {}
	for name in names:
		# if name in ignoredLanguages: break
		# lname =
		namefiledata = os.path.join(basePath, outputPath, outputLibraryPath, '%s.json' % name)
		with open(namefiledata, "r") as read_file:
			data = json.load(read_file)
		uppercase_unicodes_list = data['uppercase_unicodes_list']
		lowercase_unicodes_list = data['lowercase_unicodes_list']

		namefilelang = os.path.join(libraryPath, '%s.json' % name)
		with open(namefilelang, "r") as read_file:
			datalang = json.load(read_file)
		local = datalang['local']

		data_unicodes_list = uppercase_unicodes_list + lowercase_unicodes_list
		unicodes_list = []
		for item in data_unicodes_list:
			sfxraw = item['types']
			uni = item['unicode']
			if sfxraw and signtypes[featuresign] in sfxraw:
				# for sfx in locales[local]:
				# 	_uni = '%s.%s' % (uni, sfx)
				# 	unicodes_list.append(_uni)
				uni += '*'

			unicodes_list.append(uni)
		# print(name, unicodes_list)
		missingGlyphs = False
		# missingGlyphsList = {}
		missingGlyphsListFonts = {}
		missingQuestionable = {}
		for uni in unicodes_list:
			# intunilist = []
			if '*' in uni:
				uni = uni.replace('*','')
				_intuni = int(uni, 16)
				for font in fontsStorage:
					fontTitle = '%s %s' % (font.info.familyName, font.info.styleName)
					if _intuni not in font.getCharacterMapping():
						print('***', uni, font.info.familyName, font.info.styleName)
					else:
						f_glyphlist = font.getCharacterMapping()[_intuni]
						founded = False
						for _g in f_glyphlist:
							for sfx in locales[local]:
								gl = '%s.%s' % (_g, sfx)
								if gl in font and not founded:
									founded = True
								elif not founded:
									missingGlyphs = True
									if fontTitle not in missingQuestionable:
										missingQuestionable[fontTitle] = [gl]
									else:
										missingQuestionable[fontTitle].append(gl)

			else:
				intuni = int(uni, 16)
				for font in fontsStorage:
					fontTitle = '%s %s' % (font.info.familyName, font.info.styleName)

					if intuni not in font.getCharacterMapping():
						# if uni not in missingGlyphsList:
						# 	missingGlyphsList[uni] = [fontTitle]
						# else:
						# 	missingGlyphsList[uni].append(fontTitle)
						missingGlyphs = True
						if fontTitle not in missingGlyphsListFonts:
							missingGlyphsListFonts[fontTitle] = [uni]
						else:
							missingGlyphsListFonts[fontTitle].append(uni)

		if missingGlyphs:
			print(name, '=' * (40 - len(name)))

		# for k, v in missingGlyphsList.items():
		# 	print (k, ':')
		# 	print ('\t%s' % '\n\t'.join(v))

		for k, v in missingGlyphsListFonts.items():
			print (k)
			print (' '.join(v), '\n')
			if k not in missgloballist:
				missgloballist[k] = v
			else:
				for _v in v:
					if _v not in missgloballist[k]:
						missgloballist[k].append(_v)
	print('='*40)
	print('Total:')
	for k,v in missgloballist.items():
		print(k)
		print(' '.join(sorted(v)), '\n')



if __name__ == "__main__":
	main(ufofolder = sys.argv[1:])
