# -*- coding: utf-8 -*-

import json
import os.path

def main ():
	codeslangfile = '/Users/alexander/GitHub/PythonWorks/cyrillic_lib/cyrillic-languages/cyrillic_library.json'
	with open(codeslangfile, "r") as read_file:
		data = json.load(read_file)

	for item in data:
		item['enable'] = True
		print (item)
	# data['enable'] = True
	#
	outputJSONfile = codeslangfile
	with open(outputJSONfile, "w") as write_file:
		json.dump(data, write_file, indent = 4, ensure_ascii = False)


if __name__ == "__main__":
	main()
