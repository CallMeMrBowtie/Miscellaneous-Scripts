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

parser = OptionParser("usage: %prog file1 file2 ... outfile")
parser.add_option("-d", "--debug",
                  action="callback",callback=optional_arg('xxxemptyxxx'), 
                  dest="debug", default="",
                  help="Run the script in debug mode (currently not implemented!)")

(options, args) = parser.parse_args()

print bcolours.D_BLUE+" -_/\_/\_/\_- "+bcolours.BLUE+"NESSUS COMBINER"+bcolours.D_BLUE+" -_/\_/\_/\_- \n"+bcolours.ENDC

num_files = len(sys.argv)
file_not_found = ""
files = list()
output_file = sys.argv[num_files-1]

if num_files < 2:
	parser.print_help()
else:
	i=1
	print bcolours.BLUE+"Processing:"+bcolours.ENDC
	while i < num_files-1:
		print bcolours.D_BLUE + '\t' + sys.argv[i] + bcolours.ENDC
		exists = os.path.isfile(sys.argv[i])
		if exists:
			files.append(readFromFile(sys.argv[i]))
		else:
			file_not_found = sys.argv[i]
		i=i+1
	print ""

	if file_not_found != "":
		print "File '" + file_not_found + "' doesn't exist :(\n"
		parser.print_help()
		print ""
	else:
		i=0
		while i < num_files-3:
			files[i].remove("</Report>")
			files[i].remove("</NessusClientData_v2>")
			i=i+1
		i=1
		while i < num_files-2:
			indices = []
			for y, elem in enumerate(files[i]):
				if '<Report name=' in elem:
					indices.append(y)
			del files[i][0:indices[0]+1]
			i=i+1


		# check if output file exists
		exists = os.path.isfile(output_file)
		if exists:
			print "File '" + output_file + "' already exists :(\n"
		else:
			# output to file
			print bcolours.BLUE + "Outputing nessus data to: " + bcolours.D_BLUE + sys.argv[num_files-1] + '\n' + bcolours.ENDC
			outputToFile(output_file,files)
			print bcolours.BLUE + "Done :)\n" + bcolours.ENDC

