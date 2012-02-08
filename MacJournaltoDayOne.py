#!/usr/bin/env python2.6
# encoding: utf-8
"""
untitled.py

Created by kdm on 2010-02-10.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

import sys
#import getopt
import time
from datetime import date
from datetime import timedelta
from time import strptime
import os
import string
import subprocess
import shlex
import optparse
import logging
from shutil import copyfileobj

def main(argv=None):
	if argv is None:
		argv = sys.argv
	
#Parse input variables
	
	main_logger = logging.getLogger('main')

	usage = "usage:  %prog [options] <MacJournal File to import>"
	parser = optparse.OptionParser(usage=usage)
	
	parser.add_option("--debug", dest="debug", default=False, action = "store_true", help = "Turn on debug output (default false)")
	
	(options, args) = parser.parse_args()
	
	if len(args) != 1:
		parser.error("File to import required")
	else:
		journal_name = args[0]	
	
	if options.debug:
		logging.basicConfig(level="logging.debug")
	else:
		logging.basicConfig(level="logging.error")
	
	try:
		journal = open(journal_name,'r')
	except:
		main_logger.error("Could not open %s" % journal_name)
		return 1 # Could not open journal

	numEntries = 0
	prevEntryDate = None
	journalEntry = None
	curEntryLines = 0
	prevEntryLines = 0
	continueLoop = True
	entryDone = False
	curEntryDate = None
	prevEntry = ''
	curEntry = ''

	#Due to python's lack of a DO/UNTIL statement, have to do things a bit differently
	
	while continueLoop is True:
	
		entryLine = journal.readline()
	
		if not entryLine: #Reached EOF
			entryDone = True
			continueLoop = False
			prevEntryDate = curEntryDate
			prevEntry = curEntry
			prevEntryLines = curEntryLines
			curEntry = ''
			curEntryLines = 0

			print("Reached EOF")
	
		if entryLine.startswith("\tDate:\t"): # An entry is finished
			prevEntryDate = curEntryDate
			prevEntry = curEntry
			prevEntryLines = curEntryLines
			curEntry = ''
			curEntryLines = 0
			curEntryDate = entryLine.replace("\tDate:\t",'').rstrip()
			entryDone = True
			print("Found entry " + curEntryDate)
		elif entryLine is not "":
			curEntry += entryLine
			curEntryLines += 1

		if (entryDone is True) and (prevEntryLines is not 0):
			#Write output to DayOne
			print '{0} has {1} lines'.format(prevEntryDate,repr(prevEntryLines))
			addCommandParsed = ['/Applications/Day One.app/Contents/MacOS/dayone', '-d="' + format(prevEntryDate) +'"', 'new']
			print addCommandParsed
			try:
				addCommandProcess = subprocess.Popen(addCommandParsed,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			except:
				None
			addCommandOut = addCommandProcess.communicate(prevEntry)
			print addCommandOut[0]
			print addCommandOut[1]
			numEntries += 1
			entryDone = False
			prevEntryDate = None
			prevEntry = None
			prevEntryLines = 0


	print("Found %s entries" % numEntries)
	
	journal.close()
	
	return 0

if __name__ == "__main__":
	sys.exit(main())
