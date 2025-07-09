
import re

dangersymbols = {
	'\t' : '',
    '\"' : '\''
}
#
# class CyrillicOrderSorter(object):
#
# 	def __init__(self, sortorderfile):
#
# 		self.missigChars = {}
# 		print ('Initializing sorting keys..')
#
# 		f = open(sortorderfile, mode = 'r')
# 		self.upperlist = []
# 		self.lowerlist = []
# 		for idx, line in enumerate(f):
# 			line = line.strip()
# 			line = re.sub("\s\s+" , " ", line)
# 			if line and not line.startswith('#'):
# 				rawline = line.split('/')
# 				rawupper, rawlower = None, None
# 				if len(rawline) == 2:
# 					rawupper = rawline[0]
# 					rawlower = rawline[1]
# 				elif len(rawline) == 1:
# 					rawupper = rawline[0]
# 				else:
# 					print ('ERROR', sortorderfile, idx)
# 				if rawupper:
# 					# sign = rawupper.split('=')[0]
# 					uni = rawupper.split('=')[1]
# 					# sign = chr(int(uni,16))
# 					self.upperlist.append(uni)
# 				if rawlower:
# 					# sign = rawlower.split('=')[0]
# 					uni = rawlower.split('=')[1]
# 					# sign = chr(int(uni, 16))
# 					self.lowerlist.append(uni)
# 		self.sortkey = self.upperlist + self.lowerlist
# 		# print (self.sortkey)
# 		print ('..done')
#
# 	def getSortedCyrillicList(self, characherslist, lang = None):
# 		result = []
# 		for ch in self.sortkey:
# 			if ch in characherslist and ch not in result:
# 				result.append(ch)
#
# 		# for ch in characherslist:
# 		# 	if ch not in self.sortkey:
# 		# 		if ch not in self.missigChars:
# 		# 			sfx = ''
# 		# 			_ch = ch
# 		# 			if '.alt' in ch:
# 		# 				_ch = ch.replace('.alt','')
# 		# 				sfx = '.alt'
# 		# 			self.missigChars[ch] = ( chr(int(_ch,16))+'.alt', lang)
# 		return result
#


class CharacherDescription(object):
	def __init__(self, unicodelibfile):
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
			for k,v in dangersymbols.items():
				r = r.replace(k, v)
			return r #self.stuct[unicodechar].strip().replace('\t','')
		else:
			return ''

