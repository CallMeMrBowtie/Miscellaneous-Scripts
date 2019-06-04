#!/usr/bin/python
from optparse import OptionParser
from subprocess import Popen, PIPE
from sets import Set
import os
import sys


class bcolours:
    PURPLE = '\033[95m'
    D_BLUE = '\033[94m'
    GREEN = '\033[92m'
    BLUE = '\033[96m'
    RED = '\033[91m'
    ENDC = '\033[0m'

def optional_arg(arg_default):
    def func(option,opt_str,value,parser):
        if parser.rargs and not parser.rargs[0].startswith('-'):                                       
            val=parser.rargs[0]
            parser.rargs.pop(0)
        else:
            val=arg_default
        setattr(parser.values,option.dest,val)
    return func


alpha=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

# read contents of a file into an array
def readFromFile(filename):
	f = open(filename, "r") 
	lines = f.readlines()
	f.close()

	i=0
	while i<len(lines):
		lines[i] = lines[i].rstrip()
		i=i+1

	return lines

def outputToFile(filename,files):
        f = open(filename, "w")
        i=0
        x=0
        while i < len(files):
                x=0
                while x<len(files[i]):
                        f.write(str(files[i][x]) + '\n')                                               
                        x=x+1
                i=i+1

add_unique_symbol = False
breach_creds_filename = ""

parser = OptionParser("usage: %prog credsfile")

parser.add_option("-f", "--filename",
                  action="callback",callback=optional_arg('xxxemptyxxx'), 
                  dest="breach_creds_filename", default="",
                  help="Breach creds filename.")
parser.add_option("-s", "--symbol",
                  action='store_true',                              
                  dest="add_unique_symbol", default=False,
                  help="Add *** to the start of every duplicate.")                                     

(options, args) = parser.parse_args()

print bcolours.D_BLUE+" -_/\_/\_/\_- "+bcolours.BLUE+"Breach Creds Duplicate Highlighter"+bcolours.D_BLUE+" -_/\_/\_/\_- "+bcolours.ENDC


num_files = len(sys.argv)
file_not_found = ""
output_file = sys.argv[num_files-1]
usernames = []
passwords = []

if options.add_unique_symbol == True:
	unique_symbol = "***"
else:
	unique_symbol = ""

if options.breach_creds_filename == "" or options.breach_creds_filename == 'xxxemptyxxx':
	parser.print_help()
else:
	# read each file
	file = readFromFile(options.breach_creds_filename)

	# check if a '/' is in the first area before the ':' (if so, it's rubbish, if not, the rubbish has already been removed & it's a username)
	num=0
	if "/" in file[0].split(':')[0]:
		num=1

	# extract the rubbish
	new_file = []
	i=0
	while i < len(file):
		new_file.append(str(file[i].split(':',num)[num:]))
		i=i+1
	
	# sort the data alphabetically
	new_file.sort(key=str.lower)

	# extract the usernames & pwds
	i=0
	while i < len(new_file):
		usernames.append(new_file[i].split(':')[0][2:])
		if ':' not in new_file[i]:
			passwords.append("")
		else:
			passwords.append(new_file[i].split(':')[1][:-2])
		i=i+1

	# check whether each username is the same as the previous or next one and, if so, append a 'true' to an array instead of 'false'
	is_duplicate = []
	i=0
	while i < len(new_file):
		duplicate = False
		if i > 0:
			if usernames[i].lower() == usernames[i-1].lower():
				duplicate = True
		if i < len(new_file)-1:
			if usernames[i].lower() == usernames[i+1].lower():
				duplicate = True
		is_duplicate.append(duplicate)
		i=i+1
	
	# print the usernames & pwds, highlighting the duplicate usernames
	print ""
	i=0
	while i < len(new_file):
		if is_duplicate[i] == True:
			print unique_symbol + bcolours.BLUE+usernames[i]+bcolours.ENDC + ":" + passwords[i]
		else:
			print usernames[i] + ":" + passwords[i]
		i=i+1


