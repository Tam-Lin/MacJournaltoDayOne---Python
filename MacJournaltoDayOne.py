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

	###Fencepost problem - you are picking up, but not writing out, the final entry

	for line in journal:
		if line.startswith("\tDate:	"):
			if ((entrydate is not None) and (journalEntry is not None)): #There's an entry and an associated date
				#Add entry to DayOne
				print(entrydate + " has " + repr(entryLines) + " lines")
				entrydate = None
			elif ((entrydate is not None) and (journalEntry is None)): #We have an entry date with no associated entry
				return 2
			elif ((entrydate is None) and (journalEntry is not None)): #We have an entry but not associated date
				return 3

			entries +=1
			entrydate = line.replace("\tDate:\t",'')
			journalEntry = None
			entryLines = 0

		else:
			if entrydate is not None:
				print("Reading entry")
			
				if journalEntry is not None:
					journalEntry = journalEntry  + line
					entryLines += 1
					print("Not first line")
				else:
					journalEntry = line
					entryLines = 1
					print("First line")

	print("Found %s entries" % entries)
	
	journal.close()
	
	return 0

if __name__ == "__main__":
	sys.exit(main())
