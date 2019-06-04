#!/usr/bin/python
import sys
from optparse import OptionParser
from subprocess import Popen, PIPE
import os
import readline

# parse in dns recon out file path or use current working dir to load it
# parse in list of IPs in-scope
# go through each line checking whether the in-scope IP is in each line of the dns recon output. amend an array part to true if it is
# print the dns recon output again but print the lines in colour which have IPs that are in-scope


alpha=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

class bcolours:
    PURPLE = '\033[95m'
    D_BLUE = '\033[94m'
    GREEN = '\033[92m'
    BLUE = '\033[96m'
    RED = '\033[91m'
    ENDC = '\033[0m'


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

def optional_arg(arg_default):
    def func(option,opt_str,value,parser):
        if parser.rargs and not parser.rargs[0].startswith('-'):
            val=parser.rargs[0]
            parser.rargs.pop(0)
        else:
            val=arg_default
        setattr(parser.values,option.dest,val)
    return func


parser = OptionParser()
parser.add_option("-d", "--dns-output",
                  action="callback",callback=optional_arg('xxxemptyxxx'), 
                  dest="dns_output", default="",
                  help="The dnsrecon/fiece output file")
parser.add_option("-i", "--ips-in-scope",
                  action="callback",callback=optional_arg('xxxemptyxxx'), 
                  dest="ips_inscope", default="",
                  help="The list of the individual in-scope IPs")
parser.add_option("-x", "--extract",
                  action="store_true", 
                  dest="extract_IPs", default=False,
                  help="Extract the lines that match from the output")

(options, args) = parser.parse_args()

def print_banner():
	print bcolours.D_BLUE+"\n -_/\_/\_/\_- "+bcolours.PURPLE+"IDENTIFY IN-SCOPE DNS RESULTS"+bcolours.D_BLUE+" -_/\_/\_/\_- \n"+bcolours.ENDC
	return None

if os.path.exists(options.dns_output) == False:
	if os.path.exists(options.ips_inscope) == False:
		print_banner()
		parser.print_help()
		print ""
	else:
		print_banner()
		print "Sorry the DNS output file wasn't found :(\n"
elif os.path.exists(options.ips_inscope) == False:
	print_banner()
	print "Sorry the in-scope IPs file wasn't found :(\n"
else:
	dns_output_file = readFromFile(options.dns_output)
	ips_inscope_file = readFromFile(options.ips_inscope)

	results = [False] * len(dns_output_file)
	x=0
	y=0
	while x < len(ips_inscope_file):
		y=0
		while y < len(dns_output_file):
			if dns_output_file[y].endswith(" "+ips_inscope_file[x]):
				results[y] = True
			y=y+1
		x=x+1

	y=0
	if options.extract_IPs == True:
		while y < len(dns_output_file):
			if results[y] == True:
				print dns_output_file[y]
			y=y+1
	
	else:
		while y < len(dns_output_file):
			if results[y] == True:
				print bcolours.PURPLE+dns_output_file[y]+bcolours.ENDC
			else:
				print dns_output_file[y]
			y=y+1

