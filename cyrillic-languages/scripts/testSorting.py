txt = 'А Б В Г Гу Гъ Гъу Д Дж Дз Дзу Е Ё Ж Жь Жъ Жъу З И Й К Ку Къ Къу КӀ КӀу Л Ль ЛӀ М Н О П ПӀ ПӀу Р С Т ТӀ ТӀу У Ф ФӀ Х Хь Ху Хъ Хъу Ц Цу ЦӀ Ч Чъ ЧӀ Ш Шъ Шъу ШӀ ШӀу Щ Ъ Ы Ь Э Ю Я Ӏ Ӏу'.split(' ')
inputtxt = []
for item in txt:
	if item != 'Ё' and item != 'ё':
		inputtxt.append(item)
outputtxt = []
for item in sorted(txt):
	if item != 'Ё' and item != 'ё':
		outputtxt.append(item)
tttin = ''
tttout = ''
for idx, item in enumerate(inputtxt):
	# if item != 'Ё' and item != 'ё':
	# print (item, outputtxt[idx])
	if item != outputtxt[idx]:
		tttin += item + '\t'
		tttout += outputtxt[idx] + '\t'
print(tttin)
print(tttout)