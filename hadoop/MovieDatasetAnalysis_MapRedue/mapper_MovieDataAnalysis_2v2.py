#!/usr/bin/env python

import sys

for line in sys.stdin:
	dataToken = line.strip().split("::")
	if(len(dataToken)>=3): # check for empty line or false data
		print('%s=%s' % (dataToken[0],dataToken[2]))

