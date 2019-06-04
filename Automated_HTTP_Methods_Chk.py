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


def readFromFile(filename):
	f = open(filename, "r") 
	lines = f.readlines()
	lines.sort()
	f.close()

	i=0
	while i<len(lines):
		lines[i] = str(lines[i]).decode('string_escape')
		i=i+1

	return lines

def printHelp():
	print bcolours.BLUE+"\n\t -- Burp 'URLs in this host' output > list of web directories: --"+bcolours.ENDC
	print "./Automated_HTTP_Methods_Chk.py"+bcolours.PURPLE+" -o 1 -f <path_&_file_containing_Burp_output>"+bcolours.ENDC
	print "\t\t(Note: If there's files in the above output, they're probably just API endpoints!)"
	print bcolours.BLUE+"\n\t -- List of web directories > NSE script to detect HTTP methods: --"+bcolours.ENDC
	print "./Automated_HTTP_Methods_Chk.py"+bcolours.PURPLE+" -o 2 -f <path_&_file_containing_web_directories> -i <target_ip> -p <port_web_server_is_on>\n\n"+bcolours.ENDC


parser = OptionParser()
parser.add_option("-o", "--options",
                  action="callback",callback=optional_arg('xxxemptyxxx'), 
                  dest="options", default="",
                  help="2 options for running the program")
parser.add_option("-f", "--file-path",
                  action="callback",callback=optional_arg('xxxemptyxxx'), 
                  dest="file", default="",
                  help="The input file for the options specified")
parser.add_option("-i", "--target-ip",
                  action="callback",callback=optional_arg('xxxemptyxxx'), 
                  dest="ip", default="",
                  help="Target IP/URL")
parser.add_option("-p", "--target-port",
                  action="callback",callback=optional_arg('xxxemptyxxx'), 
                  dest="port", default="",
                  help="Target Port")

(options, args) = parser.parse_args()

print bcolours.D_BLUE+" -_/\_/\_/\_- "+bcolours.BLUE+"AUTOMATED HTTP METHODS CHECK"+bcolours.D_BLUE+" -_/\_/\_/\_- \n"+bcolours.ENDC


# if -o is working
continue_exec = False

if (options.options != "") and (options.options != "xxxemptyxxx"):
	continue_exec = True
	option = int(options.options)
if (continue_exec == True) and (option > 0) and (option < 3):
	file = readFromFile(options.file)

	if option == 1:
		i=0
		dir_list = []
		while i<len(file):
			char_loc = file[i].rfind('/')
			end_string = file[i][char_loc:]
			if "." not in end_string:
				if len(end_string) == 3:
					file[i] = file[i][:-3]
				entry = (file[i].rstrip('\n'))
				entry = entry.rstrip('\r')
				loc = (entry.find("/", entry.find("/") + 2))
				dir_list.append(entry[loc:])
			i=i+1
		keys = {}
		for e in dir_list:
			keys[e] = 1
		final_dir_list = (list(keys.keys()))
		final_dir_list.sort()
		i=0
		while i< len(final_dir_list):
			print final_dir_list[i]
			i=i+1
	elif option == 2:
		print "Error! Code: 100"
	else:
		print "ERROR! Code: 101"
else:
	printHelp()

