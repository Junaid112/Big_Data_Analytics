#!/usr/bin/env python


import sys
import os
import fileinput # import this to read multiple files

try:
	inputF=os.environ['map_input_file']
except KeyError:
	print("Error")

for dataLine in sys.stdin:
	filePath=inputF.strip().split("/")# removing pre and after unnecessary space
	fileNo=filePath[-2]
	if(not dataLine.isspace()):
		tokenInLine=dataLine.split(' ')
		for w in tokenInLine:	
			if(not w.isspace()):
				print("%s\t%s" % (w,fileNo[0])) #simply this lien to reducer
